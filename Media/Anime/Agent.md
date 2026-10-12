
## Anime（动漫）信息填充规范

触发：「补充 Anime 文档」「更新追番」「新建 YYYY年MM月追番」等。分两步：

1. **脚本**：生成追番表格和动漫笔记的属性（frontmatter），不写正文。
2. **Agent**：自己搜索资料写正文，格式参考 `Accel World.md`。

### 数据来源

| 信息 | 来源 | 说明 |
| --- | --- | --- |
| 作品类别 | acgsecrets.hk 季度页 | 只记两个标签：`#新作` / `#續作` + `#漫畫改編` / `#小說改編` / `#遊戲改編` / `#原創` / `#其他改編` |
| 首播日期 | acgsecrets 播放日 + Sonarr | 本季度有 acgsecrets 条目：用其日本播出日（深夜档算前一天）；跨季度续播：Sonarr 本季度第一集日期，按该作 acgsecrets 与 Sonarr 的日期差换算 |
| 季度 / 集数 | 本地 Sonarr | `第N季` 和 `起-止` 集号都按 Sonarr 的季号、季内集号算，可能和官方说法不一样，以 Sonarr 为准 |
| 动漫笔记属性 | acgsecrets 作品详情 + Sonarr | 见下文「动漫笔记」 |
| 动漫笔记正文 | Agent 搜索（Wikipedia zh/ja/en、MAL、AniList、Bangumi、官网、ANN、fandom wiki） | **不用 acgsecrets** |

- acgsecrets 季度页：`https://acgsecrets.hk/bangumi/YYYYMM/`（MM = 01/04/07/10），追番文件第一行就是这个链接；作品详情在同一页的 `#bangumi_anime_xxx` 区块，作品页为 `https://acgsecrets.hk/anime/<id>/`。
- 跨季度的 2 クール作品（如 LIAR GAME、GNOSIA）在本季度页面查不到时，往前找最多 3 个季度。
- Netflix / Prime Video 独占（JoJo SBR、Edgerunners 等）一般不会收录：笔记属性改用 Sonarr 元数据补，`acgsecrets: 未收录`；改编类型由 Agent 查证后手工写进表格的作品类别（脚本会保留）。

### 季度归属规则（Sonarr 集 → 追番季度）

1. 每一集按播出日落在哪个自然季度（1/4/7/10 月 1 日起）就归哪个季度；
2. 连续播出（间隔 ≤ 21 天）算同一轮。如果一轮在季度结束前 14 天内才开播（9 月下旬提前开播的秋番），整轮都归下一季度；
3. 一个季度里出现多个季号时，以集数最多的那一季为准。

### 追番表格

列固定为：`标题 | Sonar | 作品类别 | 首播日期 | 季度 | 集数`。

- `标题`：中文名（手填）。
- `Sonar`：`[[笔记名]]`，笔记名用 Sonarr 标题；标题里有 Obsidian 不允许的字符（`: / [ ] # ^ |` 等）时，改用 Sonarr 文件夹名（`:` → ` -`）并去掉非法字符。
- `作品类别` 每次都会按 acgsecrets 重写；`首播日期 / 季度 / 集数` 只填空格，已有值保留。值和 Sonarr 不一致时，脚本会列在「需人工确认」里。

### 动漫笔记（`<笔记名>.md`）

属性由脚本维护，正文由 Agent 撰写，两部分分开。

| 属性                                                                          | 来源                                  |
| --------------------------------------------------------------------------- | ----------------------------------- |
| `title`                                                                     | `追番表中文名 (Sonarr 标题)`                |
| `type`                                                                      | `anime`                             |
| `platform`                                                                  | Sonarr network                      |
| `genre`                                                                     | acgsecrets 类型标签（去掉 高期待/高評價/高人氣）     |
| `category`                                                                  | 最近一季的 `#新作/#續作` + 改编类型              |
| `seasons` / `episodes` / `runtime`                                          | Sonarr 正片季数、总集数、单集时长                |
| `author` / `based_on`                                                       | acgsecrets 原作                       |
| `director` / `series_composition` / `character_design` / `music` / `studio` | acgsecrets 製作人員                     |
| `airtime`                                                                   | acgsecrets 播放日                     |
| `first_aired` / `last_aired`                                                | Sonarr（播出中写 `连载中`）                  |
| `acgsecrets`                                                                | 各季 acgsecrets 作品页 URL 列表            |
| `official_site` / `cover`                                                   | acgsecrets 官网链接、封面图                 |
| `sync`                                                                      | `auto` = 属性由脚本维护，重跑时整块属性重新生成；正文永远不动 |

- 有多季 acgsecrets 条目时，制作信息取最近一季。
- **手工整理过属性的笔记**（没有 `sync: auto`，如 Re ZERO、Accel World、SAO）：脚本只补缺失的属性，已有属性不动。想自己维护某篇笔记的属性时，删掉 `sync: auto` 这行即可。
- 脚本新建笔记时正文只有 `# 标题`，需要 Agent 补写。
- alias （别名）和 status （连载状态）不记录/不更新。
- **声优、OP/ED 不写进属性**：声优记在正文 `## 主要角色` 表，OP/ED 记在正文 `**主题曲：**`。

#### 正文规范（参考 `Accel World.md`）

用简体中文写，专有名词用官方中文译名，第一次出现时括号注日/英文名；关键人名、术语加粗。章节按作品实际情况取舍：

- 开头 2–3 段：设定、主角、核心看点；一句话交代原作和制作公司。
- `## 世界观设定` / 核心机制表：只在世界观有特色时写。
- `## 各集列表`：每季一个 `###` 小节，表头 `| # | 标题（英/日/中） | 日期 |`，只列已经播出或已经公布的集；还没公布的写 `> 后续单集标题尚未公布。`。长篇作品（Bleach、JoJo 等）用各季/篇章汇总表（集数范围 + 日期），只有当季逐集列出。
- `**主题曲：**` 列各季 OP/ED。
- `## 剧情概要`：按季或篇章写，只写已经播出的内容。
- `## 原作`：卷数或篇章，以及动画改编到哪里。
- `## 主要角色`：表头 `| 角色 | 声优 | 简介 |`，可按阵营分组。
- `## 核心主题`（简短列表）、`## 制作信息`（制作公司、导演、系列构成、角色设计、音乐、原作）。
- 准确优先：查不到的集名、日期、剧情不写，不要编造。刚开播或还没开播的新番可以写短一些。不加引用列表，不用 emoji。
- 写正文时不要改属性块。

### 执行

脚本在本机（不在 vault 内）：`~/Developer/Scripts/anime_sync/`

```bash
cd ~/Developer/Scripts/anime_sync
python3 sync.py --dry-run              # 预览，列出要改的文件和需人工确认项
python3 sync.py                        # 写入全部追番表格和动漫笔记
python3 sync.py --quarter 202610       # 只处理某个季度
python3 sync.py --refresh              # 重新下载 acgsecrets 页面（默认用 ~/.cache/anime-sync 缓存）
```

- Sonarr 地址和 API key 在 `~/.config/anime-sync/sonarr.env`（`SONARR_URL`、`SONARR_API_KEY`），不写进 vault。
- 新季度：先建 `YYYY年MM月追番.md`（第一行 acgsecrets 季度页链接 + 空表格），填好 `标题` 和 `Sonar` 两列，再跑 `--refresh`；然后给新建的笔记（正文只有 `# 标题` 的那些）按上面的正文规范补写正文，笔记多时可以分批交给子 agent 并行写。
- 跑完逐条处理「需人工确认」：Sonarr 找不到的检查 Sonarr 标题；acgsecrets 未收录的手工补改编类型；保留值和 Sonarr 不一致的向用户确认。
