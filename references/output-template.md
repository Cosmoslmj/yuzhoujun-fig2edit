# Output Template

Use this response structure when generating reconstruction VBA, SVG, or multi-format editable scientific figure outputs. For presentation targets, do not return only a PNG or preview image; the response must account for editable VBA/deck artifacts and the detected Office/WPS runtime. For SVG targets, distinguish vector SVG objects from preserved raster image elements.

## Short Explanation

State the selected output target, Office host when relevant, canvas size, editability mode, and reconstruction strategy in 2-4 sentences. Mention whether the result is pure editable vector/Shapes, high-editability hybrid, high-fidelity hybrid, or background-image-assisted. Say whether Microsoft PowerPoint automation, WPS-compatible manual flow, SVG export, or a no-local-runtime fallback was used.

## Environment

List what was detected or inferred:

- OS:
- Presentation app:
- SVG/vector tooling, if checked:
- Source size:
- Lossless/high-res working asset:
- Materialization path: Windows PowerPoint COM / macOS PowerPoint AppleScript / WPS-compatible manual path / no local runtime.
- Automation status:

## Generated Artifacts

List the local artifacts that were created or attempted:

- VBA source:
- Scene manifest, if generated:
- SVG file, if generated:
- Editable deck:
- Lossless/high-res assets:
- Preserved raster assets, if any:
- Opened in app: yes/no, with blocker if no.
- Automation runner, if created or used:
- Preview screenshot, if any: optional diagnostic only; not the editable deliverable.

## Editability Map

Summarize what is editable and what is preserved:

- Editable Shapes:
- Editable SVG/vector elements:
- Preserved raster elements:
- Non-editable regions and why:
- Full-background image used: yes/no.

For each preserved raster element, include its asset path, approximate source region, slide placement, and reason for preservation.

If any whole panel or large region is preserved as an image, explicitly say which internal items are not editable. Do not imply that a deck is fully editable when it contains large raster regions.

## Complete VBA Code

For VBA/Office targets, return one complete code block:

```vb
' Paste into the VBA editor and run ReconstructFromImage
Option Explicit

Sub ReconstructFromImage()
    ' Complete runnable macro here.
End Sub
```

The code must include cleanup, canvas setup, background, each object, shape names, color settings, and visual-region comments. Use a stable generated-object prefix such as `AITVBA_`. In hybrid mode, preserved raster crops must be inserted with `Shapes.AddPicture` and named with the same prefix.

## Scene Manifest / SVG

For SVG or multi-format targets, list:

- Scene manifest path:
- SVG path:
- SVG element count:
- Preserved `<image>` elements:

If helpful, include a short excerpt of `scene_manifest.json`, but do not paste a very large manifest unless the user asks.

## How to Run

Give brief host-specific steps and prefer the already-created local artifact when available:

- Windows PowerPoint: open the generated deck if it is not already open. If automation failed, open VBA editor, import or paste the generated `.bas` code, and run the macro. If VBA import was blocked, mention Trust Center macro/VBA project access.
- macOS PowerPoint: open the generated deck if it is not already open. If automation failed, open VBA editor, import or paste the generated `.bas` code, and run the macro. If AppleScript or macro security blocked execution, say so.
- WPS Presentation: open WPS Presentation, open or create a deck, open its macro/VBA editor if the installed WPS version supports it, import or paste the generated `.bas` code, and run the macro. If macro support is unavailable, use the editable `.pptx` fallback when provided.
- Excel: open VBA editor, insert module, paste code, select/create target sheet, run the macro.
- Word: open VBA editor, insert module, paste code, run the macro.

## Self-Check Results

Include the required checks:

- Structure check:
- Image quality check:
- Editability check:
- Preservation check:
- Scene manifest check:
- SVG check:
- Code check:
- Materialization check:
- Visual check:

Each item should state pass/revised/remaining concern. Preservation check should state "not applicable" for pure editable reconstructions. SVG check should state "not applicable" when no SVG was requested. Materialization check must mention the detected app and whether the macro actually ran. Visual check must say "manual estimate" unless a rendered screenshot was actually compared.

## Possible Errors

List expected differences such as approximate gradients, substituted fonts, unreadable text placeholders, simplified icons, preserved raster regions that are not editable Shapes/vector paths, photo-like areas that cannot be fully recreated with Shapes/SVG primitives, PowerPoint automation limitations, WPS compatibility limits, or absent local office runtime.

## Next Optimization

Suggest one concrete next step, such as providing a screenshot of the VBA render for image comparison or specifying exact slide size/font constraints.
