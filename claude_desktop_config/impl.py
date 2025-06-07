# -*- coding: utf-8 -*-

import typing as T
import json
import enum
import dataclasses
from pathlib import Path

from .os_platform import IS_WINDOWS, IS_MACOS, IS_LINUX


@dataclasses.dataclass
class Mcp:
    """
    Represents a Model Context Protocol (MCP) server configuration.

    :param name: The name of the MCP server.
    :param settings: The settings for the MCP server, typically including command and arguments.
    """

    name: str = dataclasses.field()
    settings: dict[str, T.Any] = dataclasses.field()


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


def enable_mcp_server(
    config: dict[str, T.Any],
    name: str,
    settings: dict[str, T.Any],
) -> bool:
    """
    Enable an MCP server by setting its configuration in the provided dictionary.

    This is an idempotent operation - no error if the server already exists with the same settings.

    :param config: The configuration dictionary to modify.
    :param name: The name of the MCP server.
    :param settings: The settings for the MCP server.

    :return: True if the configuration was changed, False if it was unchanged.
    """
    if "mcpServers" not in config:
        config["mcpServers"] = {
            name: settings,
        }
        return True

    if name in config["mcpServers"]:
        existing_settings = config["mcpServers"][name]
        if existing_settings == settings:
            return False
        else:
            config["mcpServers"][name] = settings
            return True
    else:
        config["mcpServers"][name] = settings
        return True


def disable_mcp_server(
    config: dict[str, T.Any],
    name: str,
) -> bool:
    """
    Remove an MCP server by deleting its entry from the provided configuration dictionary.

    This is an idempotent operation - no error if the server doesn't exist.

    :param config: The configuration dictionary to modify.
    :param name: The name of the MCP server to remove.

    :return: True if the configuration was changed, False if it was unchanged.
    """
    if "mcpServers" in config and name in config["mcpServers"]:
        del config["mcpServers"][name]
        return True
    return False


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


@dataclasses.dataclass
class Mcp:
    name: str = dataclasses.field()
    settings: dict[str, T.Any] = dataclasses.field()


class BaseMcpEnum(enum.Enum):
    @classmethod
    def apply(
        cls,
        wanted_mcps: T.Union[set["BaseMcpEnum"], list["BaseMcpEnum"]],
        cdc: ClaudeDesktopConfig,
    ) -> bool:
        """
        Apply the MCP configuration to the Claude Desktop Config.

        This method should be overridden by subclasses to define Mcp Enumerations.

        :param wanted_mcps: A set of MCPs that should be enabled.
        :param cdc: An instance of ClaudeDesktopConfig to read and write the configuration.

        :return: True if the configuration was changed, False if it was unchanged.
        """
        config = cdc.read()
        flag_list = list()
        for mcp_enum in cls:
            if mcp_enum in wanted_mcps:
                flag = enable_mcp_server(
                    config,
                    name=mcp_enum.value.name,
                    settings=mcp_enum.value.settings,
                )
            else:
                flag = disable_mcp_server(
                    config,
                    name=mcp_enum.value.name,
                )

            flag_list.append(flag)

        if any(flag_list):
            cdc.write(config)
            return True
        return False
