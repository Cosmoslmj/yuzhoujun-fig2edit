# Reconstruction Checklist

Use this checklist before returning VBA/SVG reconstruction artifacts. If an item fails, revise the output or explicitly document the remaining uncertainty.

## Canvas

- Target output is identified as PowerPoint, Excel, Word, SVG, or multi-format.
- Editability mode is identified as high-fidelity hybrid or high-editability reconstruction.
- Source image quality path is documented: original, lossless working PNG, high-res working PNG if used.
- For presentation targets, the local runtime is identified as Microsoft PowerPoint, WPS Presentation/WPS Office, none, or unknown.
- Reconstruction mode is identified as pure editable, hybrid preserved-element, or full-background-assisted.
- Canvas size is set or clearly controlled.
- Aspect ratio matches the source image.
- If a standard slide ratio is required, the source image is uniformly fitted with offsets instead of stretched.
- Coordinate system is in points for Office outputs and pixels/viewBox units for SVG outputs unless the user asked otherwise.
- Scale factor is consistent for all objects.

## Background

- Background color or gradient is recreated.
- Page/slide edges and margins match the source.
- Textures are approximated honestly, not claimed as exact.
- If a source image is used as a background, that choice is explicitly labeled.

## Main Objects

- Every major visible object is represented.
- Every major object is classified as editable Shape/vector element, preserved raster element, or background/base.
- Whole panels are not preserved as one image when their text, arrows, labels, legend, axis titles, or captions can be rebuilt as editable overlays.
- High-editability mode extracts every legible label, arrow, leader line, bracket, panel letter, legend item, and caption into editable objects unless explicitly impossible.
- Editable text does not duplicate visible text that remains inside a preserved raster crop.
- If editable text replaces raster text, the original raster text is excluded by crop or covered by a clean background mask.
- Repeated elements use consistent dimensions and spacing.
- Icons are built from simple shapes, lines, or freeforms where practical.
- Tables, charts, and UI panels retain their hierarchy.
- Text, arrows, boxes, callouts, and connectors are editable Shapes/SVG elements unless explicitly included in a preserved raster crop for a stated reason.
- Preserved raster crops are limited to the smallest useful region around complex artwork.

## Margins and Alignment

- Outer margins match the reference.
- Left/right/top/bottom alignments are intentional.
- Centers, baselines, gutters, and repeated spacing are consistent.
- Objects that should touch or overlap do so without accidental gaps.

## Color

- Key colors are expressed as `RGB(r, g, b)`.
- Palette is consistent across repeated components.
- Transparency values match glass, overlay, disabled, or muted elements.
- Gradients are approximated with Office gradient APIs or layered translucent shapes.

## Typography

- Legible text is converted to TextBoxes.
- Unreadable text uses placeholders with comments.
- Font family, size, weight, case, and color approximate the source.
- Text box margins do not shift text away from the intended position.
- Text does not overflow unless the original does.

## Lines and Borders

- Stroke colors, weights, dashes, and arrowheads match the source.
- Border visibility is correct for each shape.
- Rounded corners are approximated using shape adjustments where possible.

## Layers

- Objects are created back-to-front or explicitly ordered with `ZOrder`.
- Shadows sit behind their objects.
- Overlays, masks, highlights, and callouts appear above the correct base layers.
- Preserved raster elements are placed at the correct z-order relative to editable overlays.

## Shadows and Effects

- Shadow offset, blur, color, and transparency are approximated.
- Soft edges, glow, or blur-like effects are represented with Office effects or layered shapes.
- Effects are omitted only when the Office API cannot reproduce them reasonably.

## Code Runability

- Code contains `Sub ... End Sub`.
- Variables are declared or intentionally simple.
- Cleanup code avoids deleting unrelated user content when a safer name-prefix cleanup is required.
- Host-specific object models are valid.
- WPS-only mode avoids advanced PowerPoint-only APIs unless local WPS support was verified.
- Shape names are assigned.
- Generated shape names use a stable prefix such as `AITVBA_`.
- Preserved raster shapes use the generated prefix and descriptive names.
- `Shapes.AddPicture` uses local asset paths and embeds images when the host supports it.
- Comments label visual regions.
- Generated code can be pasted into the VBA editor and run.

## Scene Manifest and SVG

- `scene_manifest.json` is saved when SVG or multi-format output is requested.
- Manifest contains `version`, `source`, `canvas`, `outputs`, and `elements`.
- Element ids are stable and match the generated SVG ids and VBA shape names where practical.
- Z-order is explicit and generated outputs draw lower `z` elements first.
- SVG file is saved when requested.
- SVG is parseable XML and has a matching `viewBox`.
- SVG includes expected primitive elements for editable objects and `<image>` elements only for preserved raster assets.
- Preserved raster assets referenced by SVG exist at the reported paths.
- The final response does not claim preserved raster assets are vectorized.

## Hybrid Preservation

- Hybrid mode is used only when requested or when pure shape reconstruction would be noisy/low-fidelity.
- Preserved elements have asset files, source crop coordinates, slide placement coordinates, and preservation reasons.
- Preserved assets are cropped from lossless/high-res PNG working assets, not from compressed screenshots.
- Preserved raster cores are the smallest useful regions; full-panel preserved images are justified in the report if used.
- Preserved assets are stored next to the generated VBA/deck, preferably in an `assets/` folder.
- Editable overlays do not get flattened into the preserved crop unless necessary and documented.
- The final response tells the user which elements are not editable because they are preserved raster assets.

## Image Quality

- Source dimensions are recorded.
- Lossless PNG working asset is created when local file access is available.
- 2x high-res working asset is created by default for raster preservation; 4x is used only when appropriate.
- PPTX embeds PNG assets without intentional downsampling or JPEG conversion.
- SVG preserved images are embedded or linked from PNG assets, not lossy JPEG.
- Any final preview/export is rendered at 2x or higher when generated.

## Materialization

- VBA source was saved to a local `.bas`, `.vba`, or `.txt` file.
- SVG and scene manifest paths are reported when generated.
- Preserved raster assets were saved locally when hybrid mode is used.
- The local presentation runtime was detected or explicitly marked unknown.
- Windows Microsoft PowerPoint uses the Windows COM path when available.
- macOS Microsoft PowerPoint uses the AppleScript path when available.
- WPS-only environments are treated as compatibility/manual unless local macro automation is actually verified.
- The editable deck was created/opened, or the blocker is stated plainly.
- If no local presentation app exists, a `.bas` is still delivered and an editable `.pptx` fallback is generated when feasible.
- PNG/JPEG/PDF previews are labeled as diagnostics only and are not treated as the final editable deliverable.

## Difference Statement

- Remaining visual differences are listed plainly.
- Complex photo, texture, or person limitations are acknowledged.
- Hybrid preserved raster regions are identified as non-editable image assets.
- The next iteration request is specific: ask for a rendered screenshot, target host, or higher-resolution source only when useful.
