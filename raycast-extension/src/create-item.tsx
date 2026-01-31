import {
    ActionPanel,
    Action,
    Form,
    showToast,
    Toast,
    List,
    Icon,
    Color,
    AI,
    environment,
    getPreferenceValues,
} from "@raycast/api";
import { useState } from "react";
import { parseInput, executeCommand, CLIResult } from "./python-bridge";

interface Preferences {
    useRaycastAI: boolean;
}

// System prompt for parsing natural language to calendar events/reminders
const PARSE_SYSTEM_PROMPT = `You are a calendar and reminder assistant. Parse the user's natural language input and extract event/reminder information.

Output ONLY valid JSON in this exact format:
{
  "type": "calendar_event" | "reminder",
  "title": "string",
  "start_time": "ISO 8601 datetime string or null",
  "end_time": "ISO 8601 datetime string or null",
  "location": "string or null",
  "due_date": "ISO 8601 datetime string or null (for reminders)",
  "priority": 0-3 (for reminders, 0=none, 1=low, 2=medium, 3=high),
  "notes": "string or null"
}

Rules:
1. If the input mentions a specific time (e.g., "2pm", "下午3点"), it's a calendar_event
2. If the input says "remind me" or is a task without specific time, it's a reminder
3. Use the current date as reference for relative dates like "tomorrow", "next week"
4. Parse both English and Chinese natural language`;

async function parseWithRaycastAI(text: string): Promise<CLIResult> {
    try {
        const currentDate = new Date().toISOString();
        const prompt = `Current date/time: ${currentDate}\n\nUser input: ${text}\n\nParse this and return JSON:`;

        const response = await AI.ask(prompt, {
            model: "gpt-4o-mini",
            creativity: "low",
        });

        // Try to parse the JSON from response
        const jsonMatch = response.match(/\{[\s\S]*\}/);
        if (!jsonMatch) {
            return { success: false, error: "Failed to parse AI response" };
        }

        const parsed = JSON.parse(jsonMatch[0]);

        // Now call the Python CLI to create the actual event/reminder
        // We'll pass the pre-parsed data to avoid needing the Python AI client
        const args = ["parse", text];
        const result = await executeCommand(args);

        if (!result.success) {
            // If Python CLI fails (likely not configured), show what we parsed
            return {
                success: true,
                message: "Parsed with Raycast AI (Preview only - configure Python backend to create items)",
                items: [{
                    type: parsed.type,
                    title: parsed.title,
                    subtitle: parsed.start_time || parsed.due_date || "No time specified",
                }],
            };
        }

        return result;
    } catch (error) {
        return {
            success: false,
            error: `Raycast AI error: ${String(error)}`,
        };
    }
}

export default function Command() {
    const [isLoading, setIsLoading] = useState(false);
    const [result, setResult] = useState<CLIResult | null>(null);
    const preferences = getPreferenceValues<Preferences>();
    const canUseRaycastAI = environment.canAccess(AI);

    async function handleSubmit(values: { text: string }) {
        if (!values.text.trim()) {
            showToast({
                style: Toast.Style.Failure,
                title: "Please enter some text",
            });
            return;
        }

        setIsLoading(true);
        setResult(null);

        try {
            let response: CLIResult;

            // Use Raycast AI if available and preferred
            if (preferences.useRaycastAI && canUseRaycastAI) {
                response = await parseWithRaycastAI(values.text);
            } else {
                // Use Python backend
                response = await parseInput(values.text);
            }

            setResult(response);

            if (response.success) {
                showToast({
                    style: Toast.Style.Success,
                    title: response.message || "Success",
                });
            } else {
                showToast({
                    style: Toast.Style.Failure,
                    title: "Failed",
                    message: response.error,
                });
            }
        } catch (error) {
            showToast({
                style: Toast.Style.Failure,
                title: "Error",
                message: String(error),
            });
        } finally {
            setIsLoading(false);
        }
    }

    if (result?.success && result.items && result.items.length > 0) {
        return (
            <List>
                <List.Section title="Created Items">
                    {result.items.map((item, index) => (
                        <List.Item
                            key={index}
                            icon={
                                item.type === "calendar_event"
                                    ? { source: Icon.Calendar, tintColor: Color.Blue }
                                    : { source: Icon.CheckCircle, tintColor: Color.Green }
                            }
                            title={item.title || "Untitled"}
                            subtitle={item.subtitle}
                            accessories={[
                                { text: item.type === "calendar_event" ? "Event" : "Reminder" },
                            ]}
                        />
                    ))}
                </List.Section>
            </List>
        );
    }

    return (
        <Form
            isLoading={isLoading}
            actions={
                <ActionPanel>
                    <Action.SubmitForm title="Create" onSubmit={handleSubmit} />
                </ActionPanel>
            }
        >
            <Form.TextArea
                id="text"
                title="Natural Language Input"
                placeholder="e.g., Meeting tomorrow at 2pm, 明天下午3点开会"
                info={
                    preferences.useRaycastAI && canUseRaycastAI
                        ? "Using Raycast AI"
                        : "Using Python backend"
                }
            />
            {!canUseRaycastAI && (
                <Form.Description
                    title="Note"
                    text="Raycast AI requires Raycast Pro. Using Python backend."
                />
            )}
        </Form>
    );
}
