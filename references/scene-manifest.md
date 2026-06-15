# Scene Manifest Format

Use this reference when the user asks for SVG, multi-format export, versioned reconstruction data, or editable scientific figures outside Office. The scene manifest is the shared intermediate representation. Generate it before format-specific code so VBA, SVG, and fallback PPTX stay aligned.

## Required File

Save the manifest as `scene_manifest.json` next to generated outputs.

```json
{
  "version": "1.0",
  "source": {
    "path": "source.png",
    "width_px": 1600,
    "height_px": 900
  },
  "canvas": {
    "width": 1600,
    "height": 900,
    "unit": "px",
    "background": "#ffffff"
  },
  "outputs": {
    "vba": "reconstruct.bas",
    "svg": "reconstruct.svg",
    "pptx": "reconstruct.pptx"
  },
  "palette": {
    "ink": "#111111",
    "muted": "#6b7280",
    "accent": "#2563eb"
  },
  "elements": []
}
```

## Element Schema

Each element must have:

- `id`: stable id, such as `B01`, `E01`, `T01`, `L01`, `R01`.
- `type`: `rect`, `roundrect`, `ellipse`, `line`, `arrow`, `polyline`, `polygon`, `textbox`, `image`, `group`.
- `bucket`: `editable`, `preserved`, or `background`.
- `bbox`: `[x, y, w, h]` in canvas units. Required except for pure lines with endpoints.
- `style`: fill, stroke, stroke_width, opacity, radius, font, font_size, font_weight, align, dash, arrow_start, arrow_end.
- `text`: string for `textbox`, otherwise omitted or null.
- `points`: for `line`, `arrow`, `polyline`, or `polygon`.
- `asset`: local path for `image` elements.
- `preserve_reason`: required when `bucket` is `preserved`.
- `z`: lower draws first.

## Supported SVG Mapping

- `rect` / `roundrect` -> `<rect>`.
- `ellipse` -> `<ellipse>`.
- `line` / `arrow` -> `<line>` or `<polyline>` with marker arrows.
- `polygon` -> `<polygon>`.
- `textbox` -> `<text>` with simple tspans for line breaks.
- `image` -> `<image href="...">`; preserved raster regions remain editable only as positioned image objects, not vector paths.

## SVG Honesty Rules

- SVG output is editable as SVG objects, but preserved raster crops remain raster images inside the SVG.
- Do not claim Office-only effects are perfectly represented in SVG. Shadows, gradients, soft edges, and text wrapping may need approximations.
- If the goal is "科研图可修改", prefer SVG plus scene manifest. If the goal is "PPT 里可修改", prefer VBA/PPTX.
- When both are requested, produce `scene_manifest.json`, `.svg`, `.bas`, and the deck attempt from the same manifest.

## Minimal Example

```json
{
  "version": "1.0",
  "source": {"path": "source.png", "width_px": 800, "height_px": 450},
  "canvas": {"width": 800, "height": 450, "unit": "px", "background": "#ffffff"},
  "elements": [
    {
      "id": "B01",
      "type": "rect",
      "bucket": "background",
      "bbox": [0, 0, 800, 450],
      "style": {"fill": "#ffffff", "stroke": "none"},
      "z": 0
    },
    {
      "id": "E01",
      "type": "roundrect",
      "bucket": "editable",
      "bbox": [80, 120, 180, 64],
      "style": {"fill": "#e0f2fe", "stroke": "#0284c7", "stroke_width": 2, "radius": 12},
      "z": 1
    },
    {
      "id": "T01",
      "type": "textbox",
      "bucket": "editable",
      "bbox": [105, 140, 130, 28],
      "text": "Input",
      "style": {"fill": "#111111", "font_size": 22, "font_weight": "700", "align": "middle"},
      "z": 2
    },
    {
      "id": "L01",
      "type": "arrow",
      "bucket": "editable",
      "points": [[260, 152], [390, 152]],
      "style": {"stroke": "#111111", "stroke_width": 3, "arrow_end": true},
      "z": 3
    }
  ]
}
```
