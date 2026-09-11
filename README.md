# 记账小工具 (Personal Bookkeeping Tool)

一个轻量级的 Python 命令行记账工具，支持记录收入/支出、查看流水、统计汇总、分类管理。

## 功能

- ✅ 添加收入/支出记录
- ✅ 查看所有流水记录
- ✅ 按月份/分类统计
- ✅ 删除记录
- ✅ 数据持久化（JSON 存储）
- ✅ 导出 CSV

## 安装

```bash
cd bookkeeping
pip install -r requirements.txt
```

## 使用

```bash
# 添加一笔支出
python main.py add --type expense --amount 25.5 --category 餐饮 --remark 午饭

# 添加一笔收入
python main.py add --type income --amount 8000 --category 工资 --remark 月薪

# 查看所有记录
python main.py list

# 查看统计汇总
python main.py summary

# 按月份统计
python main.py summary --month 2026-09

# 删除记录
python main.py delete --id 3

# 导出 CSV
python main.py export --output records.csv
```

## 技术栈

- Python 3.8+
- 无外部依赖（标准库实现）

## License

MIT
