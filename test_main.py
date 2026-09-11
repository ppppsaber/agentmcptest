# 记账小工具测试
# 运行: python -m pytest test_main.py

import subprocess
import json
import os
import sys

MAIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")


def run_cmd(*args):
    """运行 main.py 命令"""
    result = subprocess.run([sys.executable, MAIN] + list(args), capture_output=True, text=True)
    return result.stdout + result.stderr


def setup_function(func):
    """每个测试前清理数据"""
    if os.path.exists(DATA):
        os.remove(DATA)


def test_add_expense():
    """测试添加支出"""
    out = run_cmd("add", "--type", "expense", "--amount", "25.5", "--category", "餐饮", "--remark", "午饭")
    assert "✅" in out
    assert "25.50" in out
    assert "餐饮" in out


def test_add_income():
    """测试添加收入"""
    out = run_cmd("add", "--type", "income", "--amount", "8000", "--category", "工资", "--remark", "月薪")
    assert "✅" in out
    assert "8000.00" in out


def test_list_records():
    """测试列出记录"""
    run_cmd("add", "--type", "expense", "--amount", "10", "--category", "交通")
    run_cmd("add", "--type", "income", "--amount", "5000", "--category", "工资")
    out = run_cmd("list")
    assert "2 条记录" in out


def test_summary():
    """测试统计汇总"""
    run_cmd("add", "--type", "income", "--amount", "10000", "--category", "工资")
    run_cmd("add", "--type", "expense", "--amount", "3000", "--category", "房租")
    run_cmd("add", "--type", "expense", "--amount", "500", "--category", "餐饮")
    out = run_cmd("summary")
    assert "10000.00" in out
    assert "3500.00" in out
    assert "6500.00" in out  # 净余额


def test_delete():
    """测试删除记录"""
    run_cmd("add", "--type", "expense", "--amount", "10", "--category", "测试")
    out = run_cmd("delete", "--id", "1")
    assert "✅" in out
    # 验证已删除
    out = run_cmd("list")
    assert "暂无记录" in out


def test_export_csv():
    """测试导出 CSV"""
    run_cmd("add", "--type", "expense", "--amount", "10", "--category", "测试")
    output_file = os.path.join(os.path.dirname(DATA), "test_export.csv")
    out = run_cmd("export", "--output", output_file)
    assert "✅" in out
    assert os.path.exists(output_file)
    os.remove(output_file)


def test_persistence():
    """测试数据持久化"""
    run_cmd("add", "--type", "expense", "--amount", "42", "--category", "测试")
    # 数据文件应该存在
    assert os.path.exists(DATA)
    with open(DATA, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data["records"]) == 1
    assert data["records"][0]["amount"] == 42.0
