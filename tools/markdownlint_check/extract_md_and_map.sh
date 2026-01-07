#!/bin/bash
# extract_md_and_map.sh - 最终版（解决cell: null+零报错）
set -euo pipefail

# 1. 环境与目录初始化
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
TARGET_DIR="./temp_md"
MAP_FILE="./md_ipynb_mapping.log"
ERROR_LOG="./jq_batch_error.log"

mkdir -p "$TARGET_DIR"
rm -f "$MAP_FILE" "$ERROR_LOG" temp_extract.tmp

# 2. 检查依赖文件
if [ ! -f "valid_ipynb.txt" ]; then
  echo "❌ 请先创建 valid_ipynb.txt，写入待处理的.ipynb路径（每行一个）"
  exit 1
fi
VALID_CHANGED_IPYNB=$(cat valid_ipynb.txt)

# 3. 遍历处理每个.ipynb文件
while IFS= read -r nb_file; do
  # 跳过空行/无效文件
  if [ -z "$nb_file" ] || [ ! -f "$nb_file" ] || [ ! -s "$nb_file" ]; then
    echo "ℹ️  跳过无效文件：$nb_file"
    continue
  fi

  # 生成临时MD文件路径
  nb_relpath=$(echo "$nb_file" | sed 's|^./||')
  md_file="$TARGET_DIR/${nb_relpath%.ipynb}.md"
  mkdir -p "$(dirname "$md_file")"
  > "$md_file"  # 先创建空文件

  # ===================== 核心修复：自动生成cell序号（解决null） =====================
  # 用jq的foreach遍历，自动生成从0开始的markdown单元格序号
  jq -r --arg nb_relpath "$nb_relpath" '
    # 遍历所有markdown单元格，生成自增序号
    foreach (.cells[] | select(.cell_type == "markdown")) as $cell (
      0;  # 初始序号为0
      . + 1;  # 每遍历一个单元格，序号+1
      # 拼接注释（序号-1，因为初始是0，+1后要还原）
      "<!-- ORIGIN: \($nb_relpath) (cell: \(. - 1)) -->\n" +
      (
        $cell.source
        | if type == "array" then map(.) | join("") else . end
      ) + "\n<!-- CELL_BOUNDARY -->"
    )
  ' "$nb_file" > temp_extract.tmp 2>> "$ERROR_LOG"

  # 检查jq执行结果
  if [ $? -ne 0 ]; then
    echo "⚠️  jq处理失败：$nb_file（查看错误日志：$ERROR_LOG）"
    rm -f temp_extract.tmp "$md_file"
    continue
  fi

  # ===================== awk处理（匹配HTML注释，无语法错误） =====================
  awk -v nb_file="$nb_file" -v map_file="$MAP_FILE" -v md_file="$md_file" '
    BEGIN {
      # 用HTML注释作为分隔符（注释单独成行，零语法风险）
      RS = "<!-- CELL_BOUNDARY -->"
      first_cell = 1
      md_line = 0
      cell_idx = 0
    }
    $0 != "" {
      # 清理首尾空行
      gsub(/^[\n\r]+/, "");
      gsub(/[\n\r]+$/, "");
      current_cell = $0;

      # 提取HTML注释中的cell索引（匹配<!-- ORIGIN: ... (cell: N) -->）
      if (current_cell ~ /^<!-- ORIGIN: .* \(cell: [0-9]+\) -->$/) {
        split(current_cell, parts, /\(cell: |\)/);
        cell_idx = parts[2];
        print current_cell >> md_file;  # 写入真注释行
        md_line++;
        next;
      }

      # 写入markdown内容（处理空行分隔）
      if (first_cell == 1) {
        print current_cell >> md_file;
        first_cell = 0;
      } else {
        print "" >> md_file;
        print current_cell >> md_file;
        md_line++;  # 空行占1行
      }

      # 生成行号映射表（临时MD行号 → 原ipynb单元格）
      cell_lines = split(current_cell, lines, "\n");
      for (i=1; i<=cell_lines; i++) {
        md_line++;
        print nb_file "," cell_idx "," md_file "," md_line >> map_file;
      }
    }
  ' temp_extract.tmp

  # 清理临时文件+验证结果
  rm -f temp_extract.tmp
  sync "$md_file"

  if [ -s "$md_file" ]; then
    echo "✅ 处理成功：$nb_file → $md_file"
  else
    rm -f "$md_file"
    echo "ℹ️  无有效MD内容：$nb_file（文件无markdown单元格）"
  fi
done <<< "$VALID_CHANGED_IPYNB"

# 最终提示
echo -e "\n======================================"
echo "✅ 所有文件处理完成！"
echo "📁 临时MD文件目录：$TARGET_DIR"
echo "🗺️  行号映射表：$MAP_FILE"
echo "❌ JQ错误日志：$ERROR_LOG"
echo "======================================"

exit 0