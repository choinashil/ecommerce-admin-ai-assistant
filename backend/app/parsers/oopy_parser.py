import asyncio

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from app.parsers.base import BaseParser, ParseResult


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

    def parse(self, html: str) -> ParseResult:
        soup = BeautifulSoup(html, "lxml")
        title = self._extract_title(soup)
        breadcrumb = self._extract_breadcrumb(soup)
        content = self._extract_content(soup, title)
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

    def _extract_content(self, soup: BeautifulSoup, title: str) -> str:
        """본문 내용을 추출한다.

        breadcrumb, 제목 중복, TOC(목차), OOPY UI 텍스트를 제거한다.
        """
        for tag in soup.find_all(
            ["nav", "header", "footer", "script", "style", "noscript"]
        ):
            tag.decompose()

        body = soup.find("body")
        if not body:
            return ""

        text = body.get_text(separator="\n", strip=True)
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        # breadcrumb + "Search" 줄 제거 (순서 중요: "Search"를 구분자로 사용하므로 noise 제거보다 먼저)
        lines = self._remove_breadcrumb_lines(lines)

        # OOPY UI 텍스트 제거 ("/" 구분자, "로 돌아가기", 등)
        _HEADER_NOISE = {"Search", "로 돌아가기"}
        _TOGGLE_HINT = "(클릭) "
        lines = [line for line in lines if line not in _HEADER_NOISE and line != "/"]
        lines = [line.replace(_TOGGLE_HINT, "") for line in lines]

        # 제목 중복 제거 (content 첫 줄이 title과 같으면 제거)
        if lines and lines[0] == title:
            lines = lines[1:]

        # TOC(목차) 제거
        lines = self._remove_toc(lines)

        # 마지막 footer 잔재 제거 ("식스샵 프로 가이드", "TOP" 등)
        _FOOTER_NOISE = {"식스샵 프로 가이드", "TOP"}
        while lines and lines[-1] in _FOOTER_NOISE:
            lines.pop()

        return "\n".join(lines)

    def _extract_breadcrumb(self, soup: BeautifulSoup) -> str | None:
        """OOPY 페이지에서 breadcrumb을 추출한다.

        OOPY는 aria-label 없이 breadcrumb을 렌더링하므로,
        '/' 구분자 패턴으로 첫 몇 줄에서 추출한다.
        """
        body = soup.find("body")
        if not body:
            return None

        text = body.get_text(separator="\n", strip=True)
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        # 첫 줄들이 breadcrumb 조각인 경우 ('홈', '/', 'FAQ', ...)
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
        """content 앞부분의 breadcrumb 줄들을 제거한다.

        OOPY breadcrumb은 '/' 구분자와 경로 조각이 별개 줄로 렌더링된다.
        'Search' 줄 직전까지가 breadcrumb 영역이다.
        """
        start_idx = 0
        for i, line in enumerate(lines):
            if line == "Search":
                start_idx = i
                break

        return lines[start_idx:]

    def _remove_toc(self, lines: list[str]) -> list[str]:
        """본문 시작 전의 목차(TOC)를 제거한다.

        OOPY에서 Notion의 TOC 블록은 소제목 목록으로 렌더링된다.
        본문은 소제목이 아닌 일반 텍스트로 시작하므로,
        첫 줄부터 연속된 소제목들이 본문에 다시 등장하면 TOC로 판단한다.
        """
        if len(lines) < 3:
            return lines

        # 첫 줄부터 연속된 짧은 줄들이 뒤에서 소제목으로 재등장하는지 확인
        toc_end = 0
        remaining = lines[1:]  # 첫 줄 이후 텍스트에서 재등장 검사

        for i, line in enumerate(lines):
            # 소제목은 보통 짧고 (50자 이하), 불렛(•◦▪)이 아님
            if len(line) > 50 or line.startswith(("•", "◦", "▪")):
                break
            # 이 줄이 나중에 다시 등장하면 TOC 항목
            if line in remaining[i:]:
                toc_end = i + 1
            else:
                break

        return lines[toc_end:]
