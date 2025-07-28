import requests
import re
import json
import os

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
                "key": "your_base64_key_here",  # 可替换为真实 key
                "kid": "your_base64_kid_here"   # 可替换为真实 kid
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

def save_m3u(channels, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for ch in channels:
            f.write(f"""#KODIPROP:inputstream.adaptive.license_type=clearkey
#KODIPROP:inputstream.adaptive.license_key={{ "keys":[ {{ "kty":"oct", "k":"{ch['license']['key']}", "kid":"{ch['license']['kid']}" }} ], "type":"temporary" }}
#EXTINF:-1 tvg-id="{ch['id']}" tvg-name="{ch['name']}" tvg-logo="{ch['logo']}" group-title="{ch['group']}",{ch['name']}
{ch['url']}\n""")

if __name__ == "__main__":
    m3u_url = "https://raw.githubusercontent.com/kfwong3030/autobot/main/myfile.m3u"
    valid_channels = fetch_valid_channels(m3u_url)

    # 保存 JSON 到 output 文件夹
    os.makedirs("output", exist_ok=True)
    with open("output/astro_channels.json", "w", encoding="utf-8") as f:
        json.dump(valid_channels, f, indent=2, ensure_ascii=False)

    # 保存 M3U 到 output 文件夹
    save_m3u(valid_channels, "output/astro.m3u")

    print(f"✅ 已成功生成 output/astro_channels.json 和 output/astro.m3u，共 {len(valid_channels)} 个有效频道")
