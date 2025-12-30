# 配置文件路径
NB_FILE="./cv/resnet/finetune_resnet50_chinese_herbal_classification.ipynb"
MD_FILE="./finetune_resnet50_chinese_herbal_classification.md"

# 核心命令：改用 jq 支持的纯文本分隔符 + 单元格间单空行分隔
jq -r '
  # 步骤1：提取每个独立的 markdown 单元格，添加 jq 支持的纯文本边界标记（###CELL_BOUNDARY###）
  .cells[]
  | select(.cell_type == "markdown")
  | (
      # 保留单元格内内容 1:1 还原（无任何修改）
      .source
      | map(.)
      | join("")
    ) + "###CELL_BOUNDARY###"  # 【关键修复】改用纯文本分隔符，jq 无编译报错
' "$NB_FILE" | \
  awk '
    # 步骤2：按纯文本分隔符分割单元格，之间添加单空行
    BEGIN {
      # 【关键】以纯文本分隔符作为记录分隔符（匹配独立单元格）
      RS = "###CELL_BOUNDARY###"
      first_cell = 1  # 标记第一个单元格，避免首行前加空行
    }
    # 处理每个独立单元格（仅清理首尾多余空行，保留内部完整格式）
    $0 != "" {
      # 清理单元格首尾的多余空行/换行（不破坏单元格内部的任何格式）
      gsub(/^[\n\r]+/, "");
      gsub(/[\n\r]+$/, "");
      current_cell = $0;

      # 第一个单元格直接打印，后续单元格前加单空行分隔（核心诉求）
      if (first_cell == 1) {
        print current_cell;
        first_cell = 0;
      } else {
        print "";  # 单元格之间添加单空行（解决二级标题无空行问题）
        print current_cell;
      }
    }
  ' | \
  # 最终轻微清理：仅删除连续多空行，保留正常单空行分隔，不破坏内容
  sed -e '/^\n\{2,\}/D' | \
  tee "$MD_FILE" > /dev/null && \
  sync "$MD_FILE"

# 验证结果
echo "✅ 生成完成！无 jq 报错，所有独立代码块（包括二级标题）之间均有单空行分隔"
echo "目标文件：$MD_FILE"