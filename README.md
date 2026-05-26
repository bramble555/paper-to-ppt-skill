# paper-to-ppt-skill

三阶段工作流：

`PDF论文 -> paper-detail.txt(人工确认) -> preview.html(10-12页) -> presentation.pptx(可编辑)`

## 安装
```bash
npx skills add https://github.com/bramble555/paper-to-ppt-skill
```

## 阶段一：解析论文并生成详细汇报（会中断等待）
```bash
python scripts/run_pipeline.py --pdf /path/to/paper.pdf
```
输出：
- `out/paper-detail.txt`

程序会提示：
“论文详细汇报已生成，是否同意以此内容开始生成 HTML 和 PPT？”

## 阶段二：确认后继续生成 HTML 与 PPT
```bash
python scripts/run_pipeline.py --pdf /path/to/paper.pdf --approve-detail
```
输出：
- `out/preview.html`（10-12 页，frontend-slides 风格结构 + beautiful-html-templates 风格样式）
- `out/presentation.pptx`（从 HTML DOM 映射生成、完全可编辑）

## 架构说明
- 主 Agent：`scripts/pdf_parser.py` + `scripts/paper_report.py`
- 子 Agent 1（HTML 渲染官）：`scripts/html_preview.py`
  - 每页 `<section>`，标题 `<h1>/<h2>`，要点 `<ul>/<li>`
- 子 Agent 2（PPTX 转换官）：`scripts/pptx_generator.py`
  - 解析 `preview.html` DOM 并映射为 pptx 幻灯片
