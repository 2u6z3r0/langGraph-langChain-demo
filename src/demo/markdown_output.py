from __future__ import annotations


def render_markdown(markdown_text: str) -> str:
    """Return terminal-rendered markdown text for use with print()."""
    text = str(markdown_text)

    try:
        from rich.console import Console
        from rich.markdown import Markdown as RichMarkdown

        console = Console(force_terminal=True)
        with console.capture() as capture:
            console.print(RichMarkdown(text))
        return capture.get().rstrip("\n")

    except Exception:
        return text
