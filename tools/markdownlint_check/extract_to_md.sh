# 1. 配置文件路径
NB_FILE="./llm/t5/finetune_t5_daily_email_summarization.ipynb"
MD_FILE="./finetune_t5_daily_email_summarization.md"

# 2. 核心命令：单空行分隔 + 冗余空白清理
echo "===== 开始生成规范 .md 文件（单空行分隔）====="
jq -r '
  # 平铺式提取核心内容（保留可行逻辑）
  .cells[]
  | select(.cell_type == "markdown")
  | .source
  | map(select(. != ""))  # 过滤纯空字符串
  | join("")  # 拼接单元格内部内容，保留原始有效格式
' "$NB_FILE" | \
  awk '
    # 核心优化1：单元格之间仅用 1 个空行分隔（而非 2 个）
    NF > 0 {
      # 清理行首/行尾冗余空格、制表符（解决单个单元格内的多余空格）
      gsub(/^[ \t]+/, "");
      gsub(/[ \t]+$/, "");
      # 打印当前单元格内容 + 1 个换行（实现单空行分隔）
      print $0;
      # 单元格之间添加 1 个空行（后续用 sed 去重末尾空行）
      print "";
    }
  ' | \
  sed -e '$ d' -e '/^$/N;/^\n$/D' |  # 核心优化2：清理多余空行（保留单个空行，删除连续空行）
  tee "$MD_FILE" > /dev/null && \
  sync "$MD_FILE"

# 3. 验证生成结果
echo "===== 规范 .md 文件生成结果验证 ====="
if [ -f "$MD_FILE" ]; then
  echo "✅ 规范 .md 文件已成功创建！"
  echo "📂 文件路径：$(realpath "$MD_FILE" 2>/dev/null || echo "$MD_FILE")"
  echo "📊 文件大小：$(wc -c < "$MD_FILE") 字节"
  echo -e "\n===== .md 文件内容片段（前 20 行）====="
  head -20 "$MD_FILE"
else
  echo "❌ 规范 .md 文件生成失败"
  exit 1
fi