
.. image:: https://readthedocs.org/projects/claude-desktop-config/badge/?version=latest
    :target: https://claude-desktop-config.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/claude_desktop_config-project/actions/workflows/main.yml/badge.svg
    :target: https://github.com/MacHu-GWU/claude_desktop_config-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/claude_desktop_config-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/claude_desktop_config-project

.. image:: https://img.shields.io/pypi/v/claude-desktop-config.svg
    :target: https://pypi.python.org/pypi/claude-desktop-config

.. image:: https://img.shields.io/pypi/l/claude-desktop-config.svg
    :target: https://pypi.python.org/pypi/claude-desktop-config

.. image:: https://img.shields.io/pypi/pyversions/claude-desktop-config.svg
    :target: https://pypi.python.org/pypi/claude-desktop-config

.. image:: https://img.shields.io/badge/✍️_Release_History!--None.svg?style=social&logo=github
    :target: https://github.com/MacHu-GWU/claude_desktop_config-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/⭐_Star_me_on_GitHub!--None.svg?style=social&logo=github
    :target: https://github.com/MacHu-GWU/claude_desktop_config-project

------

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://claude-desktop-config.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/claude_desktop_config-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/claude_desktop_config-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/claude_desktop_config-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/claude-desktop-config#files


Welcome to ``claude_desktop_config`` Documentation
==============================================================================
.. image:: https://claude-desktop-config.readthedocs.io/en/latest/_static/claude_desktop_config-logo.png
    :target: https://claude-desktop-config.readthedocs.io/en/latest/

``claude_desktop_config`` is a Python library for programmatically managing Claude Desktop's MCP (Model Context Protocol) server configurations. It provides a simple, Pythonic interface to add, update, and remove MCP servers in the ``claude_desktop_config.json`` file without manually editing JSON. The library handles platform-specific configuration paths automatically and ensures safe, atomic updates to maintain configuration integrity.


Usage Examples
------------------------------------------------------------------------------
**Functional API - Add or Update an MCP Server**

.. code-block:: python

    from claude_desktop_config.api import ClaudeDesktopConfig, enable_mcp_server

    # Create config instance (auto-detects platform-specific path)
    cdc = ClaudeDesktopConfig()
    
    # Read current configuration
    config = cdc.read()
    
    # Add or update an MCP server
    changed = enable_mcp_server(
        config,
        name="my-knowledge-base",
        settings={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-memory"]
        }
    )
    
    # Write back if changed
    if changed:
        cdc.write(config)

**Functional API - Remove an MCP Server**

.. code-block:: python

    from claude_desktop_config.api import ClaudeDesktopConfig, disable_mcp_server

    cdc = ClaudeDesktopConfig()
    config = cdc.read()
    
    # Remove a server (idempotent - no error if doesn't exist)
    if disable_mcp_server(config, "my-knowledge-base"):
        cdc.write(config)

**Enum API - Declarative Server Management**

.. code-block:: python

    from claude_desktop_config.api import ClaudeDesktopConfig, BaseMcpEnum, Mcp
    
    # Define your MCP servers as an enum
    class MyMcpServers(BaseMcpEnum):
        filesystem = Mcp(
            name="filesystem",
            settings={
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/documents"]
            }
        )
        github = Mcp(
            name="github", 
            settings={
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"]
            }
        )
        memory = Mcp(
            name="memory",
            settings={
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-memory"]
            }
        )
    
    # Apply desired state - this will:
    # 1. Enable filesystem and github servers
    # 2. Disable memory server (if it exists)
    cdc = ClaudeDesktopConfig()
    MyMcpServers.apply([MyMcpServers.filesystem, MyMcpServers.github], cdc)

**Work with Custom Config Path**

.. code-block:: python

    from pathlib import Path

    # Use a custom configuration file path
    cdc = ClaudeDesktopConfig(path=Path("/custom/path/config.json"))

    # Read current configuration
    current_config = cdc.read()
    print(current_config)

**Batch Operations with Functional API**

.. code-block:: python

    from claude_desktop_config.api import ClaudeDesktopConfig, enable_mcp_server, disable_mcp_server

    cdc = ClaudeDesktopConfig()
    config = cdc.read()
    
    # Track if any changes were made
    changed = False
    
    # Add multiple MCP servers
    servers = {
        "filesystem": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/documents"]
        },
        "github": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"]
        }
    }
    
    for name, settings in servers.items():
        changed |= enable_mcp_server(config, name, settings)
    
    # Remove unwanted servers
    for name in ["old-server", "deprecated-server"]:
        changed |= disable_mcp_server(config, name)
    
    # Write once if any changes were made
    if changed:
        cdc.write(config)


.. _install:

Install
------------------------------------------------------------------------------

``claude_desktop_config`` is released on PyPI, so all you need is to:

.. code-block:: console

    $ pip install claude-desktop-config

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade claude-desktop-config
