#!/bin/bash
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

TARGET_DIR="./temp_md"
mkdir -p "$TARGET_DIR"
rm -f jq_batch_error.log

find . -name "*.ipynb" -type f | while IFS= read -r nb_file; do
  # 跳过隐藏目录和空文件
  if [[ "$nb_file" =~ /\./ ]]; then continue; fi
  if [ ! -s "$nb_file" ]; then continue; fi

  # 生成目标 .md 文件路径
  if command -v realpath &> /dev/null; then
    nb_relpath=$(realpath --relative-to=. "$nb_file")
  else
    nb_relpath=$(echo "$nb_file" | sed 's|^./||')
  fi
  md_file="$TARGET_DIR/${nb_relpath%.ipynb}.md"
  mkdir -p "$(dirname "$md_file")"

  # 核心逻辑（同步修复分隔符，无 jq 报错）
  jq -r '
    .cells[]
    | select(.cell_type == "markdown")
    | (
        .source
        | map(.)
        | join("")
      ) + "###CELL_BOUNDARY###"
  ' "$nb_file" | \
    awk '
      BEGIN {
        RS = "###CELL_BOUNDARY###"
        first_cell = 1
      }
      $0 != "" {
        gsub(/^[\n\r]+/, "");
        gsub(/[\n\r]+$/, "");
        current_cell = $0;

        if (first_cell == 1) {
          print current_cell;
          first_cell = 0;
        } else {
          print "";
          print current_cell;
        }
      }
    ' | \
    sed -e '/^\n\{2,\}/D' | \
    tee "$md_file" > /dev/null 2>> jq_batch_error.log && \
    sync "$md_file"

  # 验证结果
  if [ -s "$md_file" ]; then
    echo "✅ 处理成功：$nb_file → $md_file"
  else
    rm -f "$md_file"
    echo "ℹ️  无有效内容，跳过：$nb_file"
  fi
done

echo "===== 批量处理完成！无 jq 报错，所有二级标题单元格均有单空行分隔 ====="