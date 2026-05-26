# paper-to-ppt-skill

Agent-agnostic Codex Skill for automating:

`Academic PDF -> parsing -> structured understanding -> graduate-level slides -> editable PPTX`

## 安装（CLI）
```bash
npx skills add https://github.com/bramble555/paper-to-ppt-skill
```

> 这个 skill 设计为“下载后直接在 Codex / Antigravity 里运行”，不要求用户自己配置本地 Python 虚拟环境或 OpenAI API Key。

## 使用方式（Agent 内直接运行）
在 Codex 或 Antigravity 中调用本 skill，传入论文 PDF 路径与输出目录。

示例命令：
```bash
python scripts/run_pipeline.py \
  --pdf /path/to/paper.pdf \
  --output-dir ./out \
  --ppt-theme templates/default_theme.json \
  --html-template templates/html/base.html \
  --html-preview
```

## Agent-first 工作流
1. `run_pipeline.py` 解析 PDF，输出 `parsed_paper.json`。
2. 如需由 Agent 生成高质量 slide plan，可先导出提示词：
   ```bash
   python scripts/run_pipeline.py --pdf /path/to/paper.pdf --output-dir ./out --emit-agent-prompt
   ```
3. 将 `out/agent_prompt.txt` 交给 Codex/Antigravity agent，生成 `slide_plan.json`。
4. 回填并生成最终 PPT：
   ```bash
   python scripts/run_pipeline.py \
     --pdf /path/to/paper.pdf \
     --output-dir ./out \
     --agent-slide-plan-json ./out/slide_plan.json \
     --html-preview
   ```

> 若未提供 `--agent-slide-plan-json`，系统会使用内置 fallback 规划器生成可编辑草稿，供二次润色。

## 输出
- `out/presentation.pptx`（可编辑）
- `out/preview.html` + `out/assets/slide-theme.css`（可选）
- `out/parsed_paper.json`
- `out/slide_plan.json`
- `out/agent_prompt.txt`（可选）

## 结构
- `SKILL.md`：skill 触发与流程说明
- `scripts/`：解析、规划、渲染流水线
- `templates/`：PPT / HTML 模板
- `assets/`：预览样式
- `references/`：prompt 与 schema
