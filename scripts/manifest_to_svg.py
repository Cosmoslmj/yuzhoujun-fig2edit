#!/usr/bin/env python3
"""Convert a scene_manifest.json reconstruction plan into editable SVG."""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path
from typing import Any


def number(value: Any, default: float = 0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def fmt(value: Any) -> str:
    n = number(value)
    if abs(n - round(n)) < 0.001:
        return str(int(round(n)))
    return f"{n:.3f}".rstrip("0").rstrip(".")


def style_value(style: dict[str, Any], key: str, default: Any = None) -> Any:
    return style.get(key, default)


def paint_attrs(style: dict[str, Any], *, text: bool = False) -> str:
    if text:
        fill = style_value(style, "fill", style_value(style, "color", "#111111"))
        attrs = [f'fill="{html.escape(str(fill))}"']
    else:
        fill = style_value(style, "fill", "none")
        stroke = style_value(style, "stroke", "none")
        attrs = [
            f'fill="{html.escape(str(fill))}"',
            f'stroke="{html.escape(str(stroke))}"',
        ]
        if stroke != "none":
            attrs.append(f'stroke-width="{fmt(style_value(style, "stroke_width", 1))}"')
            if style.get("dash"):
                attrs.append(f'stroke-dasharray="{html.escape(str(style["dash"]))}"')
    if style.get("opacity") is not None:
        attrs.append(f'opacity="{fmt(style["opacity"])}"')
    return " ".join(attrs)


def bbox(element: dict[str, Any]) -> tuple[float, float, float, float]:
    values = element.get("bbox") or element.get("bbox_px") or [0, 0, 0, 0]
    padded = list(values)[:4] + [0, 0, 0, 0]
    return tuple(number(v) for v in padded[:4])  # type: ignore[return-value]


def points_attr(points: list[Any]) -> str:
    pairs = []
    for point in points:
        if isinstance(point, dict):
            x, y = point.get("x", 0), point.get("y", 0)
        else:
            x, y = (list(point) + [0, 0])[:2]
        pairs.append(f"{fmt(x)},{fmt(y)}")
    return " ".join(pairs)


def marker_defs(elements: list[dict[str, Any]]) -> str:
    needs_arrow = any((element.get("style") or {}).get("arrow_end") for element in elements)
    if not needs_arrow:
        return ""
    return """
  <defs>
    <marker id="arrow-end" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L0,6 L9,3 z" fill="context-stroke" />
    </marker>
  </defs>""".rstrip()


def render_text(element: dict[str, Any]) -> str:
    x, y, w, h = bbox(element)
    style = element.get("style") or {}
    font_size = number(style.get("font_size"), 16)
    font_family = html.escape(str(style.get("font_family", "Arial, sans-serif")))
    weight = html.escape(str(style.get("font_weight", "400")))
    align = style.get("align", "start")
    anchor = {"middle": "middle", "center": "middle", "end": "end", "right": "end"}.get(str(align), "start")
    text_x = x + (w / 2 if anchor == "middle" else w if anchor == "end" else 0)
    lines = str(element.get("text") or "").splitlines() or [""]
    first_y = y + max(font_size, (h - font_size * len(lines) * 1.2) / 2 + font_size)
    attrs = [
        f'id="{html.escape(str(element.get("id", "")))}"',
        f'x="{fmt(text_x)}"',
        f'y="{fmt(first_y)}"',
        f'font-family="{font_family}"',
        f'font-size="{fmt(font_size)}"',
        f'font-weight="{weight}"',
        f'text-anchor="{anchor}"',
        paint_attrs(style, text=True),
    ]
    body = []
    for i, line in enumerate(lines):
        dy = "0" if i == 0 else fmt(font_size * 1.2)
        body.append(f'<tspan x="{fmt(text_x)}" dy="{dy}">{html.escape(line)}</tspan>')
    return f"  <text {' '.join(attrs)}>{''.join(body)}</text>"


def render_element(element: dict[str, Any], manifest_dir: Path) -> str:
    element_type = str(element.get("type", "rect")).lower()
    style = element.get("style") or {}
    element_id = html.escape(str(element.get("id", "")))
    x, y, w, h = bbox(element)

    if element_type in {"rect", "roundrect", "rectangle"}:
        radius = style.get("radius", 0 if element_type != "roundrect" else min(w, h) * 0.12)
        return (
            f'  <rect id="{element_id}" x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" '
            f'rx="{fmt(radius)}" ry="{fmt(radius)}" {paint_attrs(style)} />'
        )
    if element_type in {"ellipse", "oval"}:
        return (
            f'  <ellipse id="{element_id}" cx="{fmt(x + w / 2)}" cy="{fmt(y + h / 2)}" '
            f'rx="{fmt(w / 2)}" ry="{fmt(h / 2)}" {paint_attrs(style)} />'
        )
    if element_type in {"line", "arrow"}:
        points = element.get("points") or []
        if len(points) < 2:
            return f"  <!-- skipped {element_id}: missing line points -->"
        (x1, y1), (x2, y2) = (list(points[0]) + [0, 0])[:2], (list(points[-1]) + [0, 0])[:2]
        marker = ' marker-end="url(#arrow-end)"' if style.get("arrow_end") or element_type == "arrow" else ""
        return (
            f'  <line id="{element_id}" x1="{fmt(x1)}" y1="{fmt(y1)}" x2="{fmt(x2)}" y2="{fmt(y2)}" '
            f'{paint_attrs({"fill": "none", **style})}{marker} />'
        )
    if element_type == "polyline":
        marker = ' marker-end="url(#arrow-end)"' if style.get("arrow_end") else ""
        return f'  <polyline id="{element_id}" points="{points_attr(element.get("points") or [])}" {paint_attrs({"fill": "none", **style})}{marker} />'
    if element_type == "polygon":
        return f'  <polygon id="{element_id}" points="{points_attr(element.get("points") or [])}" {paint_attrs(style)} />'
    if element_type in {"textbox", "text"}:
        return render_text(element)
    if element_type in {"image", "raster", "raster_crop"}:
        asset = element.get("asset") or element.get("crop_path") or ""
        href = html.escape(str(asset))
        if asset and Path(asset).is_absolute():
            href = Path(asset).as_uri()
        elif asset:
            candidate = manifest_dir / str(asset)
            href = html.escape(candidate.as_posix() if candidate.exists() else str(asset))
        return (
            f'  <image id="{element_id}" href="{href}" x="{fmt(x)}" y="{fmt(y)}" '
            f'width="{fmt(w)}" height="{fmt(h)}" preserveAspectRatio="xMidYMid meet" />'
        )
    return f"  <!-- skipped {element_id}: unsupported type {html.escape(element_type)} -->"


def manifest_to_svg(manifest: dict[str, Any], manifest_dir: Path) -> str:
    canvas = manifest.get("canvas") or {}
    source = manifest.get("source") or {}
    width = number(canvas.get("width"), number(source.get("width_px"), 960))
    height = number(canvas.get("height"), number(source.get("height_px"), 540))
    background = canvas.get("background")
    elements = sorted(manifest.get("elements") or [], key=lambda item: number((item or {}).get("z"), 0))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{fmt(width)}" height="{fmt(height)}" viewBox="0 0 {fmt(width)} {fmt(height)}">',
    ]
    defs = marker_defs(elements)
    if defs:
        lines.append(defs)
    if background:
        lines.append(f'  <rect id="canvas-background" x="0" y="0" width="{fmt(width)}" height="{fmt(height)}" fill="{html.escape(str(background))}" />')
    for element in elements:
        if isinstance(element, dict):
            lines.append(render_element(element, manifest_dir))
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert scene_manifest.json to editable SVG.")
    parser.add_argument("manifest", help="Path to scene_manifest.json.")
    parser.add_argument("-o", "--output", help="Output SVG path. Defaults to manifest outputs.svg or reconstruct.svg.")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"manifest_to_svg: {exc}", file=sys.stderr)
        return 2

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path((manifest.get("outputs") or {}).get("svg") or "reconstruct.svg")
        if not output_path.is_absolute():
            output_path = manifest_path.parent / output_path

    svg = manifest_to_svg(manifest, manifest_path.parent)
    output_path.write_text(svg, encoding="utf-8")
    print(output_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
