from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from jinja2 import Environment, FileSystemLoader, select_autoescape

from syncques_resume_renderer.schemas.resume_document import ResumeDocument, ResumeTemplateId

_PKG_DIR = Path(__file__).resolve().parent.parent
HTML_TEMPLATES_DIR = _PKG_DIR / "templates" / "html"

_MONTHS = (
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
)


def _format_resume_date(value: str | None) -> str:
    if not value:
        return "Present"

    normalized = str(value).strip()
    if normalized.lower() == "present":
        return "Present"

    try:
        parsed = datetime.fromisoformat(normalized.replace("Z", "+00:00"))
        return f"{_MONTHS[parsed.month - 1]} {parsed.year}"
    except ValueError:
        pass

    if len(normalized) >= 7 and normalized[4] == "-":
        try:
            year = int(normalized[:4])
            month = int(normalized[5:7])
            if 1 <= month <= 12:
                return f"{_MONTHS[month - 1]} {year}"
        except ValueError:
            pass

    return normalized


def _format_external_url(url: str | None) -> str:
    if not url:
        return ""
    normalized = str(url).strip()
    return normalized if normalized.startswith("http") else f"https://{normalized}"


def _resume_link_domain(url: str | None) -> str | None:
    href = _format_external_url(url)
    if not href:
        return None
    try:
        hostname = urlparse(href).hostname or ""
        return hostname.removeprefix("www.") or None
    except ValueError:
        return None


def _resume_favicon_url(url: str | None) -> str:
    domain = _resume_link_domain(url)
    if not domain:
        return ""
    return f"https://www.google.com/s2/favicons?domain={domain}&sz=32"


_PLATFORM_LABELS = {
    "linkedin": "LinkedIn",
    "github": "GitHub",
    "gitlab": "GitLab",
    "twitter": "Twitter",
    "x": "X",
    "youtube": "YouTube",
    "instagram": "Instagram",
    "facebook": "Facebook",
    "portfolio": "Portfolio",
    "website": "Website",
    "syncques": "SyncQues",
    "leetcode": "LeetCode",
    "stackoverflow": "Stack Overflow",
    "medium": "Medium",
    "behance": "Behance",
    "dribbble": "Dribbble",
    "credential": "View Credential",
    "live": "Live",
}

_DOMAIN_LABEL_PATTERNS: list[tuple[str, str]] = [
    ("linkedin.com", "LinkedIn"),
    ("github.com", "GitHub"),
    ("gitlab.com", "GitLab"),
    ("twitter.com", "X"),
    ("x.com", "X"),
    ("youtube.com", "YouTube"),
    ("youtu.be", "YouTube"),
    ("instagram.com", "Instagram"),
    ("facebook.com", "Facebook"),
    ("fb.com", "Facebook"),
    ("syncques.com", "SyncQues"),
    ("leetcode.com", "LeetCode"),
    ("stackoverflow.com", "Stack Overflow"),
    ("medium.com", "Medium"),
    ("behance.net", "Behance"),
    ("dribbble.com", "Dribbble"),
    ("credly.com", "Credly"),
]


def _resume_link_label(
    platform_or_kind: str, url: str | None = None, fallback: str | None = None
) -> str:
    platform_key = platform_or_kind.lower().replace(" ", "_")
    if platform_key in _PLATFORM_LABELS:
        return _PLATFORM_LABELS[platform_key]

    href = _format_external_url(url)
    if href:
        lower_href = href.lower()
        for domain, label in _DOMAIN_LABEL_PATTERNS:
            if domain in lower_href:
                return label

        domain = _resume_link_domain(href)
        if domain:
            base = domain.split(".")[0]
            return base[:1].upper() + base[1:]

    if fallback:
        return fallback

    return platform_or_kind.replace("_", " ").title()


TEMPLATE_DIRS: dict[ResumeTemplateId, str] = {
    "professional": "professional",
    "executive": "executive",
    "modern": "modern",
    "classic": "classic",
    "compact": "compact",
}

_LEGACY_TEMPLATE_ALIASES: dict[str, ResumeTemplateId] = {
    "creative": "modern",
}


def _get_template_env(template_id: ResumeTemplateId) -> Environment:
    template_dir = HTML_TEMPLATES_DIR / TEMPLATE_DIRS[template_id]
    env = Environment(
        loader=FileSystemLoader(
            [str(template_dir), str(HTML_TEMPLATES_DIR)],
        ),
        autoescape=select_autoescape(["html", "xml"]),
    )
    env.filters["format_resume_date"] = _format_resume_date
    env.filters["format_external_url"] = _format_external_url
    env.filters["resume_favicon_url"] = _resume_favicon_url
    env.globals["resume_link_label"] = _resume_link_label
    return env


def _load_css(template_id: ResumeTemplateId) -> str:
    css_path = HTML_TEMPLATES_DIR / TEMPLATE_DIRS[template_id] / "styles.css"
    return css_path.read_text(encoding="utf-8")


def _resolve_template_id(
    template_id: str | ResumeTemplateId | None,
    *,
    fallback: ResumeTemplateId = "professional",
) -> ResumeTemplateId:
    normalized = str(template_id or fallback).strip().lower()
    if normalized in _LEGACY_TEMPLATE_ALIASES:
        return _LEGACY_TEMPLATE_ALIASES[normalized]
    if normalized in TEMPLATE_DIRS:
        return normalized  # type: ignore[return-value]
    return fallback


def populate_html_template(
    document: ResumeDocument,
    template_id: ResumeTemplateId | None = None,
    *,
    interactive: bool = False,
) -> str:
    selected_template = _resolve_template_id(template_id or document.template_id)
    env = _get_template_env(selected_template)
    template = env.get_template("template.html.j2")
    return template.render(
        document=document,
        css_content=_load_css(selected_template),
        interactive=interactive,
    )


def save_html_file(content: str, output_path: str) -> str:
    html_path = output_path.replace(".pdf", ".html")
    Path(html_path).write_text(content, encoding="utf-8")
    return html_path