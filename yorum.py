import requests
import json
import time

# Kullanıcıdan giriş bilgilerini al
sessionid = input("Instagram sessionid çerezini girin: ")
shortcode = input("Instagram gönderi kısa kodunu girin (): ")

# Başlangıç değişkenleri
comments = []
end_cursor = None  # Sayfalama için cursor
retry_count = 0  # Hata tekrar deneme sayacı
max_retries = 3  # Maksimum tekrar deneme sayısı

while True:
    try:
        # API URL (GraphQL endpoint)
        variables = {"shortcode": shortcode, "first": 100}  # 50 yerine 100 yorum çekiyoruz
        if end_cursor:
            variables["after"] = end_cursor  # Sayfalama varsa ekle
        
        url = f"https://www.instagram.com/graphql/query/?query_hash=97b41c52301f77ce508f55e66d17620e&variables={json.dumps(variables)}"

        # Headers ve çerezleri ayarla
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": f"https://www.instagram.com/p/{shortcode}/"
        }
        cookies = {"sessionid": sessionid}

        # HTTP isteğini gönder
        response = requests.get(url, headers=headers, cookies=cookies)

        # Yanıtı kontrol et
        if response.status_code == 200 and response.text.strip():  # Boş yanıt kontrolü
            data = json.loads(response.text)  # Burada boş yanıt hatasını önlüyoruz
            edges = data["data"]["shortcode_media"]["edge_media_to_parent_comment"]["edges"]

            for comment in edges:
                username = comment["node"]["owner"]["username"]
                text = comment["node"]["text"]
                comments.append(f"{username}: {text}")

            # Sayfalama kontrolü
            page_info = data["data"]["shortcode_media"]["edge_media_to_parent_comment"]["page_info"]
            if page_info["has_next_page"]:
                end_cursor = page_info["end_cursor"]  # Yeni sayfa için cursor
                print(f"⚡ {len(comments)} yorum alındı, 3 saniye bekleniyor...")
                time.sleep(3)  # API limitine yakalanmamak için bekleme süresi azaldı
            else:
                break  # Tüm yorumlar çekildi
        else:
            print(f"⚠ API Hatası! HTTP {response.status_code} - {response.text}")
            retry_count += 1
            if retry_count >= max_retries:  # 3 kez hata alırsa işlemi durdur
                print("❌ API hataları devam ediyor, işlemi durduruyorum.")
                break
            print("🔄 Hata alındı, 2 saniye bekleniyor ve tekrar deneniyor...")
            time.sleep(2)  # Daha hızlı yeniden deneme
    except json.JSONDecodeError:
        print("⚠ Instagram boş veya geçersiz yanıt döndürdü, tekrar deneniyor...")
        retry_count += 1
        if retry_count >= max_retries:
            print("❌ Maksimum hata sınırına ulaşıldı, işlemi durduruyorum.")
            break
        time.sleep(2)
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")
        break

# Yorumları dosyaya kaydet
with open("yorumlar.txt", "w", encoding="utf-8") as file:
    for comment in comments:
        file.write(comment + "\n")

print(f"✅ {len(comments)} yorum başarıyla kaydedildi: yorumlar.txt")
            
