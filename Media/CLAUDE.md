---
description: Media（影视/剧集）笔记的 Claude 指令
---

# Media 笔记规范

## 评分获取

新建或更新影视笔记时，查询以下三个平台的评分，写入 frontmatter：

| 属性 | 来源 | 取值 |
|------|------|------|
| `rotten_tomatoes` | Rotten Tomatoes | 影评人 Tomatometer 各季均值（百分比），备注各季分数 |
| `imdb` | IMDb | 剧集总评分（X.X/10） |
| `metacritic` | Metacritic | 用户评分（百分比） |

查询方式：WebSearch `"<片名>" Rotten Tomatoes IMDb Metacritic scores`，提取每季 critics 分（取中位数或可靠来源的共识值）、IMDb 总评、Metacritic 用户分。

格式示例（见 `Public/Media/Series/Silo.md`）：

```yaml
rotten_tomatoes: 93%（三季影评人均值：S1 88% / S2 92% / S3 100%）
imdb: 8.1/10
metacritic: 73%（用户评分）
```

## 笔记模板

影视笔记使用 YAML frontmatter + 正文内容，必须包含：

- `title`：中文名（英文名）
- `type`：series / movie / anime
- `status`：ongoing / completed / cancelled
- `platform`：播出平台
- `genre`：类型标签列表
- `seasons`：季数
- `episodes`：集数
- `runtime`：每集时长
- `creator`：创作者
- `based_on`：原著（如有）
- `stars`：主演列表（支持 `[[]]` 链接）
- `first_aired` / `last_aired`：首播/末播日期
- `rotten_tomatoes` / `imdb` / `metacritic`：评分（如上）
