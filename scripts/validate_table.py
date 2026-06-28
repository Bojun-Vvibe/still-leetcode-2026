#!/usr/bin/env python3
"""校验 README.md「📊 公司清单」表格格式。

无第三方依赖，可直接 `python3 scripts/validate_table.py` 本地运行，
也用于 GitHub Action。校验失败时退出码非 0，并打印所有问题。
"""
import re
import sys
from pathlib import Path

README = Path(__file__).resolve().parent.parent / "README.md"

SECTION_PREFIX = "## 📊 公司清单"
STATUS_TOKENS = {"✅", "🟡", "❌", "❓"}
DATE_RE = re.compile(r"^\d{4}-\d{2}$")
EXPECTED_COLS = 7
COL_NAMES = ["公司", "是否面 LC", "面试形式", "难度", "AI 工具政策", "信息来源", "更新时间"]


def split_row(line: str):
    """把 `| a | b |` 拆成 ['a', 'b']，去掉首尾空单元。"""
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return cells


def is_separator(cells):
    return all(set(c) <= set("-: ") and c for c in cells)


def main() -> int:
    if not README.exists():
        print(f"❌ 找不到 {README}")
        return 1

    lines = README.read_text(encoding="utf-8").splitlines()

    # 定位「公司清单」章节
    try:
        start = next(i for i, l in enumerate(lines) if l.strip().startswith(SECTION_PREFIX))
    except StopIteration:
        print(f"❌ 找不到章节标题：{SECTION_PREFIX}")
        return 1

    # 收集该章节内的表格行（到下一个 ## 标题为止）
    table_rows = []
    for idx in range(start + 1, len(lines)):
        line = lines[idx]
        if line.startswith("## "):
            break
        if line.strip().startswith("|"):
            table_rows.append((idx + 1, line))  # 1-based 行号

    if len(table_rows) < 3:
        print("❌ 公司清单表格行数过少（至少需表头 + 分隔行 + 1 行数据）。")
        return 1

    errors = []
    data_rows = 0
    for lineno, line in table_rows:
        cells = split_row(line)
        if is_separator(cells):
            continue
        # 表头：与预期列名一致则跳过
        if cells == COL_NAMES:
            continue
        # 其余视为数据行
        data_rows += 1
        prefix = f"  README.md:{lineno}"

        if len(cells) != EXPECTED_COLS:
            errors.append(f"{prefix} 列数为 {len(cells)}，应为 {EXPECTED_COLS}：{line.strip()}")
            continue

        company, asks, fmt, diff, ai, source, date = cells

        if not company:
            errors.append(f"{prefix} 公司名为空")
        if not any(tok in asks for tok in STATUS_TOKENS):
            errors.append(f"{prefix} 「是否面 LC」缺少 ✅/🟡/❌/❓ 之一，实际：{asks!r}")
        if not fmt:
            errors.append(f"{prefix} 「面试形式」为空")
        if not ai:
            errors.append(f"{prefix} 「AI 工具政策」为空（未知请填「未知」）")
        if not source:
            errors.append(f"{prefix} 「信息来源」为空")
        if not DATE_RE.match(date):
            errors.append(f"{prefix} 「更新时间」应为 YYYY-MM 格式，实际：{date!r}")

    if errors:
        print(f"❌ 表格校验失败，发现 {len(errors)} 个问题：\n")
        print("\n".join(errors))
        print("\n字段说明见 CONTRIBUTING.md。")
        return 1

    print(f"✅ 表格校验通过，共 {data_rows} 行数据。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
