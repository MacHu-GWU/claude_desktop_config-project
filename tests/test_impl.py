# -*- coding: utf-8 -*-

import json
from pathlib import Path
from claude_desktop_config.impl import ClaudeDesktopConfig, Mcp, BaseMcpEnum


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


class TestClaudeDesktopConfig:
    def test(self):
        reset_config()
        cdc = ClaudeDesktopConfig(path=path_test_claude_desktop_config_json)
        wanted_mcps = [
            McpEnum.mcp_1,
            McpEnum.mcp_2,
            McpEnum.mcp_3,
        ]
        McpEnum.apply(wanted_mcps, cdc)

    # def test_put_mcp_server(self):
    #     cdc = ClaudeDesktopConfig(path=path)
    #
    #     # Test 1: Add server when mcpServers doesn't exist
    #     cdc.write({})
    #     cdc.put_mcp_server(
    #         name="my_mcp_server",
    #         settings={
    #             "command": "npx",
    #             "args": ["-y", "mcp-remote", "https://my-mcp-server.com/sse"],
    #         },
    #     )
    #     config = cdc.read()
    #     assert config == {
    #         "mcpServers": {
    #             "my_mcp_server": {
    #                 "command": "npx",
    #                 "args": ["-y", "mcp-remote", "https://my-mcp-server.com/sse"],
    #             }
    #         }
    #     }
    #
    #     # Test 2: Add server when mcpServers already exists
    #     cdc.write({"mcpServers": {}})
    #     cdc.put_mcp_server(
    #         name="another_server",
    #         settings={
    #             "command": "node",
    #             "args": ["server.js"],
    #         },
    #     )
    #     config = cdc.read()
    #     assert config == {
    #         "mcpServers": {
    #             "another_server": {
    #                 "command": "node",
    #                 "args": ["server.js"],
    #             }
    #         }
    #     }
    #
    #     # Test 3: Update existing server with different settings
    #     cdc.write(
    #         {
    #             "mcpServers": {
    #                 "existing_server": {
    #                     "command": "old_command",
    #                     "args": ["old_arg"],
    #                 }
    #             }
    #         }
    #     )
    #     cdc.put_mcp_server(
    #         name="existing_server",
    #         settings={
    #             "command": "new_command",
    #             "args": ["new_arg"],
    #         },
    #     )
    #     config = cdc.read()
    #     assert config == {
    #         "mcpServers": {
    #             "existing_server": {
    #                 "command": "new_command",
    #                 "args": ["new_arg"],
    #             }
    #         }
    #     }
    #
    #     # Test 4: No change when settings are identical
    #     initial_config = {
    #         "mcpServers": {
    #             "unchanged_server": {
    #                 "command": "same_command",
    #                 "args": ["same_arg"],
    #             }
    #         }
    #     }
    #     cdc.write(initial_config)
    #
    #     # Read file before put_mcp_server to track if write was called
    #     original_content = path.read_text()
    #
    #     cdc.put_mcp_server(
    #         name="unchanged_server",
    #         settings={
    #             "command": "same_command",
    #             "args": ["same_arg"],
    #         },
    #     )
    #
    #     # Verify file wasn't written (content unchanged)
    #     new_content = path.read_text()
    #     assert original_content == new_content
    #
    #     # Verify config is still the same
    #     config = cdc.read()
    #     assert config == initial_config
    #
    # def test_del_mcp_server(self):
    #     cdc = ClaudeDesktopConfig(path=path)
    #
    #     # Test 1: Delete server when it exists
    #     cdc.write(
    #         {
    #             "mcpServers": {
    #                 "server_to_delete": {
    #                     "command": "npx",
    #                     "args": ["server"],
    #                 },
    #                 "server_to_keep": {
    #                     "command": "node",
    #                     "args": ["app.js"],
    #                 },
    #             }
    #         }
    #     )
    #     cdc.del_mcp_server("server_to_delete")
    #     config = cdc.read()
    #     assert config == {
    #         "mcpServers": {
    #             "server_to_keep": {
    #                 "command": "node",
    #                 "args": ["app.js"],
    #             }
    #         }
    #     }
    #
    #     # Test 2: Delete last server (should remove mcpServers key)
    #     cdc.write(
    #         {
    #             "mcpServers": {
    #                 "last_server": {
    #                     "command": "python",
    #                     "args": ["server.py"],
    #                 }
    #             },
    #             "otherConfig": "value",
    #         }
    #     )
    #     cdc.del_mcp_server("last_server")
    #     config = cdc.read()
    #     assert config == {"otherConfig": "value"}
    #     assert "mcpServers" not in config
    #
    #     # Test 3: Delete non-existent server (idempotent - no error)
    #     initial_config = {
    #         "mcpServers": {
    #             "existing_server": {
    #                 "command": "npm",
    #                 "args": ["start"],
    #             }
    #         }
    #     }
    #     cdc.write(initial_config)
    #     original_content = path.read_text()
    #
    #     cdc.del_mcp_server("non_existent_server")
    #
    #     # Verify file wasn't written
    #     new_content = path.read_text()
    #     assert original_content == new_content
    #
    #     # Verify config unchanged
    #     config = cdc.read()
    #     assert config == initial_config
    #
    #     # Test 4: Delete when mcpServers doesn't exist (idempotent)
    #     cdc.write({"otherConfig": "value"})
    #     original_content = path.read_text()
    #
    #     cdc.del_mcp_server("any_server")
    #
    #     # Verify file wasn't written
    #     new_content = path.read_text()
    #     assert original_content == new_content
    #
    #     # Verify config unchanged
    #     config = cdc.read()
    #     assert config == {"otherConfig": "value"}


if __name__ == "__main__":
    from claude_desktop_config.tests import run_cov_test

    run_cov_test(
        __file__,
        "claude_desktop_config.impl",
        preview=False,
    )
