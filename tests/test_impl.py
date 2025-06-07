# -*- coding: utf-8 -*-

from pathlib import Path
from claude_desktop_config.impl import ClaudeDesktopConfig

path = Path(__file__).absolute().parent / "claude_desktop_config.json"


class TestClaudeDesktopConfig:
    def test_put_mcp_server(self):
        cdc = ClaudeDesktopConfig(path=path)
        
        # Test 1: Add server when mcpServers doesn't exist
        cdc.write({})
        cdc.put_mcp_server(
            name="my_mcp_server",
            settings={
                "command": "npx",
                "args": ["-y", "mcp-remote", "https://my-mcp-server.com/sse"],
            },
        )
        config = cdc.read()
        assert config == {
            "mcpServers": {
                "my_mcp_server": {
                    "command": "npx",
                    "args": ["-y", "mcp-remote", "https://my-mcp-server.com/sse"],
                }
            }
        }
        
        # Test 2: Add server when mcpServers already exists
        cdc.write({"mcpServers": {}})
        cdc.put_mcp_server(
            name="another_server",
            settings={
                "command": "node",
                "args": ["server.js"],
            },
        )
        config = cdc.read()
        assert config == {
            "mcpServers": {
                "another_server": {
                    "command": "node",
                    "args": ["server.js"],
                }
            }
        }
        
        # Test 3: Update existing server with different settings
        cdc.write({
            "mcpServers": {
                "existing_server": {
                    "command": "old_command",
                    "args": ["old_arg"],
                }
            }
        })
        cdc.put_mcp_server(
            name="existing_server",
            settings={
                "command": "new_command",
                "args": ["new_arg"],
            },
        )
        config = cdc.read()
        assert config == {
            "mcpServers": {
                "existing_server": {
                    "command": "new_command",
                    "args": ["new_arg"],
                }
            }
        }
        
        # Test 4: No change when settings are identical
        initial_config = {
            "mcpServers": {
                "unchanged_server": {
                    "command": "same_command",
                    "args": ["same_arg"],
                }
            }
        }
        cdc.write(initial_config)
        
        # Read file before put_mcp_server to track if write was called
        original_content = path.read_text()
        
        cdc.put_mcp_server(
            name="unchanged_server",
            settings={
                "command": "same_command",
                "args": ["same_arg"],
            },
        )
        
        # Verify file wasn't written (content unchanged)
        new_content = path.read_text()
        assert original_content == new_content
        
        # Verify config is still the same
        config = cdc.read()
        assert config == initial_config


if __name__ == "__main__":
    from claude_desktop_config.tests import run_cov_test

    run_cov_test(
        __file__,
        "claude_desktop_config.impl",
        preview=True,
    )
