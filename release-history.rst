.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.2.1 (2025-06-07)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add new functional API for managing MCP servers:
    - ``enable_mcp_server(config, name, settings)``: Enable/update an MCP server in a config dictionary
    - ``disable_mcp_server(config, name)``: Remove an MCP server from a config dictionary
- Add ``BaseMcpEnum`` class for declarative MCP server management:
    - Define all MCP servers as enum values
    - Apply desired state with ``BaseMcpEnum.apply(wanted_mcps, cdc)``
    - Automatically enables/disables servers based on the wanted list
- Add ``Mcp`` dataclass for structured MCP server definitions

**Breaking Changes**

- **REMOVED**: ``ClaudeDesktopConfig.put_mcp_server()`` method - use ``enable_mcp_server()`` instead
- **REMOVED**: ``ClaudeDesktopConfig.del_mcp_server()`` method - use ``disable_mcp_server()`` instead
- The new API separates configuration manipulation (enable/disable functions) from file I/O (ClaudeDesktopConfig read/write)

**Migration Guide**

Old API:
.. code-block:: python

    config = ClaudeDesktopConfig()
    config.put_mcp_server("my-server", {"command": "cmd"})
    config.del_mcp_server("my-server")

New API (functional approach):
.. code-block:: python

    from claude_desktop_config.api import ClaudeDesktopConfig, enable_mcp_server, disable_mcp_server
    
    cdc = ClaudeDesktopConfig()
    config = cdc.read()
    
    # Enable/update a server
    if enable_mcp_server(config, "my-server", {"command": "cmd"}):
        cdc.write(config)
    
    # Disable a server
    if disable_mcp_server(config, "my-server"):
        cdc.write(config)

New API (enum approach):
.. code-block:: python

    from claude_desktop_config.api import ClaudeDesktopConfig, BaseMcpEnum, Mcp
    
    class MyMcpServers(BaseMcpEnum):
        server1 = Mcp(name="server1", settings={"command": "cmd1"})
        server2 = Mcp(name="server2", settings={"command": "cmd2"})
    
    cdc = ClaudeDesktopConfig()
    # Enable only server1 (server2 will be disabled if it exists)
    MyMcpServers.apply([MyMcpServers.server1], cdc)


0.1.1 (2025-06-07)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- First release
- Add the following public APIs:
    - ``claude_desktop_config.api.ClaudeDesktopConfig
