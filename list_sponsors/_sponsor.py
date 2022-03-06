import abc
import re
from collections import namedtuple
from textwrap import dedent
from typing import Optional


class Sponsor(
    namedtuple("Sponsor", "name login avatarUrl url monthlyPriceInDollars isOneTimePayment")
):
    @property
    def name_and_login(self) -> str:
        if not self.name:
            return self.login

        return f"{self.name} ({self.login})"

    @property
    def alt(self) -> str:
        return f"onetime: {self.name_and_login}" if self.isOneTimePayment else self.name_and_login


class SponsorRendererInterface(metaclass=abc.ABCMeta):
    REGEXP_HAS_AVATAR = re.compile(r"&u=")

    @abc.abstractclassmethod
    def render(self, sponsor: Sponsor, avatar_size: Optional[int] = None) -> str:
        pass


class MarkdownSponsorRenderer(SponsorRendererInterface):
    def render(self, sponsor: Sponsor, avatar_size: Optional[int] = None) -> str:
        return '[![{alt}]({avatar} "{alt}")]({url})'.format(
            alt=sponsor.alt, avatar=sponsor.avatarUrl, url=sponsor.url
        )


class RstSponsorRenderer(SponsorRendererInterface):
    def render(self, sponsor: Sponsor, avatar_size: Optional[int] = None) -> str:
        return dedent(
            """\
            .. image:: {avatar}
               :target: {url}
               :alt: {alt}"""
        ).format(alt=sponsor.alt, avatar=sponsor.avatarUrl, url=sponsor.url)


class HtmlSponsorRenderer(SponsorRendererInterface):
    def render(self, sponsor: Sponsor, avatar_size: Optional[int] = None) -> str:
        has_avatar = self.REGEXP_HAS_AVATAR.search(sponsor.avatarUrl) is not None

        if has_avatar:
            template = """\
            <a href="{url}">
              <img src="{avatar}"
                   alt="{alt}"
                   title="{alt}">
            </a>"""
        else:
            template = """\
            <a href="{url}">
              <img src="{avatar}"
                   alt="{alt}"
                   title="{alt}"
                   width="{width}" height="{height}">
            </a>"""

        avatar_size = 48

        return dedent(template).format(
            alt=sponsor.alt,
            avatar=sponsor.avatarUrl,
            url=sponsor.url,
            width=avatar_size,
            height=avatar_size,
        )


def create_sponsor_renderer(format_name: str) -> SponsorRendererInterface:
    format_name = format_name.strip().casefold()

    if format_name in ["markdown", "md"]:
        return MarkdownSponsorRenderer()

    if format_name in ["rst", "restructuredtext"]:
        return RstSponsorRenderer()

    if format_name == "html":
        return HtmlSponsorRenderer()

    raise ValueError(f"unknown format: {format_name}")
