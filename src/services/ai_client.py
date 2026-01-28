"""
AI Client for parsing natural language with OpenAI/DeepSeek/custom endpoints.
"""
import json
from typing import Optional, Dict, Any
from datetime import datetime
import time
import openai
import httpx
from ..models.ai_config import AIConfiguration
from ..models.parse_result import ParseResult
from ..models.calendar_event import CalendarEvent
from ..models.reminder import Reminder
from ..utils.logger import get_logger

logger = get_logger(__name__)


class AIClient:
    """AI service abstraction for parsing natural language."""

    def __init__(self, config: AIConfiguration):
        """
        Initialize AI client.
        
        Args:
            config: AI configuration
        """
        self.config = config
        self._openai_client: Optional[openai.OpenAI] = None

    def _get_openai_client(self) -> openai.OpenAI:
        """Get or create OpenAI client."""
        if not self._openai_client:
            self._openai_client = openai.OpenAI(
                api_key=self.config.api_key,
                base_url=self.config.api_endpoint,
                timeout=self.config.timeout,
            )
        return self._openai_client

    def _build_system_prompt(self) -> str:
        """Build system prompt for AI."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"""You are a calendar and reminder parsing assistant for macOS. Extract events/reminders from text (English/Chinese).

Current time: {current_time}

Output: Valid JSON only.

Rules:
1. Calendar events MUST have specific times (e.g. 2pm, 14:00, tomorrow morning).
2. Reminders are for tasks without specific times or deadlines.
3. CRITICAL: Titles MUST be short (max 50 chars). 
4. Move all long descriptions, detailed info, or conversational snippets into the 'notes' field.
5. For itineraries, extract each stop as a separate calendar_event.
6. Return ONLY the JSON object. No conversational filler.

JSON Schema:
{{
  "calendar_events": [
    {{
      "title": "Short descriptive title (max 50 chars)",
      "start_date": "ISO8601",
      "end_date": "ISO8601",
      "location": "str|null",
      "notes": "Detailed description/itinerary notes",
      "all_day": bool
    }}
  ],
  "reminders": [
    {{
      "title": "Short task name",
      "due_date": "ISO8601|null",
      "priority": 0-3,
      "notes": "str|null"
    }}
  ],
  "confidence": float,
  "ambiguities": ["str"]
}}"""

    def _build_user_prompt(self, text: str) -> str:
        """Build user prompt with input text."""
        return f"""Parse this text into Calendar Events and Reminders. 
Items with specific times -> calendar_events.
Tasks/Todos -> reminders.

Text:
\"\"\"{text}\"\"\"

Return JSON:"""

    def parse_text(self, text: str) -> ParseResult:
        """
        Parse natural language text to extract events and reminders.

        Args:
            text: User input text

        Returns:
            ParseResult with extracted items
        """
        if not text or not text.strip():
            return ParseResult.error("No text provided", text)

        try:
            # OpenAI, DeepSeek, and custom endpoints all use OpenAI-compatible API
            if self.config.provider in ["openai", "deepseek", "custom"]:
                return self._parse_with_streaming(text)
            else:
                return ParseResult.error(
                    f"Unsupported provider: {self.config.provider}",
                    text
                )
        except Exception as e:
            logger.error(f"AI parsing failed: {e}")
            return ParseResult.error(f"AI service error: {str(e)}", text)

    def _parse_with_streaming(self, text: str) -> ParseResult:
        """Parse with OpenAI-compatible API using streaming."""
        start_time = time.time()
        try:
            client = self._get_openai_client()
            # Always use streaming to prevent timeouts
            stream = client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": self._build_system_prompt()},
                    {"role": "user", "content": self._build_user_prompt(text)},
                ],
                temperature=0.1, # Lower temperature for more consistent JSON
                max_tokens=self.config.max_tokens,
                # Pass max_completion_tokens for newer models (o1, etc.) and some providers
                extra_body={"max_completion_tokens": 4096} if self.config.provider != "openai" else {}, # Limit completion to reasonable size
                response_format={"type": "json_object"},
                stream=True, 
            )
            
            content = ""
            finish_reason = None
            try:
                for chunk in stream:
                    if chunk.choices:
                        if chunk.choices[0].delta.content:
                            content += chunk.choices[0].delta.content
                        if chunk.choices[0].finish_reason:
                            finish_reason = chunk.choices[0].finish_reason
            except Exception as stream_err:
                logger.error(f"Stream interrupted after {len(content)} chars: {stream_err}")
                # Don't raise, try to parse what we have
            
            duration = time.time() - start_time
            logger.info(f"AI request completed in {duration:.2f}s, finish_reason: {finish_reason}, chars: {len(content)}")
            
            return self._parse_ai_response(content, text)

        except openai.AuthenticationError as e:
            logger.error(f"Authentication failed. Url: {self.config.api_endpoint}, Key: {self.config.api_key[:4]}***")
            return ParseResult.error(f"Invalid API key for {self.config.api_endpoint}. Please update configuration.", text)
        except openai.RateLimitError:
            return ParseResult.error("API rate limit exceeded. Try again later.", text)
        except openai.APITimeoutError:
            duration = time.time() - start_time
            logger.error(f"API request timed out after {duration:.2f}s")
            return ParseResult.error(f"API request timed out connecting to {self.config.api_endpoint} ({duration:.1f}s). Check connection.", text)
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return ParseResult.error(f"OpenAI error: {str(e)}", text)

    def _parse_ai_response(self, content: str, original_text: str) -> ParseResult:
        """
        Parse AI JSON response to ParseResult.

        Args:
            content: AI response (JSON string)
            original_text: Original user input

        Returns:
            ParseResult
        """
        try:
            # Try to extract JSON from markdown code blocks if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            data = None
            try:
                data = json.loads(content)
            except json.JSONDecodeError:
                # Recovery strategy: Regex extract complete JSON objects
                import re
                
                data = {
                    "calendar_events": [],
                    "reminders": [],
                    "ambiguities": ["Recovered from truncated response"]
                }
                
                # Extract sections more robustly
                def get_section_text(key, text):
                    match = re.search(f'"{key}"\\s*:\\s*\\[', text)
                    if not match: return ""
                    start = match.end()
                    # Find balanced brackets or end of text
                    bracket_count = 1
                    for i in range(start, len(text)):
                        if text[i] == '[': bracket_count += 1
                        elif text[i] == ']': bracket_count -= 1
                        if bracket_count == 0:
                            return text[start:i]
                    return text[start:]

                events_str = get_section_text("calendar_events", content)
                reminders_str = get_section_text("reminders", content)

                def extract_objects(text):
                    objects = []
                    brace_count = 0
                    start_idx = -1
                    in_string = False
                    escape = False
                    
                    for i, char in enumerate(text):
                        if in_string:
                            if char == '"' and not escape:
                                in_string = False
                            elif char == '\\':
                                escape = not escape
                            else:
                                escape = False
                        else:
                            if char == '"':
                                in_string = True
                            elif char == '{':
                                if brace_count == 0:
                                    start_idx = i
                                brace_count += 1
                            elif char == '}':
                                brace_count -= 1
                                if brace_count == 0 and start_idx != -1:
                                    obj_str = text[start_idx:i+1]
                                    try:
                                        obj_str = obj_str.strip()
                                        obj = json.loads(obj_str)
                                        # Truncate title if it's too long (legacy or recovery issue)
                                        if "title" in obj and isinstance(obj["title"], str) and len(obj["title"]) > 100:
                                            obj["notes"] = (obj.get("notes") or "") + "\n" + obj["title"]
                                            obj["title"] = obj["title"][:50] + "..."
                                        objects.append(obj)
                                    except:
                                        pass
                                    start_idx = -1
                    
                    # If we have a trailing unclosed object, try to close it and parse
                    if brace_count > 0 and start_idx != -1:
                        try:
                            candidate = text[start_idx:]
                            if candidate.count('"') % 2 != 0: candidate += '"'
                            candidate += '}' * brace_count
                            obj = json.loads(candidate)
                            if "title" in obj and isinstance(obj["title"], str) and len(obj["title"]) > 100:
                                obj["notes"] = (obj.get("notes") or "") + "\n" + obj["title"]
                                obj["title"] = obj["title"][:50] + "..."
                            objects.append(obj)
                        except: pass
                        
                    return objects

                data["calendar_events"] = extract_objects(events_str)
                data["reminders"] = extract_objects(reminders_str)
                
                if not data["calendar_events"] and not data["reminders"]:
                     logger.error(f"Failed to recover any data. Raw: {content[:100]}...")
                     raise json.JSONDecodeError("Could not recover JSON data", content, 0)
                
                logger.info(f"Recovered {len(data['calendar_events'])} events and {len(data['reminders'])} reminders")
            
            if not isinstance(data, dict):
                 raise ValueError(f"Parsed content is not a dictionary. Got: {type(data)}")

            # Parse calendar events
            calendar_events = []
            for event_data in data.get("calendar_events", []):
                try:
                    start_str = event_data.get("start_date")
                    end_str = event_data.get("end_date")
                    
                    if not isinstance(start_str, str):
                        logger.warning(f"Skipping event with invalid start date: {event_data}")
                        continue

                    start_date = datetime.fromisoformat(start_str)
                    
                    # Handle missing end date
                    if isinstance(end_str, str):
                        try:
                            end_date = datetime.fromisoformat(end_str)
                        except ValueError:
                            logger.warning(f"Invalid end date format, defaulting to 1 hour: {end_str}")
                            from datetime import timedelta
                            end_date = start_date + timedelta(hours=1)
                    else:
                        # Default to 1 hour if missing
                        from datetime import timedelta
                        end_date = start_date + timedelta(hours=1)

                    event = CalendarEvent(
                        title=event_data["title"],
                        start_date=start_date,
                        end_date=end_date,
                        location=event_data.get("location"),
                        notes=event_data.get("notes"),
                        all_day=event_data.get("all_day", False),
                    )
                    if event.validate():
                        calendar_events.append(event)
                except (KeyError, ValueError) as e:
                    logger.warning(f"Failed to parse event: {e}")

            # Parse reminders
            reminders = []
            for reminder_data in data.get("reminders", []):
                try:
                    due_date_str = reminder_data.get("due_date")
                    due_date = None
                    if isinstance(due_date_str, str):
                         try:
                             due_date = datetime.fromisoformat(due_date_str)
                         except ValueError:
                             logger.warning(f"Invalid reminder due date: {due_date_str}")
                    
                    reminder = Reminder(
                        title=reminder_data["title"],
                        notes=reminder_data.get("notes"),
                        due_date=due_date,
                        priority=reminder_data.get("priority", 0),
                    )
                    if reminder.validate():
                        reminders.append(reminder)
                except (KeyError, ValueError) as e:
                    logger.warning(f"Failed to parse reminder: {e}")

            result = ParseResult(
                calendar_events=calendar_events,
                reminders=reminders,
                raw_text=original_text,
                confidence=data.get("confidence", 1.0),
                ambiguities=data.get("ambiguities", []),
                raw_response=content,
            )

            if result.is_empty():
                result.errors.append(
                    "No calendar events or reminders found. Try being more specific."
                )

            return result

        except json.JSONDecodeError as e:
            snippet = content[:100] if content else "Empty response"
            logger.error(f"Failed to parse AI response as JSON: {e}. Content snippet: {snippet}")
            return ParseResult.error(
                f"AI returned invalid format: {snippet}...", original_text
            )
        except Exception as e:
            logger.error(f"Error parsing AI response: {e}")
            return ParseResult.error(f"Parsing error: {str(e)}", original_text)
