import {
    List,
    Icon,
    Color,
    ActionPanel,
    Action,
    Form,
    showToast,
    Toast,
    useNavigation,
} from "@raycast/api";
import { useEffect, useState } from "react";
import { getConfigStatus, setConfig, CLIResult } from "./python-bridge";

export default function Command() {
    const [isLoading, setIsLoading] = useState(true);
    const [config, setConfigState] = useState<CLIResult["config"] | null>(null);
    const [error, setError] = useState<string | null>(null);
    const { push } = useNavigation();

    async function fetchConfig() {
        setIsLoading(true);
        try {
            const result = await getConfigStatus();
            if (result.success && result.config) {
                setConfigState(result.config);
                setError(null);
            } else {
                setError(result.error || "Not configured");
                setConfigState(null);
            }
        } catch (e) {
            setError(String(e));
        } finally {
            setIsLoading(false);
        }
    }

    useEffect(() => {
        fetchConfig();
    }, []);

    if (error || !config) {
        return (
            <List isLoading={isLoading}>
                <List.EmptyView
                    icon={Icon.Gear}
                    title="Not Configured"
                    description={error || "AI provider not configured yet"}
                    actions={
                        <ActionPanel>
                            <Action
                                title="Configure"
                                icon={Icon.Gear}
                                onAction={() => push(<ConfigForm onSuccess={fetchConfig} />)}
                            />
                        </ActionPanel>
                    }
                />
            </List>
        );
    }

    return (
        <List isLoading={isLoading}>
            <List.Section title="AI Configuration">
                <List.Item
                    icon={{ source: Icon.Globe, tintColor: Color.Blue }}
                    title="Provider"
                    accessories={[{ text: config.provider || "Unknown" }]}
                />
                <List.Item
                    icon={{ source: Icon.LightBulb, tintColor: Color.Yellow }}
                    title="Model"
                    accessories={[{ text: config.model || "Unknown" }]}
                />
                {config.endpoint && (
                    <List.Item
                        icon={{ source: Icon.Link, tintColor: Color.Green }}
                        title="Endpoint"
                        accessories={[{ text: config.endpoint }]}
                    />
                )}
            </List.Section>
            <List.Section title="Actions">
                <List.Item
                    icon={Icon.Gear}
                    title="Update Configuration"
                    actions={
                        <ActionPanel>
                            <Action
                                title="Configure"
                                icon={Icon.Gear}
                                onAction={() => push(<ConfigForm onSuccess={fetchConfig} />)}
                            />
                        </ActionPanel>
                    }
                />
            </List.Section>
        </List>
    );
}

function ConfigForm({ onSuccess }: { onSuccess: () => void }) {
    const [isLoading, setIsLoading] = useState(false);
    const { pop } = useNavigation();

    async function handleSubmit(values: {
        provider: string;
        apiKey: string;
        model?: string;
    }) {
        if (!values.provider || !values.apiKey) {
            showToast({
                style: Toast.Style.Failure,
                title: "Provider and API Key are required",
            });
            return;
        }

        setIsLoading(true);
        try {
            const result = await setConfig(values.provider, values.apiKey, values.model);
            if (result.success) {
                showToast({
                    style: Toast.Style.Success,
                    title: "Configuration saved",
                });
                onSuccess();
                pop();
            } else {
                showToast({
                    style: Toast.Style.Failure,
                    title: "Failed to save",
                    message: result.error,
                });
            }
        } catch (e) {
            showToast({
                style: Toast.Style.Failure,
                title: "Error",
                message: String(e),
            });
        } finally {
            setIsLoading(false);
        }
    }

    return (
        <Form
            isLoading={isLoading}
            actions={
                <ActionPanel>
                    <Action.SubmitForm title="Save Configuration" onSubmit={handleSubmit} />
                </ActionPanel>
            }
        >
            <Form.Dropdown id="provider" title="AI Provider">
                <Form.Dropdown.Item value="openai" title="OpenAI" />
                <Form.Dropdown.Item value="deepseek" title="DeepSeek" />
                <Form.Dropdown.Item value="anthropic" title="Anthropic" />
                <Form.Dropdown.Item value="custom" title="Custom" />
            </Form.Dropdown>
            <Form.PasswordField
                id="apiKey"
                title="API Key"
                placeholder="sk-..."
            />
            <Form.TextField
                id="model"
                title="Model (Optional)"
                placeholder="e.g., gpt-4-turbo, deepseek-chat"
                info="Leave empty to use default model"
            />
        </Form>
    );
}
