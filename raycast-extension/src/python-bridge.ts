/**
 * Python CLI bridge for Reminder-Alf
 * Executes Python CLI commands and returns parsed JSON results
 */
import { exec } from "child_process";
import { promisify } from "util";

const execAsync = promisify(exec);

export interface CLIResult {
    success: boolean;
    message?: string;
    error?: string;
    items?: Array<{
        id?: string;
        type?: string;
        title?: string;
        subtitle?: string;
        created_at?: string;
    }>;
    config?: {
        provider?: string;
        model?: string;
        endpoint?: string;
    };
    errors?: string[];
}

import { getPreferenceValues } from "@raycast/api";

interface Preferences {
    pythonPath?: string;
    projectPath?: string;
}

/**
 * Get the Python executable path
 */
function getPythonPath(): string {
    const preferences = getPreferenceValues<Preferences>();
    return preferences.pythonPath || "python3.11";
}

/**
 * Get the project root path
 */
function getProjectPath(): string {
    const preferences = getPreferenceValues<Preferences>();
    return preferences.projectPath || `${process.env.HOME}/opensource/python/reminder-alf`;
}

/**
 * Execute a CLI command and return parsed result
 */
export async function executeCommand(args: string[]): Promise<CLIResult> {
    const pythonPath = getPythonPath();
    const projectPath = getProjectPath();

    // Note: --json must come before subcommands
    const command = `cd "${projectPath}" && ${pythonPath} -m src.cli --json ${args.map(a => `"${a}"`).join(" ")}`;

    try {
        const { stdout, stderr } = await execAsync(command, {
            timeout: 60000, // 60 second timeout
            maxBuffer: 1024 * 1024, // 1MB buffer
        });

        if (stderr && !stdout) {
            return {
                success: false,
                error: stderr.trim(),
            };
        }

        try {
            return JSON.parse(stdout.trim());
        } catch {
            return {
                success: true,
                message: stdout.trim(),
            };
        }
    } catch (error) {
        const err = error as { message?: string; stderr?: string };
        return {
            success: false,
            error: err.message || err.stderr || "Command execution failed",
        };
    }
}

/**
 * Parse natural language input
 */
export async function parseInput(text: string): Promise<CLIResult> {
    return executeCommand(["parse", text]);
}

/**
 * Get configuration status
 */
export async function getConfigStatus(): Promise<CLIResult> {
    return executeCommand(["config", "status"]);
}

/**
 * List recent items
 */
export async function listItems(count: number = 10): Promise<CLIResult> {
    return executeCommand(["list", count.toString()]);
}

/**
 * Delete an item
 */
export async function deleteItem(itemId: string): Promise<CLIResult> {
    return executeCommand(["delete", itemId]);
}

/**
 * Set configuration
 */
export async function setConfig(
    provider: string,
    apiKey: string,
    model?: string
): Promise<CLIResult> {
    const args = ["config", "set", provider, apiKey];
    if (model) {
        args.push(model);
    }
    return executeCommand(args);
}
