---
tags:
  - meta
  - plugins
---

# Plugins

Obsidian 已安装插件及详细用法归纳。

---

## 模板 & 自动化

### Templater

高级模板引擎，支持类 Handlebars 语法，替代 Obsidian 内置模板。可在模板中内嵌 JavaScript 逻辑。

**当前配置：**
- 模板目录：`Templates/`
- `trigger_on_file_creation: true` — 在特定文件夹创建文件时自动应用对应模板（需在 Settings → Templater → Folder Templates 中绑定文件夹与模板）

**核心模块：**

`tp.date` — 日期时间处理
| 函数 | 说明 |
|---|---|
| `tp.date.now("YYYY-MM-DD")` | 当前日期，支持 Moment.js 格式 |
| `tp.date.tomorrow("YYYY-MM-DD")` | 明天 |
| `tp.date.yesterday("YYYY-MM-DD")` | 昨天 |
| `tp.date.weekday("YYYY-MM-DD", 3)` | 本周特定星期（0=周日） |
| `tp.date.now("YYYY-MM-DD", -7)` | 7 天前 |

`tp.file` — 文件操作
| 函数 | 说明 |
|---|---|
| `tp.file.title` | 当前文件名（无后缀） |
| `tp.file.tags` | 文件中所有标签的数组 |
| `tp.file.content` | 文件全文 |
| `tp.file.folder()` | 所在文件夹 |
| `tp.file.creation_date("YYYY-MM-DD")` | 文件创建日期 |
| `tp.file.last_modified_date("YYYY-MM-DD")` | 最后修改日期 |
| `tp.file.rename("新标题")` | 重命名当前文件 |
| `tp.file.move("新路径/新标题")` | 移动文件到新位置 |
| `tp.file.include("[[其他文件]]")` | 嵌入其他文件内容（模板嵌套） |
| `tp.file.exists("文件名")` | 检查文件是否存在 |
| `tp.file.create_new("模板内容", "文件名")` | 从模板创建新文件 |
| `tp.file.cursor()` | 设置模板插入后的光标停留位置 |
| `tp.file.cursor_append("内容")` | 在光标后追加内容 |

`tp.frontmatter` — 元数据读写
```markdown
<% tp.frontmatter.title %>           <!-- 读取 -->
<% tp.frontmatter["date"] = "2026-07-29" %>  <!-- 写入 -->
```

`tp.system` — 系统交互
| 函数 | 说明 |
|---|---|
| `tp.system.prompt("请输入：")` | 弹出文本输入框 |
| `tp.system.suggester(["选项A","选项B"], ["A","B"])` | 弹出选择列表 |
| `tp.system.clipboard()` | 读取剪贴板内容 |

`tp.web` — 网络资源
| 函数 | 说明 |
|---|---|
| `tp.web.daily_quote()` | 每日一句 |
| `tp.web.random_picture("800x600")` | 随机图片 |
| `tp.web.request("https://api.example.com")` | HTTP 请求 |

`tp.user` — 调用用户自定义脚本（放在 Templater 脚本目录中的 JS 文件）

典型模板示例（新建日记）：
```markdown
---
date: <% tp.date.now("YYYY-MM-DD") %>
tags: [diary]
---

# <% tp.date.now("YYYY-MM-DD dddd") %>

## 待办
- [ ] 

## 笔记

## 总结
```

---

### Linter

自动格式化笔记，统一写作规范。支持 **65 条规则**，分 6 大类：

**YAML 规则（14 条）**
- `yaml-key-sort` — 按指定顺序排列 frontmatter 键
- `yaml-timestamp` — 自动添加/更新 created/modified 时间戳
- `yaml-title` — 将文件名同步到 YAML title 字段
- `format-tags-in-yaml` — 统一 YAML 中标签格式
- `move-tags-to-yaml` — 将正文内标签移入 frontmatter
- `remove-yaml-keys` — 删除指定的 YAML 键
- `dedupe-yaml-array-values` — 去除 YAML 数组重复值
- `sort-yaml-array-values` — 排序 YAML 数组

**标题规则（5 条）**
- `capitalize-headings` — 标题首字母大写
- `header-increment` — 标题层级不得跳级（H1 后必须 H2）
- `headings-start-line` — 标题和内容必须分行
- `file-name-heading` — 自动插入与文件名相同的标题
- `remove-trailing-punctuation-in-heading` — 移除标题末尾标点

**内容规则（16 条）**
- `emphasis-style` — 统一强调符（`*斜体*` vs `_斜体_`）
- `strong-style` — 统一加粗符（`**加粗**` vs `__加粗__`）
- `unordered-list-style` — 统一列表符（`-` / `*` / `+`）
- `ordered-list-style` — 统一有序列表格式
- `quote-style` — 统一引号（单引号 vs 双引号）
- `blockquote-style` — 统一引用块标记
- `proper-ellipsis` — `...` 转换为 `…`
- `auto-correct-common-misspellings` — 自动纠正常见拼写错误
- `no-bare-urls` — 将裸 URL 包裹为 `<>` 或链接格式
- `default-language-for-code-fences` — 代码块添加默认语言标识
- `remove-multiple-spaces` — 合并多个空格

**间距规则（19 条）**
- `consecutive-blank-lines` — 限制连续空行数（如最多 1 行）
- `line-break-at-document-end` — 文件末尾确保一个换行
- `trailing-spaces` — 删除行尾空格
- `paragraph-blank-lines` — 段落之间加空行
- `heading-blank-lines` — 标题前后空行规范
- `empty-line-around-code-fences` — 代码块前后加空行
- `empty-line-around-tables` — 表格前后加空行
- `empty-line-around-blockquotes` — 引用块前后加空行
- `space-after-list-markers` — 列表标记后加空格
- `space-between-chinese-japanese-or-korean-and-english-or-numbers` — CJK 与英文/数字间加空格
- `move-math-block-indicators-to-their-own-line` — `$$` 单独成行

**脚注规则（3 条）**
- `move-footnotes-to-the-bottom` — 脚注移到文末
- `re-index-footnotes` — 自动重编号脚注

**粘贴规则（8 条）** — 粘贴内容时自动应用（去空格、合并空行、规范省略号等）

用法：
- 安装后在 Settings → Linter 中按需开启规则
- 设置 `foldersToIgnore` 排除模板等不想格式化的目录
- 保存时自动格式化：开启 `Lint on save`
- 手动格式化：`Ctrl+P` → `Linter: Lint the current file`
- 批量格式化：`Ctrl+P` → `Linter: Lint all files`

**当前配置（已启用规则）：**
- `lintOnSave: true` — 保存时自动格式化
- `header-increment` — 标题层级不跳级，从 H2 开始（`start-at-h2: true`）
- `headings-start-line` — 标题和内容分行
- `remove-trailing-punctuation-in-heading` — 移除标题末尾标点
- `move-footnotes-to-the-bottom` — 脚注移至文末
- `auto-correct-common-misspellings` — 自动纠正常见英文拼写
- `blockquote-style: no space` — 引用块 `>` 后无空格
- `space-between-chinese-japanese-or-korean-and-english-or-numbers` — CJK 与英文/数字间自动加空格（对中英混排笔记重要）
- `trailing-spaces` — 删除行尾空格
- `line-break-at-document-end` — 文件末尾确保换行
- `consecutive-blank-lines` — 限制最多 1 个连续空行
- `foldersToIgnore: ["Templates"]` — 不格式化模板文件夹

---

## 数据查询

### Dataview

将 Obsidian 仓库当作结构化数据库查询。支持两种模式：**DQL**（类 SQL）和 **DataviewJS**（JavaScript API），外加行内查询。

**当前配置：**
- `enableDataviewJs: true` — DataviewJS 代码块（`dataviewjs`）已启用
- `enableInlineQueries: true` — 行内查询（`` `= expr` ``）已启用
- `defaultDateFormat: "YYYY-MM-DD"` — 日期显示格式
- `tableIdColumnName: "文件"` — 表格首列标题汉化
- `tableGroupColumnName: "分组"` — 分组列标题汉化

**查询类型：**

| 类型 | 说明 | 示例 |
|---|---|---|
| `TABLE` | 表格输出，列可自定义 | `TABLE author, file.ctime FROM #books` |
| `LIST` | 无序列表 | `LIST FROM #meeting` |
| `TASK` | 任务列表 | `TASK FROM #project WHERE !completed` |
| `CALENDAR` | 日历视图（需日期字段） | `CALENDAR due FROM #tasks` |

**完整 DQL 语法结构：**
```dataview
<QUERY-TYPE> [WITHOUT ID] [字段列表]
FROM <数据源>                    -- 标签、文件夹、链接等
[WHERE <条件>]                   -- 过滤
[SORT <字段> ASC/DESC]          -- 排序
[GROUP BY <字段>]                -- 分组
[FLATTEN <字段>]                 -- 展开数组
[LIMIT <数量>]                   -- 限制条数
```

**FROM 数据源：**
```dataview
FROM #tag                    -- 单一标签
FROM #tag1 AND #tag2         -- 同时满足
FROM #books - #archived      -- 排除
FROM "folder/subfolder"      -- 文件夹
FROM [[笔记链接]]             -- 引用特定笔记的所有文件
FROM outgoing([[笔记]])       -- 当前笔记引用的所有文件
```

**WHERE 条件函数：**
```dataview
WHERE status = "open"
WHERE due < date(today)      -- 过期的
WHERE contains(tags, "#important")
WHERE file.size < 1000
WHERE startswith(file.name, "SPX-")
WHERE !completed             -- 未完成的
```

**常用函数：**
| 函数 | 说明 |
|---|---|
| `contains(list, value)` | 列表是否包含值 |
| `filter(list, (x) => condition)` | 过滤列表 |
| `map(list, (x) => expression)` | 映射列表 |
| `date(today)` | 今天日期 |
| `date(yesterday)` | 昨天日期 |
| `choice(cond, trueVal, falseVal)` | 三元判断 |
| `default(value, fallback)` | 空值兜底 |
| `nonnull(list)` | 去空值 |
| `join(list, delimiter)` | 连接数组 |
| `sort(list)` | 排序 |
| `length(value)` | 长度 |
| `startswith(str, prefix)` | 字符串前缀匹配 |
| `regexmatch(str, pattern)` | 正则匹配 |
| `file.link` | 文件链接 |
| `file.name` | 文件名 |
| `file.path` | 相对路径 |
| `file.folder` | 文件夹 |
| `file.ctime` / `file.mtime` | 创建/修改时间 |
| `file.inlinks` / `file.outlinks` | 反向链接/正向链接 |
| `file.tags` | 所有标签 |

**FLATTEN 用法（将数组展开为独立行）：**
```dataview
TABLE item.text
FROM #notes
FLATTEN file.lists AS item
WHERE contains(item.tags, "#todo")
```
展开所有列表项，然后筛选带有 #todo 标签的。

**GROUP BY 用法：**
```dataview
TABLE rows.file.link AS "笔记"
FROM #projects
GROUP BY file.folder
```
按文件夹分组显示项目。

**行内查询：**
````markdown
今天是 `= date(today)` 
文件数量：`= length(filter( [[#]].file.inlinks, (f) => contains(f.tags, "#project")))` 
当前文件标签：`= this.file.tags` 
````

真实应用范例：
- 自动汇总所有项目状态：`TABLE status, deadline FROM #project WHERE !completed SORT deadline ASC`
- 阅读清单：`TABLE author, rating FROM #book WHERE !read SORT file.ctime DESC`
- MOC 自动生成：`LIST FROM #moc-topic AND -#template`
- 每日待办聚合：`TASK FROM "daily" WHERE !completed AND due <= date(today)`

---

### Tasks

增强任务管理，通过 Emoji 短码在任务行内标记各种属性。

**Emoji 速查：**

| Emoji | 作用 | 格式 |
|---|---|---|
| 📅 | 截止日期 (Due) | `📅 2026-07-30` |
| ⏳ | 计划日期 (Scheduled) | `⏳ 2026-07-25` |
| 🛫 | 开始日期 (Start) | `🛫 2026-07-20` |
| ✅ | 完成日期 (Done) | `✅ 2026-07-29` |
| ➕ | 创建日期 (Created) | `➕ 2026-07-15` |
| ⏰ | 提醒时间 | `⏰ 2026-07-30 10:00` |
| 🔁 | 重复规则 | `🔁 every week on Monday` |
| 🔺 | 最高优先级 | |
| ⏫ | 高优先级 | |
| 🔼 | 中优先级 | |
| 🔽 | 低优先级 | |
| ⏬ | 最低优先级 | |

**重复任务写法：**
```
- [ ] 每周复盘 🔁 every week on Sunday 📅 2026-07-26
- [ ] 每日站会 🔁 every weekday 📅 2026-07-29
- [ ] 月报提交 🔁 every month on the 1st 📅 2026-08-01
- [ ] 每两周打扫 🔁 every 2 weeks 📅 2026-07-18
- [ ] 交房租 🔁 every month 📅 2026-07-01
```

勾选完成时自动在原基础上生成下一次任务。

**查询汇总代码块：**
```tasks
not done
due before tomorrow
sort by priority
```
所有今天或之前截止的未完成事项，按优先级排列。

```tasks
not done
(priority is 🔺) OR (priority is ⏫)
group by due
```
高优先级/最高优先级任务，按截止日期分组。

```tasks
done
done on today
```
今日已完成的全部任务。

```tasks
not done
happens next week
sort by due date
```
下周的计划任务。

```tasks
not done
tags include #project/alpha
sort by urgency
```
特定项目任务，按紧急度排序。

**常用查询过滤字段：**
- `not done` / `done` — 状态
- `due before/after <date>` — 截止日期范围
- `happens this week / next week` — 自然语言时间
- `priority is above medium` — 优先级高于中
- `tags include <tag>` — 标签匹配
- `heading includes <text>` — 所在标题匹配
- `path includes <folder>` — 文件路径匹配
- `sort by priority / due / urgency / created` — 排序
- `group by due / priority / filename` — 分组

---

## 可视化 & 绘图

### Excalidraw

在 Obsidian 内直接创建和编辑手绘风格图形，是功能最丰富的社区插件之一。

**支持的图类型：**
- 流程图、架构图、线框图
- Mermaid 图表（State 图、ER 图）
- C4 架构模型图（需导入库）
- 思维导图（内置 MindMap Builder）
- 手绘草稿 & 白板笔记
- 原子绘图拼接（book-on-a-page）
- 文本自动转图（粘贴 CSV 类数据自动生成）

**核心功能：**

基础绘图：形状、箭头、自由绘制、文本、图片、橡皮擦、激光笔

链接与嵌入：
- `[[笔记]]` — 内部链接（双向链接 + 反链）
- `[[绘图#^elementID]]` — 引用图中特定元素
- `![[绘图.excalidraw]]` — 在 Markdown 中嵌入绘图
- `![[绘图.excalidraw|300]]` — 控制宽度
- 拖放：文件变链接、文本变画布元素、YouTube URL 变缩略图
- Shift+拖放 Markdown 文件 = 嵌入全文

模板系统：
- 模板文件可预设笔触粗细、颜色、字体、调色板
- 与 Templater 插件联动自动应用
- 通过 frontmatter 控制：`excalidraw-default-mode`(view/zen)、`excalidraw-autoexport`(none/both/png/svg)

脚本引擎 (ExcalidrawAutomate)：
- 宏自动化，可从脚本库下载现成脚本
- 支持 QuickAdd、Templater、Dataview 联动
- 可按文件夹分组并绑定快捷键
- 能用脚本在侧边栏创建自定义面板

导出格式：
- SVG（矢量） / PNG（位图），每次保存自动导出
- 暗色/亮色模式两套版本适配发布站
- 支持一文件一导出设置（frontmatter 中配置）
- PDF 导出、`.excalidraw` 标准格式导出

其他特性：
- LaTeX 公式输入（悬浮编辑器）
- 图片 OCR 文字识别
- 自定义字体、自定义笔刷
- SVG 导入并转为可编辑图形
- 移动端完整支持
- 支持 Obsidian Sync、Obsidian Publish

---

### Mindmap NextGen

将 Markdown 标题层级即时渲染为可交互思维导图。

**使用方式：**

1. 打开任意 Markdown 文件 → `Ctrl+P` → `Mindmap NextGen: Open as mindmap`
   - **Pinned**（固定模式）：始终显示该文件
   - **Unpinned**（浮动模式）：跟随当前活跃文件切换

2. 代码块内嵌思维导图：
````markdown
```markmap
# 项目管理
## 需求分析
### 用户访谈
### 竞品分析
## 技术方案
### 架构设计
### 数据库选型
## 开发计划
### Sprint 1
### Sprint 2
```
````

**语法支持：**
- 标题层级 (`#` ~ `######`) → 节点层级
- 任务列表 `- [ ]` / `- [x]` → 节点显示为复选框
- LaTeX：`$\frac{\partial f}{\partial t}$` → 数学公式
- 代码块：自动语法高亮（需配合 highlight.js CSS snippet）

**节点样式定制（HTML 注释语法）：**
```markdown
# 项目 <!-- nodeColor: #663366 -->
## 风险 <!-- bgColor: red; color: white; fold: this -->
- 风险项一
- 风险项二
## 目标 <!-- nodeColor: #2e86de; fold: tree -->
### 短期
### 长期
```

| 参数 | 效果 | 子节点继承？ |
|---|---|---|
| `nodeColor` | 节点圆点和连线颜色 | 是 |
| `bgColor` | 节点背景色 | 否 |
| `color` | 节点文字颜色 | 否 |
| `fold: this` | 默认折叠此节点 | 否 |
| `fold: tree` | 默认折叠该节点及全部子节点 | 否 |

**每文件 frontmatter 设置：**
```yaml
---
markmap:
  titleAsRootNode: true       # 用文件名当根节点
  screenshotTextColor: "#28F48D"
  highlight: true            # 高亮内嵌导图块
---
```

**颜色模式：**
- Branch 分支着色（每分支随机色，可设冻结层级）
- Depth 深度着色（按层级指定颜色，最多 3 级 + 默认）
- Single 单色模式

---

### Calendar

侧边栏日历面板，提供每日笔记的可视化入口。

**功能：**
- 右键侧边栏图标 → 打开日历面板
- 单击日期 → 跳转到对应日记
- 日期下方小圆点 → 表示当天已有笔记
- 需要 Obsidian 核心插件 **Daily Notes** 配合使用
- 支持周维度导航（显示当前周号）

**设置要点：**
- Daily Notes 中先配好日记文件夹和日期格式
- Calendar 会自动读取 Daily Notes 配置
- 在 Calendar 设置中可开启 `Start week on Monday`

---

## 编辑增强

### Advanced Tables

Markdown 表格编辑增强，类似电子表格操作体验。

**键盘操作：**
| 快捷键 | 功能 |
|---|---|
| `Tab` | 跳转到下一单元格（末尾自动加行） |
| `Shift+Tab` | 跳转到上一单元格 |
| `Enter` | 在单元格内换行 |
| `Ctrl+Shift+D` | 打开表格控制工具栏 |
| `Ctrl+Shift+A` | 格式化当前表格（自动对齐列宽） |

**工具栏操作（`Ctrl+Shift+D` 打开）：**
- 左/右移列
- 上/下移行
- 插入/删除行、列
- 公式求值
- 排序（按列升序/降序）
- CSV 导出

**公式语法：**

公式写在与表格紧邻的下一行，`=` 前缀，目标单元格: 表达式。需要**手动触发求值**（不会自动计算）。

```
| 项目   | 数量 | 单价 | 金额 |
|--------|------|------|------|
| 苹果   | 3    | 5    |      |
| 橘子   | 2    | 6    |      |
| 西瓜   | 1    | 20   |      |
| 合计   |      |      |      |
=D2: B2*C2
=D3: B3*C3
=D4: B4*C4
=D5: sum(D2..D4)
```

**支持的公式函数：**
| 函数 | 说明 |
|---|---|
| `sum(range)` | 求和，如 `sum(A1:A5)` `sum(A1..A5)` |
| `avg(range)` | 平均值 |
| `min(range)` | 最小值 |
| `max(range)` | 最大值 |
| `count(range)` | 计数 |
| `A1*B1` | 单元格乘 |
| `(A1+B1)/C1` | 四则运算 |

**TBLFM 内部语法（HTML 注释，可手写）：**
```
<!-- TBLFM: @>$2=sum(@I..@-2) -->
```
- `@>` = 最后一行
- `@I` = 第一个数据行
- `@-2` = 倒数第二行
- `$2` = 第 2 列

注意：公式不会自动更新，修改数据后需重新触发求值。公式在 Markdown 源码中始终可见。

---

### Iconic

在 Obsidian UI 中可视化更换图标和颜色，支持 **1700+ Lucide 图标**和 **1900+ 表情符号**。

**可自定义的对象：**
- 标签页图标（文件标签页、插件标签页）
- 文件/文件夹图标（含打开/关闭两种状态）
- 书签 & 书签分组
- 标签图标
- 属性 (Properties) 图标
- Ribbon 侧边栏命令按钮
- 窗口控制按钮（最小化/最大化/关闭）

**操作方式：**
- 右键目标元素 → `Change icon` → 搜索图标/emoji → 点击选定
- 按住 `Alt` 或 `Shift` 可批量选择多个同类型元素
- 右键颜色气泡 → RGB 拾色器精确选色
- 每种图标支持 **9 种主题自适应预设色**

**智能规则引擎：**
自动根据条件设置文件/文件夹图标：
- 按文件名、后缀、路径、文件夹匹配
- 按 frontmatter 属性、标签、标题、链接匹配
- 按文件创建/修改日期匹配
- 按系统时间（实时变更，如节日换图标）
- 支持 All / Any / None 组合逻辑
- 规则可拖拽排序，靠前优先

---

## 版本控制

### Git

在 Obsidian 内完整使用 Git 版本控制，无需打开终端。

**自动备份：**
- 按间隔自动提交+推送（如每 15 分钟）
- 支持自动拉取（启动 Obsidian 时）
- 文件修改时自动提交
- 提交信息模板：`vault backup: {{date}}`（{{date}} 自动替换）

**差异对比 (Diff View)：**
- 左右分屏对比（Split）或统一视图（Unified）
- 增/删以绿色/红色高亮，支持词级标记
- 可从 Source Control 面板、命令面板、或直接对当前文件打开

**历史与恢复：**
- 浏览全仓库提交历史（信息、作者、日期、变更文件列表）
- 查看单文件提交历史（含改名前的记录）
- 回溯到任意历史版本并恢复文件
- 撤销未提交的改动 (Discard Changes)
- 撤销暂存 (Unstage)

**命令一览：**
- `Git: Commit all changes` — 提交所有变更
- `Git: Commit and sync` — 提交 + 拉取 + 推送
- `Git: Push` / `Git: Pull` / `Git: Fetch` — 远程操作
- `Git: View history` — 查看提交历史
- `Git: View file history` — 查看当前文件历史
- `Git: Open file in GitHub` — 浏览器中打开 GitHub 对应文件
- `Git: Create backup` — 一键备份
- `Git: Discard all changes` — 放弃所有未提交改动

**当前配置：**
- `autoPullOnBoot: true` — 启动 Obsidian 时自动拉取远端
- `pullBeforePush: true` — 推送前先拉取（避免冲突）
- `disablePopupsForNoChanges: true` — 无变更时不弹提示
- `showStatusBar: true` / `showBranchStatusBar: true` — 状态栏显示 Git 状态和当前分支
- `syncMethod: "merge"` — 冲突使用 merge 策略
- 自动备份未开启（`autoSaveInterval: 0`）——手动通过命令或 pre-push hook 控制提交节奏

**注意：** 桌面端全功能，移动端使用 isomorphic-git（限制较多，仅适合小仓库小提交）。

---

## 主题 & 样式

### Style Settings

无需手写 CSS，通过界面控件调整主题和插件的 CSS 变量，更改实时生效。

**原理：**
主题/插件作者在 CSS 中通过 `/* @settings */` 注释块声明可调节项，Style Settings 自动读取并生成控件。

**支持的控件类型：**

| 类型 | 说明 |
|---|---|
| `variable-color` | 颜色选择器（支持 hex/rgb/hsl 格式） |
| `variable-themed-color` | 分亮色/暗色模式的独立颜色选择器 |
| `variable-number` | 数值输入（如 `700px` `1.2rem`） |
| `variable-number-slider` | 滑块（设 min/max/step） |
| `variable-text` | 文本输入（如字体名） |
| `variable-select` | 下拉选择框 |
| `class-toggle` | 开关（开/关 CSS class） |
| `class-select` | 多选项下拉 |
| `heading` | 分类标题（可折叠） |
| `info-text` | 说明文字 |
| `color-gradient` | 在两颜色间自动插值生成渐变色阶 |

**常见可调节项：**
- 界面主题色（强调色、背景色、边框色）
- 字体族、字号、字重、行高（可按 H1-H6 分级）
- 行宽、侧边栏宽度
- 动画开/关、彩色文件夹、聚焦模式、自定义滚动条
- 代码块配色、表格样式、图片样式、标注框 (Callout) 样式
- 状态栏、Ribbon 样式

**使用：**
Settings → Style Settings（独立选项卡）→ 选择主题/插件 → 调整各项 → 即时预览。并非所有主题都支持 Style Settings，取决于主题作者是否写了配置注释。主流主题（如 Minimal、Border、AnuPpuccin）均有丰富支持。

---

## 表格增强

### Indented Table

让 Markdown 管道表格（pipe table）在列表项缩进内正确渲染。无需配置，安装即生效。

**解决的问题：** 标准 Obsidian 不渲染列表内缩进的表格，此插件修复该行为。

**用法：**
````markdown
- 某功能对比
  | 方案 | 优点 | 缺点 |
  |------|------|------|
  | A    | 快   | 贵   |
  | B    | 便宜 | 慢   |
- 另一个列表项继续
````

渲染效果：列表项下方直接显示格式化表格，层级关系清晰。适合在需求文档、对比分析中将表格内嵌在列表结构里。

---

## 图表

### Charts

在 Markdown 中通过 `chart` 代码块创建交互式图表，基于 Chart.js 渲染。

**语法结构：**
````markdown
```chart
type: bar
labels: [一月, 二月, 三月, 四月]
series:
  - title: 完成量
    data: [12, 19, 8, 15]
  - title: 目标量
    data: [15, 15, 15, 15]
xTitle: 月份
yTitle: 数量
tension: 0.4
width: 80%
labelColors: false
fill: false
beginAtZero: true
bestFit: false
bestFitTitle: 趋势线
bestFitNumber: 0
```
````

**支持的图表类型：**

| 类型 | `type` 值 | 适用场景 |
|------|-----------|----------|
| 柱状图 | `bar` | 对比数量 |
| 折线图 | `line` | 趋势变化 |
| 饼图 | `pie` | 占比分布 |
| 环形图 | `doughnut` | 占比分布（带中空） |
| 雷达图 | `radar` | 多维度对比 |
| 极坐标图 | `polarArea` | 极坐标占比 |

**关键参数说明：**

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `type` | 图表类型 | 必填 |
| `labels` | X 轴标签数组 | 必填 |
| `series` | 数据系列（含 `title` 和 `data`） | 必填 |
| `xTitle` / `yTitle` | 坐标轴标题 | 无 |
| `tension` | 折线曲率（0=直线，1=最弯） | 0 |
| `width` | 图表宽度（px 或 %） | 100% |
| `fill` | 折线图面积填充 | false |
| `beginAtZero` | Y 轴从 0 开始 | true |
| `bestFit` | 显示趋势线（仅折线/散点图） | false |
| `labelColors` | 图例使用数据颜色 | false |

**实用示例——需求完成率折线图：**
````markdown
```chart
type: line
labels: [Sprint 1, Sprint 2, Sprint 3, Sprint 4]
series:
  - title: 完成率(%)
    data: [75, 82, 90, 88]
xTitle: Sprint
yTitle: 完成率
tension: 0.3
beginAtZero: false
fill: false
```
````
