# generate_m3u.py
import datetime

def generate_m3u_entry(channel_name, logo_url, mpd_url, license_key, kid):
    return f"""#KODIPROP:inputstream.adaptive.license_type=clearkey
#KODIPROP:inputstream.adaptive.license_key={{ "keys":[ {{ "kty":"oct", "k":"{license_key}", "kid":"{kid}" }} ], "type":"temporary" }}
#EXTINF:-1 tvg-id="{channel_name}" tvg-name="{channel_name}" tvg-logo="{logo_url}" group-title="Chinese",{channel_name}
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Linux; Android 14; ...) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Mobile Safari/537.36
{mpd_url}
"""

def main():
    channels = [
        {
            "name": "TVB Classic",
            "logo": "https://divign0fdw3sv.cloudfront.net/Images/ChannelLogo/contenthub/425_144.png",
            "mpd": "https://linearjitp-playback.astro.com.my/dash-wv/linear/5016/default_ott.mpd",
            "license_key": "kzric7Fmuqj7ID7vGnrb3w",
            "kid": "BxRIaQoOybJ+ssGn1eAwEA"
        }
    ]

    with open("myfile.m3u", "w", encoding="utf-8") as f:
        f.write(f"# 更新日期：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        for ch in channels:
            f.write(generate_m3u_entry(**ch) + "\n")

if __name__ == "__main__":
    main()
