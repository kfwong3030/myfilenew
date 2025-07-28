import os

# 示例频道列表（你可以替换为从 API 或网页抓取的内容）
channels = [
    {
        "id": "astro_awani",
        "name": "Astro Awani",
        "logo": "https://example.com/logo/awani.png",
        "group": "News",
        "url": "http://stream.example.com/awani.m3u8"
    },
    {
        "id": "astro_ria",
        "name": "Astro Ria",
        "logo": "https://example.com/logo/ria.png",
        "group": "Entertainment",
        "url": "http://stream.example.com/ria.m3u8"
    }
]

def generate_m3u_content(channels):
    lines = ["#EXTM3U"]
    for channel in channels:
        lines.append(
            f"#EXTINF:-1 tvg-id=\"{channel['id']}\" tvg-name=\"{channel['name']}\" "
            f"tvg-logo=\"{channel['logo']}\" group-title=\"{channel['group']}\",{channel['name']}"
        )
        lines.append(channel['url'])
    return "\n".join(lines)

new_content = generate_m3u_content(channels)

# 如果文件已存在，读取旧内容
if os.path.exists("playlist.m3u"):
    with open("playlist.m3u", "r", encoding="utf-8") as f:
        old_content = f.read()
else:
    old_content = ""

# 只有内容变更才写入
if new_content != old_content:
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("[✓] M3U 文件已更新：playlist.m3u")
else:
    print("[ℹ️] M3U 文件无变更，跳过写入")
