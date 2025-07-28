import requests
import re
import json

def fetch_valid_channels(m3u_url):
    response = requests.get(m3u_url)
    if response.status_code != 200:
        raise Exception(f"下载失败，状态码：{response.status_code}")

    lines = response.text.splitlines()
    channels = []
    channel = {}

    for line in lines:
        line = line.strip()

        if line.startswith("#KODIPROP:inputstream.adaptive.license_key="):
            channel["license"] = {
                "type": "clearkey",
                "key": "your_base64_key_here",
                "kid": "your_base64_kid_here"
            }

        elif line.startswith("#EXTINF"):
            match = re.search(
                r'tvg-id="([^"]+)" tvg-name="([^"]+)" tvg-logo="([^"]+)" group-title="([^"]+)",(.+)',
                line
            )
            if match:
                channel["id"] = match.group(1)
                channel["name"] = match.group(2)
                channel["logo"] = match.group(3)
                channel["group"] = match.group(4)

        elif line.startswith("http") and ".mpd" in line:
            try:
                test = requests.head(line, timeout=5)
                if test.status_code == 200:
                    channel["url"] = line
                    channels.append(channel)
            except:
                pass
            channel = {}

    return channels

if __name__ == "__main__":
    m3u_url = "https://raw.githubusercontent.com/kfwong3030/autobot/refs/heads/main/myfile.m3u"
    valid_channels = fetch_valid_channels(m3u_url)

    with open("astro_channels.json", "w", encoding="utf-8") as f:
        json.dump(valid_channels, f, indent=2, ensure_ascii=False)

    print(f"✅ 已成功生成 astro_channels.json，共 {len(valid_channels)} 个有效频道")
