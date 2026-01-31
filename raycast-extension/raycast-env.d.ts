/// <reference types="@raycast/api">

/* 🚧 🚧 🚧
 * This file is auto-generated from the extension's manifest.
 * Do not modify manually. Instead, update the `package.json` file.
 * 🚧 🚧 🚧 */

/* eslint-disable @typescript-eslint/ban-types */

type ExtensionPreferences = {
  /** Use Raycast AI - Use Raycast's built-in AI instead of Python backend (requires Raycast Pro) */
  "useRaycastAI": boolean,
  /** Python Path - Path to Python 3.11+ executable */
  "pythonPath": string,
  /** Project Path - Path to reminder-alf project directory */
  "projectPath"?: string
}

/** Preferences accessible in all the extension's commands */
declare type Preferences = ExtensionPreferences

declare namespace Preferences {
  /** Preferences accessible in the `create-item` command */
  export type CreateItem = ExtensionPreferences & {}
  /** Preferences accessible in the `list-items` command */
  export type ListItems = ExtensionPreferences & {}
  /** Preferences accessible in the `config-status` command */
  export type ConfigStatus = ExtensionPreferences & {}
}

declare namespace Arguments {
  /** Arguments passed to the `create-item` command */
  export type CreateItem = {}
  /** Arguments passed to the `list-items` command */
  export type ListItems = {}
  /** Arguments passed to the `config-status` command */
  export type ConfigStatus = {}
}

