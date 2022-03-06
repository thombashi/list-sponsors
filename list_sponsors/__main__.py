"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import argparse
import os
import sys
from textwrap import dedent

from .__version__ import __version__
from ._const import MODULE_NAME, Default, LogLevel
from ._gh_client import GitHubV4Client
from ._logger import initialize_logger, logger
from ._sponsor import create_sponsor_renderer


def parse_option() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=dedent(
            """\
            A CLI tool to list GitHub sponsors of a user/organization with specified format.

            Require a GitHub personal access token either by
            --token option or GITHUB_TOKEN environment variable.
            """
        ),
        epilog=dedent(
            f"""\
            Issue tracker: https://github.com/thombashi/{MODULE_NAME}/issues
            """
        ),
    )
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")

    parser.add_argument(
        "--name",
        metavar="GITHUB_LOGIN_NAME",
        help="""
        login name of a GitHub user.
        if this option is not specified, use the login name of the GitHub personal access token.
        """,
    )
    parser.add_argument(
        "--token",
        metavar="GITHUB_TOKEN",
        help="GitHub personal access token.",
    )
    parser.add_argument(
        "--format",
        choices=["md", "markdown", "rst", "restructuredtext", "html"],
        default="markdown",
        help="defaults to markdown.",
    )
    parser.add_argument(
        "--avatar-size",
        metavar="SIZE",
        type=int,
        default=Default.AVATAR_SIZE,
        help="avatar size will be SIZExSIZE defaults to %(default)s.",
    )

    loglevel_dest = "log_level"
    group = parser.add_mutually_exclusive_group()  # type: ignore
    group.add_argument(
        "--debug",
        dest=loglevel_dest,
        action="store_const",
        const=LogLevel.DEBUG,
        default=LogLevel.INFO,
        help="for debug print.",
    )
    group.add_argument(
        "--quiet",
        dest=loglevel_dest,
        action="store_const",
        const=LogLevel.QUIET,
        default=LogLevel.INFO,
        help="suppress execution log messages.",
    )

    return parser.parse_args()


def main() -> int:
    ns = parse_option()

    initialize_logger(name=MODULE_NAME, log_level=ns.log_level)

    token = ns.token
    if not token:
        token = os.environ.get("GITHUB_TOKEN")
    if not token:
        logger.error(
            "require a GitHub personal access token either by "
            "--token option or GITHUB_TOKEN environment variable"
        )
        sys.exit(22)

    gh_client = GitHubV4Client(token)

    login_name = ns.name
    if not login_name:
        login_name = gh_client.fetch_login_user_name()

    renderer = create_sponsor_renderer(ns.format)

    for sponsor in gh_client.fetch_sponsors(login_name, avatar_size=ns.avatar_size):
        link = renderer.render(sponsor, avatar_size=ns.avatar_size)
        print(link)

    return 0


if __name__ == "__main__":
    sys.exit(main())
