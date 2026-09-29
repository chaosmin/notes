#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "requests",
#   "beautifulsoup4",
#   "lxml",
# ]
# ///
"""
碧蓝航线舰娘信息爬虫
从 wiki.biligame.com/blhx/ 抓取数据并生成 Obsidian Markdown 文档

用法: uv run warship.py <舰娘名>
示例: uv run warship.py 普林斯顿
"""

import re
import sys
from pathlib import Path
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

# 性能评级 → 雷达图数值映射 (0-100)
GRADE_MAP: dict[str, int] = {"S": 100, "A": 85, "B": 65, "C": 45, "D": 25, "E": 10}

# 六维性能属性（雷达图顺序）
STAT_ORDER = ["耐久", "炮击", "雷击", "航空", "防空", "机动"]


# ── 工具函数 ─────────────────────────────────────────────────────────────────

def thumb_to_full(src: str) -> str:
    """MediaWiki thumb URL → 原图 URL
    e.g. .../thumb/b/b6/hash.jpg/85px-xxx.jpg  →  .../b/b6/hash.jpg
    也兼容 protocol-relative URL (//host/...)
    """
    if "/thumb/" not in src:
        return src
    # 以 /thumb/ 为界分割，取左侧 base + 右侧前三段 (a/bb/hash.ext)
    base, rest = src.split("/thumb/", 1)
    parts = rest.split("/")   # ["7", "77", "hash.jpg", "85px-...jpg"]
    if len(parts) >= 3:
        return base + "/" + "/".join(parts[:3])
    return src


def normalize_ws(text: str) -> str:
    """合并多余空白。"""
    return re.sub(r"\s+", " ", text).strip()


def elem_to_md(node) -> str:
    """
    将 BeautifulSoup 节点转为 Markdown 文本，保留加粗/斜体。
    只处理行内元素；块级结构由调用方负责。
    """
    from bs4 import NavigableString, Tag

    if isinstance(node, NavigableString):
        return str(node)

    tag = node.name
    inner = "".join(elem_to_md(c) for c in node.children)

    if tag in ("b", "strong"):
        stripped = inner.strip()
        return f"**{stripped}**" if stripped else ""
    if tag in ("i", "em"):
        stripped = inner.strip()
        return f"*{stripped}*" if stripped else ""
    if tag == "br":
        return "\n"
    # 链接：只保留文字
    return inner


def node_to_md(node) -> str:
    """elem_to_md + 空白规范化。"""
    return normalize_ws(elem_to_md(node))


# ── 网络 ──────────────────────────────────────────────────────────────────────

def fetch_page(name: str) -> tuple[BeautifulSoup, str]:
    wiki_url = f"https://wiki.biligame.com/blhx/{quote(name)}"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        )
    }
    resp = requests.get(wiki_url, headers=headers, timeout=20)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "lxml"), wiki_url


# ── 解析 ──────────────────────────────────────────────────────────────────────

def parse_header(soup: BeautifulSoup, name: str) -> dict:
    """解析 sv-general 第一行，提取舰级、号数、别名。
    示例行文本: '独立级轻型航空母舰2号舰 普林斯顿 USS Princeton プリンストン'
    """
    gen = soup.find("table", class_=lambda c: c and "sv-general" in c)
    if not gen:
        return {}

    first_td = gen.find("tr").find("td")
    if not first_td:
        return {}

    raw = normalize_ws(first_td.get_text(" ", strip=True))
    text = normalize_ws(raw.replace(name, ""))

    # 舰号：兼容 "2号舰" / "二番舰" / "2番舰" / "二号舰" / "2号艦" 等写法
    num_m = re.search(r"[一二三四五六七八九十百\d]+[号番][舰艦]", text)
    ship_number = num_m.group(0) if num_m else ""

    # 舰级 (号数前的中文部分)
    if num_m:
        ship_class = text[: num_m.start()].strip()
        remainder = text[num_m.end() :].strip()
    else:
        # 无号数舰，从 <a> 标签取舰级
        link = first_td.find("a")
        ship_class = normalize_ws(link.get_text()) if link else ""
        remainder = normalize_ws(text.replace(ship_class, ""))

    # 别名：英文（USS/HMS/KMS 等前缀或纯 ASCII）
    aliases: list[str] = []
    en_m = re.search(
        r"(USS|HMS|KMS|FFNF|MNF|SN|ROCS|IJN)\s+\S+", remainder
    )
    if en_m:
        aliases.append(en_m.group(0))
    else:
        ascii_tokens = [
            t for t in remainder.split() if re.match(r"^[A-Za-z0-9\-\.]+$", t)
        ]
        if ascii_tokens:
            aliases.append(" ".join(ascii_tokens))

    # 别名：日文（片假名）
    for tok in remainder.split():
        if re.search(r"[\u30A0-\u30FF]", tok) and tok not in aliases:
            aliases.append(tok)

    return {"ship_class": ship_class, "ship_number": ship_number, "aliases": aliases}


def parse_info(soup: BeautifulSoup) -> dict:
    """从 sv-general 提取编号、舰种、阵营、稀有度、获取途径等。"""
    info: dict = {}
    gen = soup.find("table", class_=lambda c: c and "sv-general" in c)
    if not gen:
        return info

    for row in gen.find_all("tr"):
        tds = row.find_all("td")
        texts = [normalize_ws(td.get_text()) for td in tds]

        for i, label in enumerate(texts):
            nxt = i + 1
            if nxt >= len(tds):
                continue
            val = texts[nxt]
            val_td = tds[nxt]

            if label == "编号":
                info["number"] = val
            elif label == "类型":
                info["ship_type"] = val
                img = val_td.find("img")
                if img:
                    info["ship_type_icon"] = img["src"]
            elif label == "稀有度":
                # "★★☆☆☆精锐" / "★★☆☆☆ 精锐" → "★★☆☆☆"（只保留星形字符）
                stars = re.sub(r"[^★☆]", "", val)
                info["rarity"] = stars if stars else val
            elif label == "阵营":
                info["faction"] = val
                img = val_td.find("img")
                if img:
                    info["faction_icon"] = img["src"]
            elif label == "建造时间":
                info["build_time"] = val
            elif label == "普通掉落点" and val:
                info["normal_drop"] = val
            elif "活动" in label and "掉落" in label and val:
                info["event_drop"] = val
            elif label == "其他途径" and val:
                info["other_obtain"] = val

    return info


def parse_stats(soup: BeautifulSoup) -> dict:
    """从 sv-performance 提取评级（A/B/C…）和初始→满级数值。"""
    stats: dict = {}
    perf = soup.find_all("table", class_=lambda c: c and "sv-performance" in c)

    # 第一张 sv-performance：评级内嵌表
    if perf:
        for inner in perf[0].find_all("table"):
            for row in inner.find_all("tr"):
                tds = row.find_all("td")
                if len(tds) == 2:
                    stat = tds[0].get_text(strip=True)
                    grade = tds[1].get_text(strip=True)
                    if stat in STAT_ORDER:
                        stats[f"{stat}_grade"] = grade

    # 第二张 sv-performance：数值
    if len(perf) >= 2:
        text = perf[1].get_text()
        for stat in STAT_ORDER:
            m = re.search(rf"{stat}\s+(\d+)→(\d+)", text)
            if m:
                stats[f"{stat}_init"] = int(m.group(1))
                stats[f"{stat}_max"] = int(m.group(2))

    return stats


def parse_skills(soup: BeautifulSoup) -> list[dict]:
    """从 sv-skill 提取技能（跳过模板占位行）。"""
    skills: list[dict] = []
    skill_table = soup.find("table", class_=lambda c: c and "sv-skill" in c)
    if not skill_table:
        return skills

    for row in skill_table.find_all("tr"):
        tds = row.find_all("td")
        if len(tds) != 2:
            continue
        name_text = tds[0].get_text(strip=True)
        # 跳过模板占位符和空行
        if not name_text or "{{{" in name_text:
            continue
        # 必须有真实图片（模板行的 img 不会被渲染）
        if not tds[0].find("img"):
            continue
        skills.append(
            {"name": name_text, "desc": node_to_md(tds[1])}
        )

    return skills


def get_portrait(soup: BeautifulSoup, name: str) -> str:
    """查找舰娘头像图片并返回原图 URL。"""
    for img in soup.find_all("img"):
        if f"{name}头像" in img.get("alt", ""):
            return thumb_to_full(img.get("src", ""))
    return ""


def parse_history(soup: BeautifulSoup, ship_class: str) -> dict:
    """
    解析「舰船相关」H2 下的全部小节。
    - class_parts : H3 标题与 ship_class 匹配 → 单独写到舰级 md
    - ship_parts  : 其余 H3 小节（原型舰简介、舰船历史等）→ 写到舰娘历史介绍

    返回: {
      "class_parts": [(h3_title, [paragraph, ...]), ...],
      "ship_parts":  [(h3_title, [paragraph, ...]), ...],
    }
    """
    content = soup.find(id="mw-content-text")
    if not content:
        return {"class_parts": [], "ship_parts": []}

    nodes = content.find_all(["h2", "h3", "p"])

    in_section = False
    current_h3: str | None = None
    current_texts: list[str] = []
    sections: list[tuple[str, list[str]]] = []
    done = False  # 防止 flush 重复

    def flush():
        if current_h3 and current_texts:
            sections.append((current_h3, current_texts[:]))

    for node in nodes:
        tag = node.name
        # 优先从 mw-headline span 取标题文字（排除"编辑"链接噪音）
        headline = node.find("span", class_="mw-headline")
        text = normalize_ws(headline.get_text() if headline else node.get_text())

        if tag == "h2":
            if "舰船相关" in text:
                in_section = True
                continue
            elif in_section:
                flush()
                done = True
                break

        if not in_section:
            continue

        if tag == "h3":
            flush()
            current_h3 = text
            current_texts = []
        elif tag == "p":
            md_text = node_to_md(node)
            if md_text:
                current_texts.append(md_text)

    if not done:
        flush()  # 最后一节（未遇到终止 H2 时）

    class_parts: list[tuple[str, list[str]]] = []
    ship_parts: list[tuple[str, list[str]]] = []

    for h3, texts in sections:
        # 若 H3 标题包含舰级名（或舰级名包含 H3 标题），归为舰级内容
        if ship_class and (ship_class in h3 or h3 in ship_class):
            class_parts.append((h3, texts))
        else:
            ship_parts.append((h3, texts))

    return {"class_parts": class_parts, "ship_parts": ship_parts}


def build_class_markdown(class_name: str, wiki_url: str,
                          class_parts: list[tuple[str, list[str]]]) -> str:
    """生成舰级独立 md 文件内容。"""
    lines = [
        "---",
        f"wiki: {wiki_url}",
        "---",
        "",
        f"# {class_name}",
        "",
    ]
    for h3, texts in class_parts:
        lines.append(f"### {h3}")
        lines.append("")
        for t in texts:
            lines.append(t)
            lines.append("")
    return "\n".join(lines)


# ── 辅助 ──────────────────────────────────────────────────────────────────────

def obtain_method(info: dict) -> str:
    methods = []
    bt = info.get("build_time", "")
    if bt and bt not in ("无", ""):
        methods.append("建造")
    if info.get("normal_drop"):
        methods.append("普通掉落")
    if info.get("event_drop"):
        methods.append("活动掉落")
    if info.get("other_obtain"):
        other = info["other_obtain"]
        if "活动" in other or "Pt" in other:
            methods.append("活动")
    return "、".join(methods) if methods else "未知"


# ── 生成 Markdown ─────────────────────────────────────────────────────────────

def build_markdown(
    name: str,
    wiki_url: str,
    info: dict,
    header: dict,
    stats: dict,
    skills: list[dict],
    portrait: str,
    ship_parts: list[tuple[str, list[str]]] | None = None,
) -> str:
    ship_class = header.get("ship_class", "")
    ship_number = header.get("ship_number", "")
    aliases = header.get("aliases", [])

    # ── Frontmatter ──
    aliases_yaml = "".join(f"  - {a}\n" for a in aliases)
    fm = (
        "---\n"
        f'class: "[[{ship_class}]]"\n'
        f"number: {ship_number}\n"
        "aliases:\n"
        f"{aliases_yaml}"
        f"wiki: {wiki_url}\n"
        "---"
    )

    # ── 头像 ──
    img_line = (
        f'<img align="right" src="{portrait}" width="150">' if portrait else ""
    )

    # ── 标题 ──
    if ship_class and ship_number:
        title = f"# **{ship_class}{ship_number}** {name}"
    elif ship_class:
        title = f"# **{ship_class}** {name}"
    else:
        title = f"# {name}"

    # ── 游戏参数表 ──
    ship_type = info.get("ship_type", "")
    type_icon = info.get("ship_type_icon", "")
    faction = info.get("faction", "")
    faction_icon = info.get("faction_icon", "")
    rarity = info.get("rarity", "")
    number = info.get("number", "")
    obtain = obtain_method(info)

    type_cell = f"![{ship_type}]({type_icon}) {ship_type}" if type_icon else ship_type
    faction_cell = (
        f"![{faction}]({faction_icon}) {faction}" if faction_icon else faction
    )

    params_table = (
        "## 游戏参数\n\n"
        "| 属性       | 数值                                                                                                                                       |\n"
        "| -------- | ---------------------------------------------------------------------------------------------------------------------------------------- |\n"
        f"| **编号**    | {number}                                                                                                                                   |\n"
        f"| **稀有度**  | {rarity}                                                                                                                                    |\n"
        f"| **舰种**   | {type_cell} |\n"
        f"| **阵营**   | {faction_cell} |\n"
        f"| **获取途径** | {obtain}                                                                                                                                     |"
    )

    # ── 技能 ──
    skill_lines = ["### 技能\n"]
    for i, sk in enumerate(skills, 1):
        skill_lines.append(f"{i}. **{sk['name']}**：{sk['desc']}  \n  ")
    skills_md = "\n".join(skill_lines)

    # ── 性能雷达图 (Obsidian Charts 插件格式) ──
    # 评级 → 数值: S=100, A=85, B=65, C=45, D=25, E=10
    grade_vals = [
        GRADE_MAP.get(stats.get(f"{s}_grade", "E"), 10) for s in STAT_ORDER
    ]
    radar_data = ", ".join(str(v) for v in grade_vals)

    radar = (
        "### 性能雷达图\n\n"
        "```chart\n"
        "type: radar\n"
        "labels: [耐久, 炮击, 雷击, 航空, 防空, 机动]\n"
        "series:\n"
        "  - title: 性能\n"
        f"    data: [{radar_data}]\n"
        "width: 80%\n"
        "beginAtZero: true\n"
        "```"
    )

    # ── 数值参数表 ──
    stat_rows = ""
    for s in STAT_ORDER:
        init_v = stats.get(f"{s}_init", "—")
        max_v = stats.get(f"{s}_max", "—")
        grade = stats.get(f"{s}_grade", "—")
        stat_rows += f"| {s} | {init_v} | {max_v} | {grade} |\n"

    num_table = (
        "### 数值参数\n\n"
        "| 属性 | 初始 | 满级 | 评级 |\n"
        "| -- | -- | -- | -- |\n"
        + stat_rows.rstrip()
    )

    # ── 历史介绍 ──
    history_lines = ["## 历史介绍", ""]
    if ship_parts:
        for h3, texts in ship_parts:
            history_lines.append(f"### {h3}")
            history_lines.append("")
            for t in texts:
                history_lines.append(t)
                history_lines.append("")
    else:
        history_lines.append("")
    history_md = "\n".join(history_lines)

    # ── 组装 ──
    sections = [
        fm,
        img_line,
        "",
        title,
        "",
        "> （游戏评价待填写）",
        "",
        "---",
        "",
        params_table,
        "",
        skills_md,
        "",
        "---",
        "",
        radar,
        "",
        num_table,
        "",
        "---",
        "",
        history_md,
        "",
        "---",
        "",
        "## 游戏定位",
        "",
    ]
    return "\n".join(sections)


# ── 入口 ──────────────────────────────────────────────────────────────────────

def main() -> None:
    if len(sys.argv) < 2:
        print("用法: uv run warship.py <舰娘名>")
        print("示例: uv run warship.py 普林斯顿")
        sys.exit(1)

    name = sys.argv[1]
    print(f"正在抓取: {name}")

    soup, wiki_url = fetch_page(name)

    header = parse_header(soup, name)
    info = parse_info(soup)
    stats = parse_stats(soup)
    skills = parse_skills(soup)
    portrait = get_portrait(soup, name)

    ship_class = header.get("ship_class", "")
    history = parse_history(soup, ship_class)

    md = build_markdown(
        name, wiki_url, info, header, stats, skills, portrait,
        ship_parts=history["ship_parts"],
    )

    out_dir = Path(__file__).parent
    out = out_dir / f"{name}.md"
    action = "更新" if out.exists() else "创建"
    out.write_text(md, encoding="utf-8")
    print(f"已{action}: {out}")

    # ── 舰级独立文件（仅在不存在时创建）──
    if history["class_parts"] and ship_class:
        class_file = out_dir / f"{ship_class}.md"
        if not class_file.exists():
            class_md = build_class_markdown(ship_class, wiki_url, history["class_parts"])
            class_file.write_text(class_md, encoding="utf-8")
            print(f"已创建舰级文件: {class_file}")
        else:
            print(f"舰级文件已存在，跳过: {class_file.name}")
    print(
        f"  舰种: {info.get('ship_type', '?')}  "
        f"阵营: {info.get('faction', '?')}  "
        f"稀有度: {info.get('rarity', '?')}"
    )
    if any(f"{s}_grade" in stats for s in STAT_ORDER):
        grades = " ".join(
            f"{s}:{stats.get(f'{s}_grade', '?')}" for s in STAT_ORDER
        )
        print(f"  性能: {grades}")
    if skills:
        print(f"  技能: {', '.join(sk['name'] for sk in skills)}")


if __name__ == "__main__":
    main()
