# -*- coding: utf-8 -*-

from claude_desktop_config import api


def test():
    _ = api
    _ = api.ClaudeDesktopConfig


if __name__ == "__main__":
    from claude_desktop_config.tests import run_cov_test

    run_cov_test(
        __file__,
        "claude_desktop_config.api",
        preview=False,
    )
