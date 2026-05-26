# paper-to-ppt-skill

Agent-agnostic Codex Skill for:

`Academic PDF -> paper detail report -> 10-12 page HTML briefing -> editable PPTX`

## 安装
```bash
npx skills add https://github.com/bramble555/paper-to-ppt-skill
```

## 运行流程（两阶段，含人工确认）

### 阶段一：先解析论文并生成详细汇报
```bash
python scripts/run_pipeline.py --pdf /path/to/paper.pdf
```
默认输出目录是 `./out`，先生成：
- `out/paper-detail.txt`

程序会中断并提示：
“论文详细汇报已生成，是否同意以此内容开始生成 HTML 和 PPT？”

### 阶段二：用户同意后继续生成 HTML + PPT
```bash
python scripts/run_pipeline.py --pdf /path/to/paper.pdf --approve-detail
```
会继续生成：
- `out/preview.html`（10-12 页汇报版 HTML）
- `out/presentation.pptx`（可编辑 PPT）

## 关键说明
- HTML 预览使用模板化结构与样式，设计风格参考 `beautiful-html-templates`。
- PPT 生成采用模板化结构转换策略，间接对齐 `frontend-slides` 的前端幻灯片排版思路。
- 可通过 `--output-dir` 修改输出目录（默认 `./out`）。

## 最终输出
- `out/paper-detail.txt`
- `out/presentation.pptx`
