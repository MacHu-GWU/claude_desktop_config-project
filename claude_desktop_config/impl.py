# -*- coding: utf-8 -*-

import typing as T
import json
import dataclasses
from pathlib import Path

from .os_platform import IS_WINDOWS, IS_MACOS, IS_LINUX


def get_default_claude_desktop_config_path() -> Path:  # pragma: no cover
    """
    See https://modelcontextprotocol.io/quickstart/user

    - macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
    - Windows: %APPDATA%\Claude\claude_desktop_config.json
    """
    if IS_MACOS:
        return (
            Path.home()
            / "Library"
            / "Application Support"
            / "Claude"
            / "claude_desktop_config.json"
        )
    elif IS_WINDOWS:
        import os

        appdata = os.environ.get("APPDATA")
        if appdata:
            return Path(appdata) / "Claude" / "claude_desktop_config.json"
        else:
            # Fallback to typical Windows path if APPDATA is not set
            return (
                Path.home()
                / "AppData"
                / "Roaming"
                / "Claude"
                / "claude_desktop_config.json"
            )
    elif IS_LINUX:  # pragma: no cover
        return Path.home() / ".config" / "Claude" / "claude_desktop_config.json"
    else:  # pragma: no cover
        raise OSError("Unsupported operating system")


@dataclasses.dataclass
class ClaudeDesktopConfig:
    path: Path = dataclasses.field(default=get_default_claude_desktop_config_path())

    def read(self) -> dict[str, T.Any]:
        """
        Read the configuration from the file.
        """
        return json.loads(self.path.read_text(encoding="utf-8"))

    def write(self, config: dict[str, T.Any]):
        """
        Write the configuration to the file.
        """
        self.path.write_text(json.dumps(config, indent=4), encoding="utf-8")

    def put_mcp_server(
        self,
        name: str,
        settings: dict[str, T.Any],
    ):
        """
        Sample config::

            {
                "mcpServers": {
                    "your_mcp_server_name": {
                        "command": "npx",
                        "args": [
                            "-y",
                            "mcp-remote",
                            "https://your-mcp-server.com/sse"
                        ]
                    }
                }
            }
        """
        config = self.read()
        is_changed = False

        if "mcpServers" not in config:
            config["mcpServers"] = {}
            is_changed = True

        if name in config["mcpServers"]:
            existing_settings = config["mcpServers"][name]
            if existing_settings == settings:
                pass
            else:
                config["mcpServers"][name] = settings
                is_changed = True
        else:
            config["mcpServers"][name] = settings
            is_changed = True

        if is_changed:
            self.write(config)

    def del_mcp_server(self, name: str):
        """
        Remove an MCP server from the configuration.
        This is an idempotent operation - no error if the server doesn't exist.
        """
        config = self.read()
        is_changed = False
        
        if "mcpServers" in config and name in config["mcpServers"]:
            del config["mcpServers"][name]
            is_changed = True
            
            # Remove empty mcpServers key to keep config clean
            if not config["mcpServers"]:
                del config["mcpServers"]
        
        if is_changed:
            self.write(config)
