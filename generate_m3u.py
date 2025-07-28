import json
from datetime import datetime

def generate_entry(channel):
    return f"""#KODIPROP:inputstream.adaptive.license_type=clearkey
#KODIPROP:inputstream.adaptive.license_key={{ "keys":[ {{ "kty":"oct", "k":"{channel['license_key']}", "kid":"{channel['kid']}" }} ], "type":"temporary" }}
#EXTINF:-1 tvg-id="{channel['name']}" tvg-name="{channel['name']}" tvg-logo="{channel['logo']}" group-title="Astro",{channel['name']}
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Linux; Android 14; ...) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Mobile Safari/537.36
https://linearjitp-playback.astro.com.my/dash-wv/linear/{channel['channel_id']}/default_ott.mpd
"""

def main():
    with open("astro_channels.json", "r", encoding="utf-8") as f:
        channels = json.load(f)

    m3u_content = "#EXTM3U\n"
    for channel in channels:
        m3u_content += generate_entry(channel) + "\n"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    m3u_content += f"# Generated on {timestamp}\n"

    with open("output/astro.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)

    print("✅ astro.m3u 已生成")

if __name__ == "__main__":
    main()
