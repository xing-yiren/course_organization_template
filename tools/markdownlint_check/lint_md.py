#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path

# 配置项（可根据需求调整）
LINT_DIR = "./temp_md"  # MD文件根目录
MAP_FILE = "./md_ipynb_mapping.log"
LINT_ERROR_LOG = "./markdownlint_error.log"
# 自定义规则开关
CHECK_TITLE_BLANK_LINES = True  # 标题前后空行检查
CHECK_CONSECUTIVE_BLANKS = True  # 连续空行检查
MAX_CONSECUTIVE_BLANKS = 1  # 允许的最大连续空行数
CHECK_TITLE_LEVEL = False  # 可选：标题层级检查（如H1之后必须是H2）

def load_mapping_table(map_file):
    """加载行号映射表：{ (md_file, md_line): (ipynb_file, cell_idx) }"""
    mapping = {}
    if not os.path.exists(map_file):
        print(f"❌ 错误：未找到映射表 {map_file}")
        print("👉 请先执行：./extract_md_and_map.sh")
        sys.exit(1)

    with open(map_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) != 4:
                continue
            ipynb_file, cell_idx, md_file, md_line = parts
            # 存储绝对路径和相对路径两种格式，提高匹配率
            md_file_abs = os.path.abspath(md_file.strip())
            md_file_rel = os.path.relpath(md_file_abs)
            mapping[(md_file_abs, md_line.strip())] = (ipynb_file.strip(), cell_idx.strip())
            mapping[(md_file_rel, md_line.strip())] = (ipynb_file.strip(), cell_idx.strip())
    return mapping

def find_all_md_files(root_dir):
    """递归查找所有MD文件"""
    md_files = []
    if not os.path.exists(root_dir):
        print(f"❌ 错误：临时MD目录不存在 → {root_dir}")
        sys.exit(1)

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".md"):
                md_file_abs = os.path.abspath(os.path.join(root, file))
                md_files.append(md_file_abs)

    if not md_files:
        print(f"ℹ️  在目录 {root_dir} 中未找到任何.md文件")
        print("📂 目录内容：")
        for item in os.listdir(root_dir):
            print(f"  - {item}")
    else:
        print(f"ℹ️  找到 {len(md_files)} 个待校验的MD文件")
    return md_files

def check_title_blank_lines(md_file):
    """
    自定义规则1：标题必须被空行包围（MD022）
    规则：
    - 一级标题（#）前后必须有空行（文件首行/末行除外）
    - 其他标题（##/###等）前后必须有空行
    """
    errors = []
    with open(md_file, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]  # 保留换行符外的所有字符

    line_count = len(lines)
    for idx, line in enumerate(lines):
        line_num = idx + 1
        stripped_line = line.strip()

        # 匹配标题行（# 开头，且#后有空格）
        if stripped_line.startswith("#") and len(stripped_line) > 1 and stripped_line[1] in [" ", "\t"]:
            title_level = len(stripped_line) - len(stripped_line.lstrip("#"))
            is_first_line = (idx == 0)
            is_last_line = (idx == line_count - 1)

            # 检查标题上方空行
            if not is_first_line:
                prev_line = lines[idx-1].rstrip("\n")
                if prev_line.strip() != "":
                    errors.append({
                        "md_file": md_file,
                        "md_line": str(line_num),
                        "error_msg": f"MD022 标题（H{title_level}）上方缺少空行"
                    })

            # 检查标题下方空行
            if not is_last_line:
                next_line = lines[idx+1].rstrip("\n")
                if next_line.strip() != "":
                    errors.append({
                        "md_file": md_file,
                        "md_line": str(line_num),
                        "error_msg": f"MD022 标题（H{title_level}）下方缺少空行"
                    })
    return errors

def check_consecutive_blank_lines(md_file):
    """
    自定义规则2：禁止连续空行（MD019）
    规则：最多允许MAX_CONSECUTIVE_BLANKS个连续空行
    """
    errors = []
    with open(md_file, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    blank_count = 0
    for idx, line in enumerate(lines):
        line_num = idx + 1
        stripped_line = line.strip()

        if stripped_line == "":
            blank_count += 1
            # 超过最大允许数
            if blank_count > MAX_CONSECUTIVE_BLANKS:
                errors.append({
                    "md_file": md_file,
                    "md_line": str(line_num),
                    "error_msg": f"MD019 连续空行数超过限制（最多{MAX_CONSECUTIVE_BLANKS}行）"
                })
        else:
            blank_count = 0
    return errors

def run_custom_checks(md_file):
    """执行所有自定义规则检查"""
    errors = []

    # 规则1：标题前后空行
    if CHECK_TITLE_BLANK_LINES:
        errors.extend(check_title_blank_lines(md_file))

    # 规则2：连续空行检查
    if CHECK_CONSECUTIVE_BLANKS:
        errors.extend(check_consecutive_blank_lines(md_file))

    # 可扩展其他规则（如标题层级、禁止行尾空格等）
    return errors

def run_mdformat_checks(md_files):
    """执行mdformat基础语法校验"""
    errors = []
    if not md_files:
        return errors

    print("\nℹ️  执行基础markdown语法校验...")
    for md_file in md_files:
        cmd = f"mdformat --check '{md_file}' 2>> '{LINT_ERROR_LOG}'"
        exit_code = os.system(cmd)
        if exit_code != 0:
            with open(LINT_ERROR_LOG, "r", encoding="utf-8") as f:
                log_content = f.read()
                # 匹配mdformat错误格式
                pattern1 = re.compile(r"(.+):([0-9]+):([0-9]+): (.+)")
                pattern2 = re.compile(r"error: (.+) at (.+) line ([0-9]+) column ([0-9]+)")

                matches1 = pattern1.findall(log_content)
                for match in matches1:
                    errors.append({
                        "md_file": os.path.abspath(match[0]),
                        "md_line": match[1],
                        "error_msg": match[3]
                    })

                matches2 = pattern2.findall(log_content)
                for match in matches2:
                    errors.append({
                        "md_file": os.path.abspath(match[1]),
                        "md_line": match[2],
                        "error_msg": f"语法错误：{match[0]}"
                    })

        # 执行自定义规则检查
        print(f"ℹ️  执行自定义规则校验 → {os.path.relpath(md_file)}")
        custom_errors = run_custom_checks(md_file)
        errors.extend(custom_errors)

    # 清空错误日志
    open(LINT_ERROR_LOG, "w", encoding="utf-8").close()
    return errors

def trace_errors(errors, mapping):
    """溯源错误到原.ipynb文件的cell编号"""
    if not errors:
        print("\n✅ 恭喜！所有markdown校验规则通过！")
        if os.path.exists(LINT_ERROR_LOG):
            os.remove(LINT_ERROR_LOG)
        return

    # 去重（同一行的同一错误只显示一次）
    unique_errors = []
    seen = set()
    for err in errors:
        key = (err["md_file"], err["md_line"], err["error_msg"])
        if key not in seen:
            seen.add(key)
            unique_errors.append(err)

    print("\n❌ 检测到markdown校验错误：")
    print("-" * 70)
    for err in unique_errors:
        md_file = err["md_file"]
        md_line = err["md_line"]
        error_msg = err["error_msg"]

        # 查找映射表
        key_abs = (os.path.abspath(md_file), md_line)
        key_rel = (os.path.relpath(md_file), md_line)
        ipynb_file = "未匹配到"
        cell_idx = "未知"

        if key_abs in mapping:
            ipynb_file, cell_idx = mapping[key_abs]
        elif key_rel in mapping:
            ipynb_file, cell_idx = mapping[key_rel]

        print(f"🔍 报错位置：")
        print(f"  MD文件：{os.path.relpath(md_file)} (行：{md_line})")
        print(f"  原IPYNB：{ipynb_file} (Markdown单元格：{cell_idx})")
        print(f"  错误类型：{error_msg}")
        print("-" * 70)
    print(f"❌ 校验失败！共检测到 {len(unique_errors)} 个唯一错误，请修复后重试。")

def main():
    print("=" * 70)
    print("📝 Markdown 精细化校验 + 溯源工具（支持自定义规则）")
    print("=" * 70)
    print(f"⚙️  启用的规则：")
    if CHECK_TITLE_BLANK_LINES:
        print(f"  - 标题必须被空行包围（MD022）")
    if CHECK_CONSECUTIVE_BLANKS:
        print(f"  - 连续空行数≤{MAX_CONSECUTIVE_BLANKS}（MD019）")
    print("=" * 70)

    # 1. 加载映射表
    print("\nℹ️  加载行号映射表...")
    mapping = load_mapping_table(MAP_FILE)

    # 2. 查找所有MD文件
    print("\nℹ️  查找临时MD文件...")
    md_files = find_all_md_files(LINT_DIR)

    # 3. 执行所有校验
    all_errors = run_mdformat_checks(md_files)

    # 4. 溯源并输出错误
    trace_errors(all_errors, mapping)

    # 5. 最终提示
    print("\n" + "=" * 70)
    if os.path.exists(LINT_ERROR_LOG) and os.path.getsize(LINT_ERROR_LOG) > 0:
        print(f"📄 错误日志文件：{LINT_ERROR_LOG}")
    else:
        print(f"📄 错误日志文件：无（校验通过）")
    print("=" * 70)

    # 有错误则退出非0状态码（适配CI）
    if all_errors:
        sys.exit(1)

if __name__ == "__main__":
    main()