# Project-Specific Instructions for Claude Code

## Test Strategy and File Structure

This project follows a specific test file naming convention to avoid naming collisions:

- For source code at `${package}/module/sub_module.py`, the corresponding test file is located at `tests/module/test_module_sub_module.py`
- The test file name always includes the full module path to avoid naming collisions

### Examples:
- `claude_desktop_config/impl.py` → `tests/test_impl.py`
- `claude_desktop_config/api.py` → `tests/test_api.py`
- `claude_desktop_config/utils/helper.py` → `tests/utils/test_utils_helper.py`

## Running Code Coverage Tests

### Direct Test Execution (Preferred Method)
Each test file can be run directly to generate a coverage report:

```bash
.venv/bin/python tests/module/test_module_sub_module.py
```

This will:
1. Run all unit tests for that specific module
2. Generate a code coverage HTML report at `htmlcov/${random_hash}_submodule.py.html`
3. Show which lines are covered and which are not covered in the HTML report

### Example:
```bash
.venv/bin/python tests/test_impl.py
```

This runs the coverage test using the built-in `run_cov_test` function from `claude_desktop_config.tests`.

## Coverage Goals
- Aim for 100% code coverage for all implementation files
- Use `# pragma: no cover` for code that cannot be tested (e.g., platform-specific code when testing on a different platform)
- The `get_default_claude_desktop_config_path` function has `# pragma: no cover` because it's platform-specific

## Viewing Coverage Reports
After running a test file, open the generated HTML file to see:
- Green lines: Code that was executed during tests
- Red lines: Code that was not covered by tests
- Line-by-line coverage details