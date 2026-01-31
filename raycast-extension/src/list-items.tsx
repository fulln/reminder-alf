import { List, Icon, Color, ActionPanel, Action, showToast, Toast } from "@raycast/api";
import { useEffect, useState } from "react";
import { listItems, deleteItem, CLIResult } from "./python-bridge";

interface TrackedItem {
    id?: string;
    type?: string;
    title?: string;
    created_at?: string;
}

export default function Command() {
    const [isLoading, setIsLoading] = useState(true);
    const [items, setItems] = useState<TrackedItem[]>([]);
    const [error, setError] = useState<string | null>(null);

    async function fetchItems() {
        setIsLoading(true);
        try {
            const result = await listItems(20);
            if (result.success && result.items) {
                setItems(result.items);
                setError(null);
            } else {
                setError(result.error || "Failed to fetch items");
            }
        } catch (e) {
            setError(String(e));
        } finally {
            setIsLoading(false);
        }
    }

    useEffect(() => {
        fetchItems();
    }, []);

    async function handleDelete(itemId: string) {
        try {
            const result = await deleteItem(itemId);
            if (result.success) {
                showToast({
                    style: Toast.Style.Success,
                    title: "Item deleted",
                });
                fetchItems(); // Refresh list
            } else {
                showToast({
                    style: Toast.Style.Failure,
                    title: "Delete failed",
                    message: result.error,
                });
            }
        } catch (e) {
            showToast({
                style: Toast.Style.Failure,
                title: "Error",
                message: String(e),
            });
        }
    }

    if (error) {
        return (
            <List>
                <List.EmptyView
                    icon={Icon.ExclamationMark}
                    title="Error"
                    description={error}
                />
            </List>
        );
    }

    if (items.length === 0 && !isLoading) {
        return (
            <List>
                <List.EmptyView
                    icon={Icon.Calendar}
                    title="No Items"
                    description="No tracked events or reminders found"
                />
            </List>
        );
    }

    return (
        <List isLoading={isLoading}>
            <List.Section title="Recent Items">
                {items.map((item, index) => (
                    <List.Item
                        key={item.id || index}
                        icon={
                            item.type === "calendar_event"
                                ? { source: Icon.Calendar, tintColor: Color.Blue }
                                : { source: Icon.CheckCircle, tintColor: Color.Green }
                        }
                        title={item.title || "Untitled"}
                        subtitle={item.created_at ? new Date(item.created_at).toLocaleDateString() : ""}
                        accessories={[
                            { text: item.type === "calendar_event" ? "Event" : "Reminder" },
                        ]}
                        actions={
                            item.id ? (
                                <ActionPanel>
                                    <Action
                                        title="Delete"
                                        icon={Icon.Trash}
                                        style={Action.Style.Destructive}
                                        onAction={() => handleDelete(item.id!)}
                                    />
                                    <Action
                                        title="Refresh"
                                        icon={Icon.ArrowClockwise}
                                        onAction={fetchItems}
                                    />
                                </ActionPanel>
                            ) : undefined
                        }
                    />
                ))}
            </List.Section>
        </List>
    );
}
