# 阶段 0-1：环境就绪与最小闭环分析 实现计划

> **面向 AI 代理的工作者：** 必需子技能：使用 superpowers:subagent-driven-development（推荐）或 superpowers:executing-plans 逐任务实现此计划。步骤使用复选框（`- [ ]`）语法来跟踪进度。
>
> **执行方式说明：** 本项目是零基础教学项目，每个任务的代码需要用户亲手在 Jupyter 里运行一遍并理解。执行时每完成一个任务，先向用户讲解知识点再继续下一个任务。

**目标：** 完成环境就绪、选定招聘数据集并下载、写出第一个数据概览 notebook 和第一份最小闭环分析（基本统计 + 第一张图）。

**架构：** 数据以 CSV 形式存于 `data/raw/`（不入库），Jupyter notebook 在 `notebooks/` 目录下读取并分析。本阶段不写 src/ 代码，全部逻辑在 notebook 内，边看边学。

**技术栈：** Anaconda Python 3 + Jupyter + pandas + matplotlib

**对应规格：** `docs/superpowers/specs/2026-09-15-job-market-analysis-design.md` 第 5 节（阶段 0、阶段 1）

**学习笔记：** 每个任务涉及的知识点必须实时追加到 `C:\Users\12923\Desktop\数据分析项目学习笔记.md`（规格第 13 节）。

---

### 任务 1：确认环境可用

**文件：**
- 不创建/修改代码文件（验证性质）

- [ ] **步骤 1：确认 Python 与依赖**

运行：
```bash
/c/Users/12923/anaconda3/python --version
/c/Users/12923/anaconda3/python -c "import pandas, matplotlib; print('pandas', pandas.__version__); print('matplotlib', matplotlib.__version__)"
```
预期：Python 版本号；pandas/matplotlib 版本号正常打印，无报错。

- [ ] **步骤 2：确认 Jupyter 可用**

运行：
```bash
/c/Users/12923/anaconda3/python -c "import jupyter; print('jupyter OK')"
```
预期：打印 `jupyter OK`。

- [ ] **步骤 3：缺失依赖则安装**

若步骤 1/2 报 ModuleNotFoundError，运行（哪个缺装哪个）：
```bash
/c/Users/12923/anaconda3/pip install pandas matplotlib jupyter -i https://pypi.tuna.tsinghua.edu.cn/simple
```

- [ ] **步骤 4：Commit（记录环境就绪状态）**

```bash
cd /c/Users/12923/Desktop/job-market-analysis && git commit -m "chore: 确认阶段0环境就绪" --allow-empty
```

### 任务 2：选定并下载数据集

**文件：**
- 创建：`learning/dataset-notes.md`（数据集选择记录，文字说明）
- 数据文件下载到 `data/raw/`（已被 .gitignore 排除，不入库）

- [ ] **步骤 1：搜索候选数据集**

在浏览器打开 GitHub 搜索（需代理）：
```
https://github.com/search?q=%E6%8B%9B%E8%81%98+JD+%E6%95%B0%E6%8D%AE%E9%9B%86&type=repositories
```
备选搜索词：`招聘 数据集 csv`、`拉勾网 数据集`、`前程无忧 数据`、`job posting china dataset csv`

Kaggle 搜索：`https://www.kaggle.com/search?q=china+job+postings`

筛选标准（规格第 11 节）：
1. 有 JD 文本字段（如 job description / 职位描述 / requirements）
2. 有薪资字段
3. 数据量 1000+ 条
4. 近 3 年内（2023 及以后）
5. 至少找到 2 个候选，选字段最全的 1 个下载

- [ ] **步骤 2：下载到 data/raw/**

用浏览器或 curl 下载（GitHub 文件可用 `https://raw.githubusercontent.com/...` 或 release 附件；Kaggle 需登录后下载）。

- [ ] **步骤 3：验证数据文件**

运行（`<文件名>` 换成实际文件名）：
```bash
ls -lh "C:/Users/12923/Desktop/job-market-analysis/data/raw/"
/c/Users/12923/anaconda3/python -c "
import pandas as pd
df = pd.read_csv('C:/Users/12923/Desktop/job-market-analysis/data/raw/<文件名>.csv')
print('行数:', len(df))
print('列名:', list(df.columns))
"
```
预期：能看到文件大小、行数 ≥ 1000、列名列表打印出来。

- [ ] **步骤 4：写数据集选择记录**

创建 `learning/dataset-notes.md`，内容包含：
- 数据集名称、来源链接、下载日期
- 行数、列数、关键字段（JD 文本字段、薪资字段具体叫什么）
- 为什么选它（对照 5 条筛选标准）
- 备选数据集的名称和放弃原因

- [ ] **步骤 5：Commit**

```bash
cd /c/Users/12923/Desktop/job-market-analysis && git add learning/dataset-notes.md && git commit -m "docs: 记录数据集选择与来源"
```

### 任务 3：第一个 notebook — 数据概览

**文件：**
- 创建：`notebooks/01_data_overview.ipynb`

> 执行方式：在项目目录运行 `jupyter notebook` 打开浏览器，新建 notebook 后逐个 cell 输入以下代码并运行。**每运行一个 cell，先看输出、听讲解，再继续下一个 cell。**

- [ ] **步骤 1：启动 Jupyter**

运行：
```bash
cd /c/Users/12923/Desktop/job-market-analysis && /c/Users/12923/anaconda3/python -m jupyter notebook
```
预期：浏览器自动打开 Jupyter 界面。在界面上新建 notebook 并命名为 `01_data_overview`。

- [ ] **步骤 2：Cell 1 — 导入 pandas 并读数据**

```python
# 导入 pandas 库，起别名 pd（数据岗约定俗成的写法）
import pandas as pd

# 读取原始数据（<文件名> 换成任务 2 下载的实际文件名）
df = pd.read_csv('../data/raw/<文件名>.csv')

# 看前 5 行，了解数据长什么样
df.head()
```

- [ ] **步骤 3：Cell 2 — 了解数据规模**

```python
# 数据有多少行、多少列
df.shape
```

- [ ] **步骤 4：Cell 3 — 了解每列的类型和缺失情况**

```python
# 每列的数据类型（object=文本，int64/float64=数字）、非空数量
df.info()
```

- [ ] **步骤 5：Cell 4 — 数值列的基本统计**

```python
# 数值列的描述性统计：均值、最大最小值、分位数
df.describe()
```

- [ ] **步骤 6：运行验证**

预期输出核对：
- `head()` 显示 5 行数据，能看到 JD 文本字段和薪资字段
- `shape` 行数与任务 2 验证一致
- `info()` 无报错
- `describe()` 有统计表输出

- [ ] **步骤 7：更新学习笔记**

在 `C:\Users\12923\Desktop\数据分析项目学习笔记.md` 的「pandas」小节追加（按实际运行情况写）：
```markdown
### 读取数据（阶段0）
- `import pandas as pd`：导入 pandas 并起别名
- `pd.read_csv('路径')`：读取 CSV 文件返回 DataFrame
- `df.head()`：看前 5 行
- `df.shape`：行数×列数
- `df.info()`：每列类型和非空数量
- `df.describe()`：数值列统计
```

- [ ] **步骤 8：Commit**

```bash
cd /c/Users/12923/Desktop/job-market-analysis && git add notebooks/01_data_overview.ipynb && git commit -m "feat: 第一个数据概览 notebook"
```

### 任务 4：最小闭环分析 — 基本统计 + 第一张图

**文件：**
- 创建：`notebooks/02_basic_stats.ipynb`

- [ ] **步骤 1：Cell 1 — 读数据 + 城市分布统计**

```python
import pandas as pd

df = pd.read_csv('../data/raw/<文件名>.csv')

# 统计城市列每个值出现的次数，取前 10
# （<城市列名> 换成实际的列名，如 city / 城市 / location）
df['<城市列名>'].value_counts().head(10)
```

- [ ] **步骤 2：Cell 2 — 按城市分组看平均薪资**

```python
# 按城市分组，对薪资列求平均值，按从高到低排序，取前 10
df.groupby('<城市列名>')['<薪资列名>'].mean().sort_values(ascending=False).head(10)
```

- [ ] **步骤 3：Cell 3 — 第一张图：城市岗位数量柱状图**

```python
import matplotlib.pyplot as plt

# 统计前 10 城市岗位数并画柱状图
counts = df['<城市列名>'].value_counts().head(10)
counts.plot(kind='bar', title='岗位数量最多的 10 个城市')

# 让中文正常显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.show()
```

- [ ] **步骤 4：运行验证**

预期输出核对：
- 城市分布表打印，数字合理（无异常空值主导）
- 分组薪资表有排序输出
- 柱状图正常显示，标题可见

- [ ] **步骤 5：更新学习笔记**

在 `C:\Users\12923\Desktop\数据分析项目学习笔记.md` 追加：
```markdown
### 基本统计与画图（阶段1）
- `df['列名'].value_counts()`：统计某列每个值的出现次数
- `df.groupby('列A')['列B'].mean()`：按 A 分组求 B 的平均值
- `sort_values(ascending=False)`：降序排序
- `df.plot(kind='bar', title='...')`：画柱状图
- 中文乱码解决：设置 `plt.rcParams['font.sans-serif'] = ['SimHei']`
```

- [ ] **步骤 6：Commit**

```bash
cd /c/Users/12923/Desktop/job-market-analysis && git add notebooks/02_basic_stats.ipynb && git commit -m "feat: 最小闭环分析（城市分布+薪资+第一张图）"
```

### 任务 5：启动 SQL 刷题副线

**文件：**
- 修改：`C:\Users\12923\Desktop\数据分析项目学习笔记.md`（阶段表状态更新）

- [ ] **步骤 1：注册牛客网账号并做第一道 SQL 入门题**

打开 `https://www.nowcoder.com/exam/oj?tab=SQL%E7%AF%87&topicId=199`，注册/登录后完成第一道入门题（SQL1 查询所有列）。目标：会用「SQL 在线编辑器」写 `SELECT` 并提交。

- [ ] **步骤 2：更新学习笔记**

在 `C:\Users\12923\Desktop\数据分析项目学习笔记.md`：
- 「SQL」小节追加第一条知识点：`SELECT * FROM 表名` —— 查询表的所有列
- 「📅 六阶段时间表」把阶段 0、1 状态改为 ✅ 已完成
- 「📝 每周小结」写本周小结（学了什么、卡在哪里、下周计划）

- [ ] **步骤 3：Commit**

```bash
cd /c/Users/12923/Desktop/job-market-analysis && git add docs/superpowers/plans/ && git commit -m "docs: 阶段0-1实现计划"
```

### 任务 6：阶段 0-1 验收

- [ ] **步骤 1：对照规格成功标准自查**

检查清单：
1. Jupyter 能跑 ✅（任务 1）
2. 数据集已下载到 data/raw/ 且有选择记录 ✅（任务 2）
3. 数据概览 notebook 存在且能完整运行 ✅（任务 3）
4. 最小闭环分析有图有结论 ✅（任务 4）
5. SQL 副线已启动（牛客账号 + 第一题） ✅（任务 5）
6. 学习笔记已更新 ✅

- [ ] **步骤 2：提交全部变更并确认仓库干净**

```bash
cd /c/Users/12923/Desktop/job-market-analysis && git status
```
预期：工作区干净，`git log --oneline -5` 能看到本计划各任务的 commit。

---

## 阶段 0-1 完成后

下一份计划（阶段 2：数据清洗 + EDA）将基于实际数据集字段滚动编写。届时先写 `src/cleaning.py`，从 notebook 提炼清洗函数。
