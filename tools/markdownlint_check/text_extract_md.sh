#!/bin/bash
set -x  # 打印执行过程，便于调试

# ===================== 配置项（根据你的本地环境修改） =====================
# 本地测试的 IPYNB 文件目录（替换为你要测试的文件夹路径）
TEST_IPYNB_DIR="./cv"
# 临时 MD 文件输出目录（会自动创建/清空）
TARGET_DIR="./temp_md"
# 映射表输出文件
MAP_FILE="./md_ipynb_mapping.log"
# 错误日志文件
ERROR_LOG="./extract_error.log"

# ===================== 核心提取逻辑（和 CI 中一致） =====================
# 初始化目录和文件
mkdir -p "$TARGET_DIR"
rm -rf "$TARGET_DIR"/*
rm -f "$MAP_FILE" "$ERROR_LOG"

# 查找测试目录下的所有 .ipynb 文件（模拟 CI 中的 VALID_CHANGED_IPYNB）
VALID_CHANGED_IPYNB=$(find "$TEST_IPYNB_DIR" -type f -name "*.ipynb" ! -path "*/.git/*" | grep -v '^$')

# 无文件则退出
if [ -z "$VALID_CHANGED_IPYNB" ]; then
  echo "ℹ️  No .ipynb files found in $TEST_IPYNB_DIR"
  exit 0
fi

# 遍历文件提取 markdown
while IFS= read -r nb_file; do
  # 基础校验
  if [ -z "$nb_file" ] || [ ! -f "$nb_file" ] || [ ! -s "$nb_file" ]; then
    echo "ℹ️  Skip invalid file: $nb_file" >> "$ERROR_LOG"
    continue
  fi

  # 生成目标 MD 路径
  nb_relpath="${nb_file#./}"
  md_file="$TARGET_DIR/${nb_relpath%.ipynb}.md"
  mkdir -p "$(dirname "$md_file")"
  > "$md_file"

  # JQ 极简提取（带最大容错）
  markdown_content=$(jq -r '
  try (
      .cells | to_entries[] |  # 把数组转成 {key: 索引, value: 单元格}
      select(.value.cell_type == "markdown") |
      # 加 cell 索引标记（后续 Shell 解析用）
      "<!-- CELL_IDX: \(.key) -->\n" +
      (.value.source | if type == "array" then join("") else tostring end)
  ) catch ""
  ' "$nb_file" 2>> "$ERROR_LOG")

  # 无内容则跳过
  if [ -z "$markdown_content" ]; then
    echo "ℹ️  No markdown content: $nb_file" >> "$ERROR_LOG"
    rm -f "$md_file"
    continue
  fi

  # 写入 MD 文件
  echo "$markdown_content" > "$md_file"

  # 纯 Shell 生成映射表
  md_line=0
  cell_idx=0  # 默认值
  while IFS= read -r line; do
    md_line=$((md_line + 1))

    # 修复：不用 =~ 正则，改用 grep + cut 解析 cell 索引标记（兼容所有 Shell）
    if echo "$line" | grep -q '<!-- CELL_IDX: [0-9]\+ -->'; then
      # 提取数字索引（cut 按冒号/空格分割，取第4个字段）
      cell_idx=$(echo "$line" | cut -d ':' -f 2 | cut -d ' ' -f 2)
      # 标记行不写入映射表
      continue
    fi

    # 写入映射表（用真实的 cell 索引）
    echo "$nb_file,$cell_idx,$md_file,$md_line" >> "$MAP_FILE"
  done < "$md_file"

  echo "✅ Extracted: $nb_file → $md_file"
done <<< "$VALID_CHANGED_IPYNB"

# ===================== 测试结果验证 =====================
echo -e "\n======================================"
echo "===== 本地测试结果 ====="
echo "📁 提取的 MD 文件目录: $TARGET_DIR"
echo "📄 映射表文件: $MAP_FILE (行数: $(wc -l < "$MAP_FILE" 2>/dev/null || echo 0))"
echo "❌ 错误日志: $ERROR_LOG"
if [ -s "$ERROR_LOG" ]; then
  echo -e "\n错误详情:"
  cat "$ERROR_LOG"
else
  echo -e "\n✅ 无提取错误"
fi
echo "======================================"

# 可选：列出提取的 MD 文件
echo -e "\n提取的 MD 文件列表:"
ls -l "$TARGET_DIR"/*.md 2>/dev/null || echo "  无有效 MD 文件"