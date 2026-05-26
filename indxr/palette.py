"""
Per-book color assignment for index PDFs.

Colors are assigned deterministically by book number so the same book always
gets the same color across every generated PDF. The curated default palette
uses dark, saturated colors that stay readable as swatches next to black text
and never wash out. Users may override individual books via the ``book_colors``
config option.
"""

import colorsys
from typing import Dict, List, Optional

from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

# Curated default palette: dark/saturated, mutually distinguishable, and
# readable as a swatch beside black text on a white page.
DEFAULT_PALETTE: List[str] = [
    "#C0392B",  # red
    "#2980B9",  # blue
    "#27AE60",  # green
    "#8E44AD",  # purple
    "#F1C40F",  # yellow
    "#E84393",  # pink
    "#2C3E50",  # navy
    "#C2185B",  # magenta
    "#B7950B",  # gold
    "#1ABC9C",  # turquoise
    "#7D3C98",  # deep purple
    "#5D6D7E",  # slate
]


def _generated_hex(index: int) -> str:
    """Generate a distinct, readable hex color for indices past the palette."""
    # Golden-ratio hue spacing keeps successive colors far apart on the wheel.
    hue = (index * 0.61803398875) % 1.0
    # Moderate saturation/value keeps colors vivid but not washed out and dark
    # enough to read as a swatch.
    r, g, b = colorsys.hsv_to_rgb(hue, 0.65, 0.65)
    return "#{:02X}{:02X}{:02X}".format(int(r * 255), int(g * 255), int(b * 255))


def book_color_hex(book_number: int, overrides: Optional[Dict] = None) -> str:
    """Return the hex color string assigned to a book number.

    Args:
        book_number: The book's integer id (usually 1-indexed).
        overrides: Optional mapping of book number -> hex string from config.
            TOML keys parse as strings, so both int and str keys are accepted.
    """
    if overrides:
        value = overrides.get(book_number)
        if value is None:
            value = overrides.get(str(book_number))
        if value:
            return value

    idx = (book_number - 1) if book_number > 0 else 0
    if idx < len(DEFAULT_PALETTE):
        return DEFAULT_PALETTE[idx]
    return _generated_hex(idx)


def book_color(book_number: int, overrides: Optional[Dict] = None) -> colors.Color:
    """Return the reportlab Color assigned to a book number."""
    return colors.HexColor(book_color_hex(book_number, overrides))


def readable_text_color(hex_color: str) -> colors.Color:
    """Pick black or white text for legibility on the given background color."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    # Perceived luminance (ITU-R BT.601 weights).
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    return colors.black if luminance > 150 else colors.white


def build_legend(book_numbers: List[int], overrides: Optional[Dict] = None) -> Table:
    """Build a 'Book Color Key' flowable mapping each book to its swatch.

    Args:
        book_numbers: Book numbers to include, in display order.
        overrides: Optional config color overrides.
    """
    from reportlab.lib.units import inch

    rows = []
    style_cmds = [
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (1, 0), (1, -1), 10),
        ("TEXTCOLOR", (1, 0), (1, -1), colors.HexColor("#2C3E50")),
        ("LEFTPADDING", (0, 0), (0, -1), 0),
        ("RIGHTPADDING", (0, 0), (0, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("BOX", (0, 0), (0, -1), 0.5, colors.HexColor("#BDC3C7")),
    ]

    for row_idx, book_num in enumerate(book_numbers):
        rows.append(["", f"Book {book_num}"])
        style_cmds.append(
            ("BACKGROUND", (0, row_idx), (0, row_idx), book_color(book_num, overrides))
        )

    legend = Table(rows, colWidths=[0.35 * inch, 1.4 * inch])
    legend.setStyle(TableStyle(style_cmds))
    legend.hAlign = "CENTER"
    return legend
