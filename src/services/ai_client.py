"""
AI Client for parsing natural language with OpenAI/DeepSeek/custom endpoints.
"""
import json
from typing import Optional, Dict, Any
from datetime import datetime
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
        return f"""You are a calendar and reminder parsing assistant. Your task is to extract calendar events and reminders from natural language text in English or Chinese.

Current date/time: {current_time}
User timezone: (inferred from system)

Output Format: JSON only, no additional text.

Rules:
1. Calendar events MUST have explicit time references (e.g., "3pm", "下午3点", "15:00")
2. Reminders are for action items without specific times (e.g., "remind me to...", "buy milk")
3. Extract as much detail as possible: title, date, time, location, notes
4. Use current date/time as reference for relative dates ("tomorrow", "next week", "明天")
5. If ambiguous, note it in the "ambiguities" field

Output JSON schema:
{{
  "calendar_events": [
    {{
      "title": "string",
      "start_date": "ISO 8601 datetime",
      "end_date": "ISO 8601 datetime",
      "location": "string or null",
      "notes": "string or null",
      "all_day": boolean
    }}
  ],
  "reminders": [
    {{
      "title": "string",
      "due_date": "ISO 8601 datetime or null",
      "priority": 0-3,
      "notes": "string or null"
    }}
  ],
  "confidence": 0.0-1.0,
  "ambiguities": ["list of warnings"]
}}"""

    def _build_user_prompt(self, text: str) -> str:
        """Build user prompt with input text."""
        return f"""Parse the following text and extract all calendar events and reminders:

Text: "{text}"

Return JSON only."""

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
                return self._parse_with_openai(text)
            else:
                return ParseResult.error(
                    f"Unsupported provider: {self.config.provider}",
                    text
                )
        except Exception as e:
            logger.error(f"AI parsing failed: {e}")
            return ParseResult.error(f"AI service error: {str(e)}", text)

    def _parse_with_openai(self, text: str) -> ParseResult:
        """Parse with OpenAI API."""
        try:
            client = self._get_openai_client()
            response = client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": self._build_system_prompt()},
                    {"role": "user", "content": self._build_user_prompt(text)},
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content
            return self._parse_ai_response(content, text)

        except openai.AuthenticationError as e:
            logger.error(f"Authentication failed. Url: {self.config.api_endpoint}, Key: {self.config.api_key[:4]}***")
            return ParseResult.error(f"Invalid API key for {self.config.api_endpoint}. Please update configuration.", text)
        except openai.RateLimitError:
            return ParseResult.error("API rate limit exceeded. Try again later.", text)
        except openai.APITimeoutError:
            return ParseResult.error(f"API request timed out connecting to {self.config.api_endpoint}. Check connection.", text)
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

            data = json.loads(content)

            # Parse calendar events
            calendar_events = []
            for event_data in data.get("calendar_events", []):
                try:
                    event = CalendarEvent(
                        title=event_data["title"],
                        start_date=datetime.fromisoformat(event_data["start_date"]),
                        end_date=datetime.fromisoformat(event_data["end_date"]),
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
                    reminder = Reminder(
                        title=reminder_data["title"],
                        notes=reminder_data.get("notes"),
                        due_date=datetime.fromisoformat(reminder_data["due_date"])
                        if reminder_data.get("due_date")
                        else None,
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
            logger.error(f"Failed to parse AI response as JSON: {e}")
            return ParseResult.error(
                "AI returned invalid format. Please try again.", original_text
            )
        except Exception as e:
            logger.error(f"Error parsing AI response: {e}")
            return ParseResult.error(f"Parsing error: {str(e)}", original_text)
