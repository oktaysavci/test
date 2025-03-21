import requests
import json
import time
from datetime import datetime, timezone

# Kullanıcıdan giriş bilgilerini al
sessionid = input("Instagram sessionid çerezini girin: ")
shortcode = input("Instagram gönderi kısa kodunu girin (örn: DD7srGYoj2F): ")

# Kullanıcıya seçim yaptır
print("\nSeçenekler:")
print("1- Tam Arama (Tüm yorumları kaydeder)")
print("2- Kullanıcı Adı ile Arama (Sadece belirli bir kişinin yorumlarını kaydeder)")
secim = input("Seçiminizi yapın (1 veya 2): ")

if secim == "2":
    target_username = input("Hangi kullanıcının yorumlarını bulmak istiyorsunuz?: ")
else:
    target_username = None

# API URL (GraphQL endpoint)
base_url = "https://www.instagram.com/graphql/query/"
query_hash = "97b41c52301f77ce508f55e66d17620e"
first = 20  # Küçük parçalarda yorum çekiyoruz
after = None  # Yorum sayfası ilerleme token'ı

# Headers ve çerezleri ayarla
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": f"https://www.instagram.com/p/{shortcode}/"
}
cookies = {"sessionid": sessionid}

count_total = 0  # Toplam çekilen yorum sayısı
count_saved = 0  # Kaydedilen yorum sayısı
TIMEOUT = 30  # Zaman aşımı süresi 30 saniye

# Yorumları kaydetmek için dosyayı aç
with open("yorumlar.txt", "w", encoding="utf-8") as file:
    while True:
        variables = {"shortcode": shortcode, "first": first}
        if after:
            variables["after"] = after

        url = f"{base_url}?query_hash={query_hash}&variables={json.dumps(variables)}"

        response = requests.get(url, headers=headers, cookies=cookies, timeout=TIMEOUT)

        if response.status_code != 200:
            print(f"⚠ Hata! HTTP {response.status_code} - {response.text}")
            break

        data = response.json()
        comments = data["data"]["shortcode_media"]["edge_media_to_parent_comment"]["edges"]
        page_info = data["data"]["shortcode_media"]["edge_media_to_parent_comment"]["page_info"]
        after = page_info["end_cursor"] if page_info["has_next_page"] else None

        for comment in comments:
            username = comment["node"]["owner"]["username"]
            text = comment["node"]["text"]
            timestamp = comment["node"]["created_at"]  # Unix zaman damgası

            # Unix timestamp'i okunabilir tarihe çevir
            comment_time = datetime.fromtimestamp(timestamp, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

            if target_username:  # Kullanıcı adı ile arama yapılıyorsa
                if username == target_username:
                    file.write(f"{comment_time} - {username}: {text}\n")  # Anlık olarak dosyaya yaz
                    file.flush()  # Dosya yazma işlemini zorla
                    print(f"🔍 {comment_time} - {username}: {text}")  # Kullanıcının yorumunu ekrana yazdır
                    count_saved += 1  # Kaydedilen yorum sayısını artır
            else:  # Tam arama yapılıyorsa tüm yorumları kaydet
                file.write(f"{comment_time} - {username}: {text}\n")
                file.flush()  # Dosya yazma işlemini zorla
                count_saved += 1  # Kaydedilen yorum sayısını artır

        count_total += len(comments)
        print(f"✅ {count_total} yorum çekildi, {count_saved} yorum kaydedildi...")

        if count_total >= 500 and count_total % 500 < first:
            print(f"⏳ {count_total} yorum çekildi, 30 saniye bekleniyor...")
            time.sleep(30)

        if not after:
            print("🚀 Daha fazla yorum yok. İşlem tamamlandı.")
            break

        time.sleep(5)

print(f"🎉 Toplam {count_total} yorum çekildi, {count_saved} yorum kaydedildi: yorumlar.txt")
