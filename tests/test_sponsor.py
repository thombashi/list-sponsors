import difflib
import sys

import pytest

from list_sponsors._sponsor import Sponsor, create_sponsor_renderer


def print_test_result(expected, actual, error=None):
    print(f"[expected]\n{expected}\n")
    print(f"[actual]\n{actual}\n")

    if error:
        print(error, file=sys.stderr)

    print("----------------------------------------")
    d = difflib.Differ()
    diff = d.compare(expected.splitlines(), actual.splitlines())
    for d in diff:
        print(d)


TEST_SPONSOR = Sponsor(
    name="Tsuyoshi Hombashi",
    login="thombashi",
    avatarUrl="https://avatars.githubusercontent.com/u/15517661?u=fc66e4f996473c347a7396c2ab7a78f9903818bb&v=4",
    url="https://github.com/thombashi",
    monthlyPriceInDollars=1,
    isOneTimePayment=False,
)
SPONSOR_MARKDOWN = '[![Tsuyoshi Hombashi (thombashi)](https://avatars.githubusercontent.com/u/15517661?u=fc66e4f996473c347a7396c2ab7a78f9903818bb&v=4 "Tsuyoshi Hombashi (thombashi)")](https://github.com/thombashi)'
SPONSOR_RST = """\
.. image:: https://avatars.githubusercontent.com/u/15517661?u=fc66e4f996473c347a7396c2ab7a78f9903818bb&v=4
   :target: https://github.com/thombashi
   :alt: Tsuyoshi Hombashi (thombashi)"""
SPONSOR_HTML = """\
<a href="https://github.com/thombashi">
  <img src="https://avatars.githubusercontent.com/u/15517661?u=fc66e4f996473c347a7396c2ab7a78f9903818bb&v=4"
       alt="Tsuyoshi Hombashi (thombashi)"
       title="Tsuyoshi Hombashi (thombashi)"
       width="48" height="48">
</a>"""


class Test_Sponsor_render:
    @pytest.mark.parametrize(
        ["value", "format_name", "expected"],
        [
            [TEST_SPONSOR, "markdown", SPONSOR_MARKDOWN],
            [TEST_SPONSOR, "Markdown", SPONSOR_MARKDOWN],
            [TEST_SPONSOR, "md", SPONSOR_MARKDOWN],
            [TEST_SPONSOR, "rst", SPONSOR_RST],
            [TEST_SPONSOR, "restructuredtext", SPONSOR_RST],
            [TEST_SPONSOR, "html", SPONSOR_HTML],
            [TEST_SPONSOR, "HTML", SPONSOR_HTML],
        ],
    )
    def test_normal(self, value, format_name, expected):
        renderer = create_sponsor_renderer(format_name)
        output = renderer.render(value)
        print_test_result(expected=expected, actual=output)
        assert output == expected
