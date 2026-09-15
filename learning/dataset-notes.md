# 数据集选择记录

> 记录时间：2026-09-15（阶段 0）

## 选定数据集

- **名称**：item_detail.csv（前程无忧 51job 数据分析相关岗位）
- **来源**：GitHub 仓库 [trouver/crawl-job-information-and-analyze](https://github.com/trouver/crawl-job-information-and-analyze)
- **文件位置**：`data/raw/item_detail.csv`（9.3MB）
- **下载日期**：2026-09-15

### 数据概况

| 项目 | 值 |
|------|-----|
| 行数 | 6555 |
| 列数 | 15 |
| JD 文本字段 | `job_detail`（无缺失）✅ |
| 薪资字段 | `salary(k/m)`（千/月，数值型）✅ |
| 其他关键字段 | 城市 `job_loc_city`、学历 `edu`、经验 `job_exp`、公司 `company_name`、福利 `welfare` |
| 发布时间范围 | 2019 年 |

### 对照筛选标准（规格第 11 节）

1. 有 JD 文本字段 ✅（job_detail，0 缺失）
2. 有薪资字段 ✅（salary(k/m)，均值 8.9k）
3. 数据量 1000+ ✅（6555 条）
4. 近 3 年内 ❌（2019 年数据，距今 7 年——作为学习项目可接受，但**分析结论不用于真实求职决策**）
5. 备选 ≥ 2 ✅（备选见下）

### 已知缺陷（分析阶段需处理）

- **城市分布极度集中**：成都 6283 条（96%），其他城市样本极少 → 城市维度分析降级，改用岗位类型/学历/经验维度
- **岗位类型混杂**：爬取关键词是"数据分析"，但混入产品经理(48)、运营专员(43)、新媒体运营等岗位 → 分析前需按 `func_cat`/`job_name` 过滤出数据类岗位
- **薪资有 0 值**：min=0 → 清洗阶段需处理

## 备选数据集（已查看，弃用原因）

| 数据集 | 来源 | 弃用原因 |
|--------|------|---------|
| merged_后端开发.xlsx（5399 条，BOSS 直聘，近年数据） | [poboll/bosszhipin_spider](https://github.com/poboll/bosszhipin_spider) | **无 JD 文本字段**（只有"技能要求"），无法做 LLM 抽取——不满足规格硬标准 |
| 51job-spider-and-data-analysis（3.3 万条，2019） | [yueningbo/51job-spider-and-data-analysis](https://github.com/yueningbo/51job-spider-and-data-analysis) | 仓库内无现成数据文件（仅爬虫代码） |
| city.csv（BOSS 城市代码表） | [brandonchow1997/bosszhipin_spider](https://github.com/brandonchow1997/bosszhipin_spider) | 只是城市代码映射表，非岗位数据 |
