# Zebrafish Figure Example

这是 `Yuzhoujun Fig2Edit` 的内置测试案例，使用一张斑马鱼科研复合图演示商业交付模式。

## 输入

```text
examples/zebrafish/source_zebrafish_tail.png
```

![斑马鱼科研复合图原图](screenshots/01_source_zebrafish_tail.png)

## 生成命令

```bash
python3 scripts/prepare_highres_assets.py \
  examples/zebrafish/source_zebrafish_tail.png \
  examples/zebrafish/output_v8/03_高清无损素材/highres \
  --scale 2

python3 scripts/build_zebrafish_masked_fullpanel_editable_v8.py \
  examples/zebrafish/output_v8/03_高清无损素材/highres/source_highres_2x.png \
  examples/zebrafish/output_v8
```

## 输出

```text
examples/zebrafish/output_v8/01_最终文件/zebrafish_masked_fullpanel_editable_v8.pptx
examples/zebrafish/output_v8/01_最终文件/zebrafish_masked_fullpanel_editable_v8.svg
examples/zebrafish/output_v8/02_结构与报告/scene_manifest.json
examples/zebrafish/output_v8/02_结构与报告/run_report.md
```

最终 PPT 可编辑工作页预览：

![斑马鱼可编辑 PPT 预览](screenshots/02_editable_ppt_preview.png)

最终文件：

![最终 PPT 和 SVG 文件](screenshots/03_final_files_preview.png)

输出目录结构：

![输出目录结构](screenshots/04_output_folder_preview.png)

## 设计说明

- 第 1 页：原始保真版，四个完整高清面板作为图片图层。
- 第 2 页：完整面板局部去字可编辑版，底层仍是完整面板 PNG，文字/箭头区域被局部遮盖后重建为可编辑对象。
- SVG：使用 masked full-panel 图层和可编辑标题/caption。

中间高清素材目录 `03_高清无损素材/` 可由上面的命令重新生成，未提交到仓库以避免仓库过大。
