# -*- coding: utf-8 -*-

import json
from pathlib import Path
import pytest
from claude_desktop_config.impl import (
    ClaudeDesktopConfig,
    Mcp,
    BaseMcpEnum,
    enable_mcp_server,
    disable_mcp_server,
    get_default_claude_desktop_config_path,
)
from claude_desktop_config.os_platform import IS_WINDOWS, IS_MACOS, IS_LINUX


path_test_claude_desktop_config_json = (
    Path(__file__).absolute().parent / "claude_desktop_config.json"
)


def reset_config():
    config = {}
    path_test_claude_desktop_config_json.write_text(json.dumps(config, indent=4))


class McpEnum(BaseMcpEnum):
    mcp_1 = Mcp(
        name="mcp_1",
        settings={
            "command": "npx",
            "args": ["-y", "mcp-remote", "https://mcp1.example.com/sse"],
        },
    )
    mcp_2 = Mcp(
        name="mcp_2",
        settings={
            "command": "npx",
            "args": ["-y", "mcp-remote", "https://mcp2.example.com/sse"],
        },
    )
    mcp_3 = Mcp(
        name="mcp_3",
        settings={
            "command": "npx",
            "args": ["-y", "mcp-remote", "https://mcp3.example.com/sse"],
        },
    )


class TestEnableMcpServer:
    def test_enable_new_server_no_mcpservers_key(self):
        """Test enabling a server when mcpServers key doesn't exist"""
        config = {}
        result = enable_mcp_server(
            config,
            name="test_server",
            settings={"command": "test", "args": ["arg1"]},
        )
        assert result is True
        assert config == {
            "mcpServers": {"test_server": {"command": "test", "args": ["arg1"]}}
        }

    def test_enable_new_server_with_existing_mcpservers(self):
        """Test enabling a server when mcpServers key exists with other servers"""
        config = {
            "mcpServers": {"existing_server": {"command": "existing", "args": ["arg"]}}
        }
        result = enable_mcp_server(
            config,
            name="new_server",
            settings={"command": "new", "args": ["newarg"]},
        )
        assert result is True
        assert config == {
            "mcpServers": {
                "existing_server": {"command": "existing", "args": ["arg"]},
                "new_server": {"command": "new", "args": ["newarg"]},
            }
        }

    def test_enable_existing_server_same_settings(self):
        """Test enabling a server that already exists with same settings (idempotent)"""
        config = {"mcpServers": {"test_server": {"command": "test", "args": ["arg1"]}}}
        result = enable_mcp_server(
            config,
            name="test_server",
            settings={"command": "test", "args": ["arg1"]},
        )
        assert result is False
        assert config == {
            "mcpServers": {"test_server": {"command": "test", "args": ["arg1"]}}
        }

    def test_enable_existing_server_different_settings(self):
        """Test enabling a server that already exists with different settings"""
        config = {"mcpServers": {"test_server": {"command": "old", "args": ["oldarg"]}}}
        result = enable_mcp_server(
            config,
            name="test_server",
            settings={"command": "new", "args": ["newarg"]},
        )
        assert result is True
        assert config == {
            "mcpServers": {"test_server": {"command": "new", "args": ["newarg"]}}
        }


class TestDisableMcpServer:
    def test_disable_existing_server(self):
        """Test disabling a server that exists"""
        config = {
            "mcpServers": {
                "server_to_remove": {"command": "test", "args": ["arg"]},
                "server_to_keep": {"command": "keep", "args": ["keeparg"]},
            }
        }
        result = disable_mcp_server(config, "server_to_remove")
        assert result is True
        assert config == {
            "mcpServers": {"server_to_keep": {"command": "keep", "args": ["keeparg"]}}
        }

    def test_disable_non_existent_server(self):
        """Test disabling a server that doesn't exist (idempotent)"""
        config = {
            "mcpServers": {"existing_server": {"command": "test", "args": ["arg"]}}
        }
        result = disable_mcp_server(config, "non_existent")
        assert result is False
        assert config == {
            "mcpServers": {"existing_server": {"command": "test", "args": ["arg"]}}
        }

    def test_disable_server_no_mcpservers_key(self):
        """Test disabling a server when mcpServers key doesn't exist"""
        config = {"otherKey": "value"}
        result = disable_mcp_server(config, "any_server")
        assert result is False
        assert config == {"otherKey": "value"}


class TestClaudeDesktopConfig:
    def test_read_config(self):
        """Test reading configuration from file"""
        reset_config()
        test_config = {"mcpServers": {"test": {"command": "test"}}}
        path_test_claude_desktop_config_json.write_text(
            json.dumps(test_config, indent=4)
        )

        cdc = ClaudeDesktopConfig(path=path_test_claude_desktop_config_json)
        config = cdc.read()
        assert config == test_config

    def test_write_config(self):
        """Test writing configuration to file"""
        reset_config()
        cdc = ClaudeDesktopConfig(path=path_test_claude_desktop_config_json)

        test_config = {"mcpServers": {"new_server": {"command": "new"}}}
        cdc.write(test_config)

        # Read the file directly to verify
        written_config = json.loads(path_test_claude_desktop_config_json.read_text())
        assert written_config == test_config

    def test_default_path_initialization(self):
        """Test that ClaudeDesktopConfig uses default path when not specified"""
        cdc = ClaudeDesktopConfig()
        assert cdc.path == get_default_claude_desktop_config_path()


class TestMcpDataclass:
    def test_mcp_creation(self):
        """Test Mcp dataclass creation"""
        mcp = Mcp(
            name="test_mcp", settings={"command": "test", "args": ["arg1", "arg2"]}
        )
        assert mcp.name == "test_mcp"
        assert mcp.settings == {"command": "test", "args": ["arg1", "arg2"]}


class TestBaseMcpEnum:
    def test_apply_enable_all_mcps(self):
        """Test applying all MCPs from enum"""
        reset_config()
        cdc = ClaudeDesktopConfig(path=path_test_claude_desktop_config_json)

        # Enable all MCPs
        wanted_mcps = [McpEnum.mcp_1, McpEnum.mcp_2, McpEnum.mcp_3]
        result = McpEnum.apply(wanted_mcps, cdc)

        assert result is True
        config = cdc.read()
        assert "mcpServers" in config
        assert "mcp_1" in config["mcpServers"]
        assert "mcp_2" in config["mcpServers"]
        assert "mcp_3" in config["mcpServers"]

    def test_apply_enable_subset_of_mcps(self):
        """Test applying only a subset of MCPs"""
        reset_config()
        cdc = ClaudeDesktopConfig(path=path_test_claude_desktop_config_json)

        # First enable all MCPs
        wanted_mcps = [McpEnum.mcp_1, McpEnum.mcp_2, McpEnum.mcp_3]
        McpEnum.apply(wanted_mcps, cdc)

        # Now enable only mcp_1 and mcp_3 (should disable mcp_2)
        wanted_mcps = [McpEnum.mcp_1, McpEnum.mcp_3]
        result = McpEnum.apply(wanted_mcps, cdc)

        assert result is True
        config = cdc.read()
        assert "mcp_1" in config["mcpServers"]
        assert "mcp_2" not in config["mcpServers"]
        assert "mcp_3" in config["mcpServers"]

    def test_apply_disable_all_mcps(self):
        """Test disabling all MCPs"""
        reset_config()
        cdc = ClaudeDesktopConfig(path=path_test_claude_desktop_config_json)

        # First enable all MCPs
        wanted_mcps = [McpEnum.mcp_1, McpEnum.mcp_2, McpEnum.mcp_3]
        McpEnum.apply(wanted_mcps, cdc)

        # Now disable all MCPs
        wanted_mcps = []
        result = McpEnum.apply(wanted_mcps, cdc)

        assert result is True
        config = cdc.read()
        assert "mcpServers" in config
        assert len(config["mcpServers"]) == 0

    def test_apply_no_changes_needed(self):
        """Test apply when no changes are needed"""
        reset_config()
        cdc = ClaudeDesktopConfig(path=path_test_claude_desktop_config_json)

        # Enable mcp_1 and mcp_2
        wanted_mcps = [McpEnum.mcp_1, McpEnum.mcp_2]
        McpEnum.apply(wanted_mcps, cdc)

        # Apply same configuration again
        result = McpEnum.apply(wanted_mcps, cdc)

        assert result is False

    def test_apply_with_set_input(self):
        """Test apply with set instead of list"""
        reset_config()
        cdc = ClaudeDesktopConfig(path=path_test_claude_desktop_config_json)

        # Use set instead of list
        wanted_mcps = {McpEnum.mcp_1, McpEnum.mcp_3}
        result = McpEnum.apply(wanted_mcps, cdc)

        assert result is True
        config = cdc.read()
        assert "mcp_1" in config["mcpServers"]
        assert "mcp_2" not in config["mcpServers"]
        assert "mcp_3" in config["mcpServers"]


# Clean up test file after tests
def teardown_module():
    if path_test_claude_desktop_config_json.exists():
        path_test_claude_desktop_config_json.unlink()


if __name__ == "__main__":
    from claude_desktop_config.tests import run_cov_test

    run_cov_test(
        __file__,
        "claude_desktop_config.impl",
        preview=False,
    )
