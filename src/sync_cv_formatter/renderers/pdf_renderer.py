from pathlib import Path


def render_html_to_pdf(html_file: str, output_dir: str | None = None) -> tuple[bool, str]:
    html_path = Path(html_file)

    if not html_path.exists():
        return False, f"HTML file not found: {html_file}"

    if output_dir is None:
        output_dir = html_path.parent

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = output_dir / html_path.with_suffix(".pdf").name

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return False, "Playwright is not installed. Run: playwright install chromium"

    try:
        file_url = html_path.resolve().as_uri()
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(file_url, wait_until="networkidle")
            page.pdf(
                path=str(pdf_path),
                format="A4",
                print_background=True,
                prefer_css_page_size=True,
                margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            )
            browser.close()

        if pdf_path.exists():
            return True, f"PDF created successfully: {pdf_path}"

        return False, "PDF file was not created by Playwright"
    except Exception as exc:
        return False, f"HTML to PDF rendering failed: {exc}"