import os
import datetime
import subprocess
import requests

# ✅ Telegram Bot 设置（可选）
TELEGRAM_BOT_TOKEN = "your_bot_token"
TELEGRAM_CHAT_ID = "your_chat_id"

# ✅ 输出文件名
OUTPUT_FILE = "playlist.m3u"

# ✅ 频道列表（可自行扩展）
channels = [
    {
        "name": "Astro AEC",
        "url": "https://linearjitp-playback.astro.com.my/dash-wv/linear/5016/default_ott.mpd",
        "logo": "https://example.com/logo_aec.png"
    },
    {
        "name": "Astro Awani",
        "url": "https://linearjitp-playback.astro.com.my/dash-wv/linear/5004/default_ott.mpd",
        "logo": "https://example.com/logo_awani.png"
    }
]

# ✅ M3U 生成函数
def generate_m3u_entry(name, url, logo):
    return f'#EXTINF:-1 tvg-logo="{logo}",{name}\n{url}'

# ✅ 主函数
def main():
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for ch in channels:
            f.write(generate_m3u_entry(**ch) + "\n")

    print(f"[✓] M3U 文件已生成：{OUTPUT_FILE}")

    # ✅ GitHub 自动推送（可选）
    git_push()

    # ✅ Telegram 通知（可选）
    send_telegram_message(f"✅ M3U 更新完成：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ✅ GitHub 推送函数
def git_push():
    try:
        subprocess.run(["git", "add", OUTPUT_FILE], check=True)
        subprocess.run(["git", "commit", "-m", "Auto-update M3U"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("[✓] GitHub 推送成功")
    except subprocess.CalledProcessError as e:
        print(f"[✗] GitHub 推送失败：{e}")

# ✅ Telegram 通知函数
def send_telegram_message(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[!] Telegram 设置未配置")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("[✓] Telegram 通知已发送")
        else:
            print(f"[✗] Telegram 通知失败：{response.text}")
    except Exception as e:
        print(f"[✗] Telegram 异常：{e}")

# ✅ 执行主函数
if __name__ == "__main__":
    main()
