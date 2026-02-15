import asyncio

import markdownify
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from app.shared.crawling.parsers.base import BaseParser, ContentFormat, ParseResult


class OopyParser(BaseParser):
    """OOPY(Notion 기반) 페이지 파서."""

    @staticmethod
    async def _expand_toggles(url: str) -> str:
        """Playwright로 페이지를 열고 모든 토글을 펼친 뒤 HTML을 반환한다."""
        _TOGGLE_EXPAND_DELAY_MS = 800
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, wait_until="networkidle")

            buttons = await page.query_selector_all('[aria-label="unfold"]')
            for button in buttons:
                await button.click()
                await page.wait_for_timeout(_TOGGLE_EXPAND_DELAY_MS)

            html = await page.content()
            await browser.close()
            return html

    def fetch_html(self, url: str) -> str:
        """정적 HTML을 가져오고, 토글이 있으면 Playwright로 재크롤링한다."""
        html = super().fetch_html(url)
        if "notion-toggle-block" in html:
            html = asyncio.run(self._expand_toggles(url))
        return html

    def parse(
        self, html: str, *, content_format: ContentFormat = ContentFormat.TEXT
    ) -> ParseResult:
        soup = BeautifulSoup(html, "lxml")
        title = self._extract_title(soup)
        breadcrumb = self._extract_breadcrumb(soup)
        content = self._extract_content(soup, title, content_format)
        return ParseResult(title=title, content=content, breadcrumb=breadcrumb)

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """페이지 제목을 추출한다."""
        h1 = soup.find("h1")
        if h1:
            return h1.get_text(strip=True)

        title_tag = soup.find("title")
        if title_tag:
            return title_tag.get_text(strip=True)

        return "제목 없음"

    def _extract_content(
        self,
        soup: BeautifulSoup,
        title: str,
        content_format: ContentFormat = ContentFormat.TEXT,
    ) -> str:
        """본문 내용을 추출한다.

        breadcrumb, 제목 중복, TOC(목차), OOPY UI 텍스트를 제거한다.
        content_format에 따라 텍스트 또는 마크다운으로 출력한다.
        """
        for tag in soup.find_all(
            ["nav", "header", "footer", "script", "style", "noscript"]
        ):
            tag.decompose()

        body = soup.find("body")
        if not body:
            return ""

        if content_format == ContentFormat.MARKDOWN:
            raw = markdownify.markdownify(
                str(body), heading_style="ATX", bullets="-"
            )
        else:
            raw = body.get_text(separator="\n", strip=True)

        lines = [line.strip() for line in raw.split("\n") if line.strip()]

        lines = self._remove_breadcrumb_lines(lines)

        _HEADER_NOISE = {"Search", "로 돌아가기"}
        lines = [line for line in lines if line not in _HEADER_NOISE and line != "/"]

        if lines and lines[0] == title:
            lines = lines[1:]

        if content_format == ContentFormat.MARKDOWN:
            if lines and lines[0].startswith("# ") and lines[0].lstrip("# ") == title:
                lines = lines[1:]

        lines = self._remove_toc(lines)

        _FOOTER_NOISE = {"TOP"}
        while lines and lines[-1] in _FOOTER_NOISE:
            lines.pop()

        return "\n".join(lines)

    def _extract_breadcrumb(self, soup: BeautifulSoup) -> str | None:
        """OOPY 페이지에서 breadcrumb을 추출한다."""
        body = soup.find("body")
        if not body:
            return None

        text = body.get_text(separator="\n", strip=True)
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        breadcrumb_parts = []
        for line in lines:
            if line == "/":
                continue
            if line == "Search":
                break
            breadcrumb_parts.append(line)

        if len(breadcrumb_parts) >= 2:
            return " > ".join(breadcrumb_parts)

        return None

    def _remove_breadcrumb_lines(self, lines: list[str]) -> list[str]:
        """content 앞부분의 breadcrumb 줄들을 제거한다."""
        start_idx = 0
        for i, line in enumerate(lines):
            if line == "Search":
                start_idx = i
                break

        return lines[start_idx:]

    def _remove_toc(self, lines: list[str]) -> list[str]:
        """본문 시작 전의 목차(TOC)를 제거한다."""
        if len(lines) < 3:
            return lines

        toc_end = 0
        remaining = lines[1:]

        for i, line in enumerate(lines):
            if len(line) > 50 or line.startswith(("•", "◦", "▪")):
                break
            if line in remaining[i:]:
                toc_end = i + 1
            else:
                break

        return lines[toc_end:]
