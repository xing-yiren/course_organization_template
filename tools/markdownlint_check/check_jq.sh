# 1. 选择你要测试的 .ipynb 文件（替换为你的实际文件路径）
NB_FILE="./llm/t5/finetune_t5_daily_email_summarization.ipynb"

# 2. 最简 jq 命令：提取所有 markdown 单元格的 .source 内容，不做任何过滤
echo "===== 原始 markdown 单元格内容 ====="
jq '.cells[] | select(.cell_type == "markdown") | .source' "$NB_FILE"

# 3. 额外：查看该文件的所有单元格类型，确认是否有 markdown 类型
echo "===== 所有单元格类型 ====="
jq '.cells[] | .cell_type' "$NB_FILE" | sort | uniq -c