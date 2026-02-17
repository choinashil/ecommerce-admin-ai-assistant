import asyncio
import time

import markdownify
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from app.shared.crawling.parsers.base import BaseParser, ContentFormat, ParseResult

# OOPY 플랫폼 공통 상수
_OOPY_CDN_DOMAIN = "lazyrockets.com"
_OOPY_TOC_CLASS = "notion-table_of_contents-block"
_META_REFRESH_WAIT = 3  # OOPY 로딩 페이지의 meta refresh 대기 시간(초)
_SEARCH_MARKER = "Search"
_BACK_LINK_TEXT = "로 돌아가기"
_HEADER_NOISE = {_SEARCH_MARKER, _BACK_LINK_TEXT}
_FOOTER_NOISE = {"TOP"}


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

    def fetch_html(self, url: str) -> tuple[str, str]:
        """정적 HTML을 가져오고, 필요시 재시도/Playwright 확장한다.

        OOPY는 일부 페이지에서 meta-refresh 로딩 페이지를 먼저 반환한다.
        이를 감지하면 대기 후 재요청하여 실제 콘텐츠를 가져온다.
        """
        html, resolved_url = super().fetch_html(url)

        # OOPY 로딩 페이지 감지: meta refresh + 로딩 스피너만 있는 1KB 미만 응답
        if 'http-equiv="refresh"' in html and len(html) < 2000:
            time.sleep(_META_REFRESH_WAIT)
            html, resolved_url = super().fetch_html(resolved_url)

        if "notion-toggle-block" in html:
            html = asyncio.run(self._expand_toggles(resolved_url))

        return html, resolved_url

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

        for img in body.find_all("img"):
            src = img.get("src", "")
            if not src or _OOPY_CDN_DOMAIN in src or src.startswith("data:image"):
                img.decompose()

        toc_block = body.find(class_=_OOPY_TOC_CLASS)
        if toc_block:
            toc_block.decompose()

        if content_format == ContentFormat.MARKDOWN:
            raw = markdownify.markdownify(
                str(body), heading_style="ATX", bullets="-"
            )
        else:
            raw = body.get_text(separator="\n", strip=True)

        lines = [line.strip() for line in raw.split("\n") if line.strip()]

        lines = self._remove_breadcrumb_lines(lines)

        lines = [line for line in lines if line not in _HEADER_NOISE and line != "/"]

        if lines and lines[0] == title:
            lines = lines[1:]

        if content_format == ContentFormat.MARKDOWN:
            if lines and lines[0].startswith("# ") and lines[0].lstrip("# ") == title:
                lines = lines[1:]

        while lines and lines[-1] in _FOOTER_NOISE:
            lines.pop()

        while lines and _BACK_LINK_TEXT in lines[-1]:
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
            if line == _SEARCH_MARKER:
                break
            breadcrumb_parts.append(line)

        if len(breadcrumb_parts) >= 2:
            return " > ".join(breadcrumb_parts)

        return None

    def _remove_breadcrumb_lines(self, lines: list[str]) -> list[str]:
        """content 앞부분의 breadcrumb 줄들을 제거한다."""
        start_idx = 0
        for i, line in enumerate(lines):
            if line == _SEARCH_MARKER:
                start_idx = i
                break

        return lines[start_idx:]

