# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from claude_desktop_config.tests import run_cov_test

    run_cov_test(
        __file__,
        "claude_desktop_config",
        is_folder=True,
        preview=False,
    )
