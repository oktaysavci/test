import instaloader

def linkten_indir():
    loader = instaloader.Instaloader()

    try:
        with open("linkler.txt", "r", encoding="utf-8") as file:
            links = file.readlines()
    except FileNotFoundError:
        print("❌ linkler.txt bulunamadı.")
        return

    for link in links:
        link = link.strip()
        if "/p/" in link or "/reel/" in link or "/tv/" in link:
            try:
                shortcode = link.split("/")[-2]
                post = instaloader.Post.from_shortcode(loader.context, shortcode)
                loader.download_post(post, target="indirilenler")
                print(f"✅ İndirildi: {link}")
            except Exception as e:
                print(f"❌ İndirilemedi: {link} - Hata: {e}")

def kullanicidan_indir():
    loader = instaloader.Instaloader()

    kullanici_adi = input("👤 Hedef Instagram kullanıcı adını girin: ").strip()
    sessionid = input("🔑 Instagram sessionid çerezinizi girin: ").strip()

    # SessionID ile giriş yap
    try:
        loader.context._session.cookies.set("sessionid", sessionid)
        loader.context._session.headers.update({"User-Agent": "Mozilla/5.0"})
    except Exception as e:
        print(f"❌ SessionID yüklenemedi: {e}")
        return

    # Kullanıcının video postlarını indir
    try:
        profil = instaloader.Profile.from_username(loader.context, kullanici_adi)
        for gonderi in profil.get_posts():
            if gonderi.is_video:
                loader.download_post(gonderi, target=f"{kullanici_adi}_videolar")
                print(f"✅ Video indirildi: https://www.instagram.com/p/{gonderi.shortcode}/")
    except Exception as e:
        print(f"❌ Kullanıcıdan içerik indirilemedi: {e}")

def menu():
    print("📥 Instagram İçerik İndirici")
    print("1 - linkler.txt dosyasından indir")
    print("2 - Belirli kullanıcının videolarını indir (sessionid gereklidir)")
    secim = input("Seçiminiz (1/2): ").strip()

    if secim == "1":
        linkten_indir()
    elif secim == "2":
        kullanicidan_indir()
    else:
        print("❌ Geçersiz seçim!")

if __name__ == "__main__":
    menu()
