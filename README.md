# Yuzhoujun Fig2Edit

把科研图、机制图、论文配图、PPT 截图和流程图转换成可继续修改的 PPT / SVG / 结构化资产的 Agent Skill。

核心目标不是“把图片重新生成一张图”，而是把图片拆成：

- 可编辑对象：文字、标题、箭头、标签、图例、坐标轴、边框、色块、caption
- 高清图片层：显微图、热图主体、照片、复杂插画、仪器图、3D 渲染
- 结构清单：`scene_manifest.json`，记录哪些元素可编辑、哪些保留为图片

## 适合谁用

- 科研人员：想修改论文图、机制图、补标签、改 caption、统一配色
- 医学 / 生物 / 材料 / AI 论文作者：需要把扁平图片变成可修改 PPT
- 学术 PPT 制作者：从论文截图、AI 生成图、汇报图中提取可编辑结构
- 设计师 / 助研：需要把客户给的 PNG/JPG 图拆成可编辑交付物
- Agent / Skill 开发者：需要一个“图片转可编辑资产”的工作流模板

## 能做什么

- 生成高清无损工作图：默认把原图转换为 `source_lossless.png` 和 `source_highres_2x.png`
- 输出可编辑 PPTX：文字、箭头、图例等尽量是 PowerPoint 对象
- 输出 SVG：可在浏览器、Illustrator、Inkscape 中继续修改
- 输出结构报告：`scene_manifest.json` 和 `run_report.md`
- 保留复杂图像为 PNG 图层：避免显微图、热图、照片被错误矢量化
- 支持商业交付模式：优先保证不缺图、不乱码、不重叠，再说明哪些部分可编辑

## 推荐交付策略

复杂科研图不应该承诺“100% 自动全矢量可编辑”。从一张扁平 PNG 里无法无损恢复原始图层。

本 skill 默认采用更稳的策略：

1. 第 1 页：保真版  
   放完整高清面板图层，用于对照和直接交付。

2. 第 2 页：可编辑工作版  
   保持完整面板位置，只对文字/箭头区域做局部去字或遮盖，再把文字、箭头、标签重建为可编辑对象。

3. SVG：  
   使用同一套图层逻辑，复杂图像保留为 `<image>`，文字等尽量为 SVG 元素。

这样比“透明参考层”或“把图片裁成半截核心图”更适合真实交付。

## 支持平台

| 平台 | 支持情况 | 用法 |
|---|---|---|
| Codex | 推荐 | 直接安装为 skill，使用 `$yuzhoujun-fig2edit` 调用 |
| Claude / Claude Code | 可适配 | 若支持 skill 目录，复制整个文件夹；否则使用 prompt-only |
| OpenClaw / Hermes / WorkBuddy | 可适配 | 支持 `SKILL.md` 就用完整包，否则复制 `fig2edit-prompt.md` |
| macOS | 可用 | 可生成 PPTX / SVG / manifest；若装 PowerPoint 可进一步自动化 |
| Windows | 可用 | 可生成 PPTX / SVG / VBA；PowerPoint 自动化更完整 |
| Linux | 基础可用 | 可生成 SVG / manifest / PPTX，但通常不能自动运行 PowerPoint |
| WPS | 部分可用 | 可打开 PPTX；VBA/宏能力取决于 WPS 版本 |

## 安装方式

### 方式 A：从 GitHub 安装

```bash
git clone https://github.com/Cosmoslmj/yuzhoujun-fig2edit.git
mkdir -p ~/.codex/skills
ln -s "$(pwd)/yuzhoujun-fig2edit" ~/.codex/skills/yuzhoujun-fig2edit
```

重启 Codex 后即可使用。

### 方式 B：一句话安装

如果你使用的平台支持从 GitHub 安装 Skill / Agent Skill / Custom Skill，可以直接对 Agent 说：

```text
帮我安装这个 skill：https://github.com/Cosmoslmj/yuzhoujun-fig2edit
```

或：

```text
帮我安装这个 skill：Cosmoslmj/yuzhoujun-fig2edit
```

可用于这类平台：

- Codex
- Claude / Claude Code
- OpenClaw
- Hermes
- WorkBuddy
- 其它支持从 GitHub 安装 skill 的 Agent 平台

如果平台不支持自动安装 GitHub skill，就使用下面的 Release zip 包安装方式。

安装完成后重启 Agent、刷新 skill 列表，或重新打开会话即可。

### 方式 C：没有 GitHub，用 Release zip 包

1. 打开 GitHub Releases：

```text
https://github.com/Cosmoslmj/yuzhoujun-fig2edit/releases
```

2. 下载最新版本里的 `yuzhoujun-fig2edit-full.zip`
2. 解压得到 `yuzhoujun-fig2edit/`
3. 复制到 skills 目录

macOS / Linux:

```bash
mkdir -p ~/.codex/skills
cp -R /你的解压路径/yuzhoujun-fig2edit ~/.codex/skills/yuzhoujun-fig2edit
```

Windows:

```text
C:\Users\你的用户名\.codex\skills\yuzhoujun-fig2edit
```

### 方式 D：平台不支持 Skill

使用 `fig2edit-prompt.md`：

1. 打开 `fig2edit-prompt.md`
2. 复制全部内容到 ChatGPT / Claude / WorkBuddy / Hermes
3. 上传图片
4. 让 Agent 按 prompt 输出 SVG / PPTX / manifest

注意：prompt-only 没有本地脚本能力，效果取决于平台是否允许生成文件、读取图片坐标和运行代码。

## 如何调用

中文常用：

```text
用 $yuzhoujun-fig2edit 把这张科研图转成可编辑 PPT 和 SVG。复杂显微图/热图保留为高清 PNG 图层，文字、箭头、图例、标题尽量做成可编辑对象。不要压缩图片。
```

也可以不用记 skill 名，直接用自然语言调用：

```text
用科研图转可编辑 PPT 的技能处理这张图。
```

```text
用图片转可编辑 PPT/SVG 的技能，把这张图转成可修改版本。
```

```text
用 Yuzhoujun Fig2Edit 技能，把这张截图转成可编辑 PPT 和 SVG。
```

不同平台也可以这样说：

```text
调用图片转可编辑 PPT/SVG 的 skill。
```

```text
使用 Fig2Edit，把这张图片变成可编辑 PPT 和 SVG。
```

```text
用科研图可编辑化的技能处理这张论文图。
```

如果平台支持 `$skill-name`，最稳定的调用方式仍然是：

```text
用 $yuzhoujun-fig2edit 处理这张图。
```

商业交付版：

```text
用 $yuzhoujun-fig2edit 输出商业交付版：第 1 页保真完整图，第 2 页可编辑工作版，文字箭头可编辑，复杂图像保留为高清 PNG 图层，同时输出 SVG 和 scene_manifest.json。
```

只要 SVG：

```text
用 $yuzhoujun-fig2edit 把这张流程图重建成可编辑 SVG，复杂图像保留为图片元素，文字和箭头做成 SVG 可编辑对象。
```

高保真优先：

```text
用 $yuzhoujun-fig2edit 处理这张图，优先不要重叠、不要缺图、不要乱码；可编辑性排第二。输出 PPTX、SVG 和报告。
```

## 输出文件结构

典型输出：

```text
01_最终文件/
  reconstruct.pptx
  reconstruct.svg
02_结构与报告/
  scene_manifest.json
  run_report.md
03_高清无损素材/
  highres/source_lossless.png
  highres/source_highres_2x.png
  complete_panels_2x/
  masked_full_panels_2x/
04_生成工程文件/
  build_xxx.js
```

## 示例案例

本仓库内置了你这张斑马鱼科研复合图作为最终案例：

```text
examples/zebrafish/source_zebrafish_tail.png
```

已生成的最终案例文件：

```text
examples/zebrafish/output_v8/01_最终文件/zebrafish_masked_fullpanel_editable_v8.pptx
examples/zebrafish/output_v8/01_最终文件/zebrafish_masked_fullpanel_editable_v8.svg
examples/zebrafish/output_v8/02_结构与报告/scene_manifest.json
examples/zebrafish/output_v8/02_结构与报告/run_report.md
```

重新生成命令：

```bash
python3 scripts/prepare_highres_assets.py \
  examples/zebrafish/source_zebrafish_tail.png \
  examples/zebrafish/output_v8/03_高清无损素材/highres \
  --scale 2

python3 scripts/build_zebrafish_masked_fullpanel_editable_v8.py \
  examples/zebrafish/output_v8/03_高清无损素材/highres/source_highres_2x.png \
  examples/zebrafish/output_v8
```

该脚本代表当前推荐的商业交付模式：

- 第 1 页：完整高清保真版
- 第 2 页：完整面板局部去字 + 可编辑文字/箭头
- 同时输出 SVG
- 所有保留图片用 PNG，不转 JPEG

## 本地验证

```bash
python3 -m py_compile scripts/*.py
python3 scripts/manifest_to_svg.py examples/sample_scene_manifest.json
```

打包：

```bash
python3 scripts/package_release.py
```

生成：

```text
dist/yuzhoujun-fig2edit-full.zip
dist/fig2edit-prompt.md
```

## 重要限制

- 单张 PNG/JPG 不是源文件，无法自动恢复真正的原始图层。
- 显微图、热图、照片、复杂纹理不会被伪装成矢量，只会作为高清图片层保留。
- OCR 或模型识别可能读错文字，交付前必须人工核对专业术语。
- “全部可编辑”和“完全保真”存在取舍；商业交付默认保真优先。
- 如果必须 100% 可编辑，建议提供原始 PPT / AI / PDF / SVG / 数据源，而不是只给截图。
