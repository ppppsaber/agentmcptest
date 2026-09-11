#!/usr/bin/env python3
"""记账小工具 - 个人收支管理 CLI"""

import argparse
import json
import os
import csv
from datetime import datetime
from collections import defaultdict

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")


def load_data():
    """加载记账数据"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"records": [], "next_id": 1}


def save_data(data):
    """保存记账数据"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_record(args):
    """添加一条记录"""
    data = load_data()
    record = {
        "id": data["next_id"],
        "type": args.type,
        "amount": round(args.amount, 2),
        "category": args.category,
        "remark": args.remark or "",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    data["records"].append(record)
    data["next_id"] += 1
    save_data(data)
    print(f"✅ 记录已添加 [ID:{record['id']}] {record['type']} ¥{record['amount']} {record['category']} {record['remark']}")


def list_records(args):
    """列出所有记录"""
    data = load_data()
    records = data["records"]
    if not records:
        print("📭 暂无记录")
        return

    # 过滤
    if args.type:
        records = [r for r in records if r["type"] == args.type]
    if args.category:
        records = [r for r in records if r["category"] == args.category]

    print(f"\n{'ID':>4}  {'类型':<6}  {'金额':>10}  {'分类':<8}  {'备注':<12}  {'日期'}")
    print("-" * 70)
    for r in records:
        type_label = "💰收入" if r["type"] == "income" else "💸支出"
        print(f"{r['id']:>4}  {type_label}  ¥{r['amount']:>9.2f}  {r['category']:<8}  {r['remark']:<12}  {r['date']}")
    print(f"\n共 {len(records)} 条记录")


def summary_records(args):
    """统计汇总"""
    data = load_data()
    records = data["records"]
    if not records:
        print("📭 暂无记录")
        return

    if args.month:
        records = [r for r in records if r["date"].startswith(args.month)]
        if not records:
            print(f"📭 {args.month} 无记录")
            return

    total_income = sum(r["amount"] for r in records if r["type"] == "income")
    total_expense = sum(r["amount"] for r in records if r["type"] == "expense")
    balance = total_income - total_expense

    print("\n📊 === 统计汇总 ===")
    if args.month:
        print(f"   月份: {args.month}")
    print(f"   💰 总收入:  ¥{total_income:.2f}")
    print(f"   💸 总支出:  ¥{total_expense:.2f}")
    print(f"   📈 净余额:  ¥{balance:.2f}")
    print(f"   📝 记录数:  {len(records)} 条")

    # 按分类统计
    cat_stats = defaultdict(lambda: {"income": 0, "expense": 0})
    for r in records:
        cat_stats[r["category"]][r["type"]] += r["amount"]

    print("\n   📁 分类明细:")
    for cat, vals in sorted(cat_stats.items()):
        parts = []
        if vals["income"]:
            parts.append(f"收入 ¥{vals['income']:.2f}")
        if vals["expense"]:
            parts.append(f"支出 ¥{vals['expense']:.2f}")
        print(f"     {cat}: {', '.join(parts)}")
    print()


def delete_record(args):
    """删除一条记录"""
    data = load_data()
    found = False
    for i, r in enumerate(data["records"]):
        if r["id"] == args.id:
            data["records"].pop(i)
            save_data(data)
            print(f"✅ 已删除记录 [ID:{args.id}] {r['type']} ¥{r['amount']} {r['category']}")
            found = True
            break
    if not found:
        print(f"❌ 未找到 ID:{args.id} 的记录")


def export_csv(args):
    """导出 CSV"""
    data = load_data()
    records = data["records"]
    if not records:
        print("📭 暂无记录可导出")
        return

    output = args.output or "records.csv"
    with open(output, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "type", "amount", "category", "remark", "date"])
        writer.writeheader()
        writer.writerows(records)
    print(f"✅ 已导出 {len(records)} 条记录到 {output}")


def main():
    parser = argparse.ArgumentParser(description="📝 记账小工具 - 个人收支管理")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # add
    p_add = subparsers.add_parser("add", help="添加一条记录")
    p_add.add_argument("--type", choices=["income", "expense"], required=True, help="类型: income/expense")
    p_add.add_argument("--amount", type=float, required=True, help="金额")
    p_add.add_argument("--category", default="其他", help="分类")
    p_add.add_argument("--remark", help="备注")
    p_add.set_defaults(func=add_record)

    # list
    p_list = subparsers.add_parser("list", help="查看所有记录")
    p_list.add_argument("--type", choices=["income", "expense"], help="过滤类型")
    p_list.add_argument("--category", help="过滤分类")
    p_list.set_defaults(func=list_records)

    # summary
    p_sum = subparsers.add_parser("summary", help="统计汇总")
    p_sum.add_argument("--month", help="按月份过滤，如 2026-09")
    p_sum.set_defaults(func=summary_records)

    # delete
    p_del = subparsers.add_parser("delete", help="删除一条记录")
    p_del.add_argument("--id", type=int, required=True, help="记录 ID")
    p_del.set_defaults(func=delete_record)

    # export
    p_exp = subparsers.add_parser("export", help="导出 CSV")
    p_exp.add_argument("--output", help="输出文件名")
    p_exp.set_defaults(func=export_csv)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return
    args.func(args)


if __name__ == "__main__":
    main()
