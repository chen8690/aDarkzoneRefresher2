"""生成本 skill 自带的示例规则表 rules_sample.xlsx（Sheet1）。

内容与真机使用的「工作簿1.xlsx」结构一致，但只保留一组示例数据，供离线冒烟测试
（--image 模式）或其它 AI 在无真机/无真实规则表时快速验证脚本能跑通。

真实规则表照常指出你自己的 Excel 文件即可（`--rules 路径`）。规则表结构约定见
references/rules-table.md。

用法（在本 skill 根目录）：
    python scripts/make_sample_rules.py
"""

import openpyxl

OUT = "rules_sample.xlsx"

# 表头行：A=类别，B=触发时机，C/D/E=第一/二/三行装备选择（池列表头）
HEADER = ["暗区首领", "验证完暗区首领后", "第一行装备选择", "第二行装备选择", "第三行装备选择"]

# 数据行：A=限定条件（「除了…」即排除名单），C/D/E=对应槽位的可选装备池
ROWS = [
    ["除了阿贾克斯和雷诺伊尔", "", "AUG突击步枪", "BT101战术防弹衣", "钢铁新星战术头盔"],
    ["", "", "SJ16栓动步枪", "治安官重型防弹衣", "野战登山背包"],
    ["", "", "AR30栓动步枪", "KN复合防弹衣", "RAL重型军用背包"],
    ["", "", "A545突击步枪", "AL指挥官弹挂甲", ""],
    ["", "", "MK14射手步枪", "", ""],
]


def main():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    ws.append(HEADER)
    for r in ROWS:
        ws.append(r)
    wb.save(OUT)
    print(f"[OK] 已生成 {OUT}（{len(ROWS)} 个数据行，3 个槽位池）")


if __name__ == "__main__":
    main()