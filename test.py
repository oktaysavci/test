from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time

# Kullanıcıdan bilgileri al
USERNAME = input("Instagram kullanıcı adınızı girin: ")
PASSWORD = input("Instagram şifrenizi girin: ")
POST_URL = input("Instagram gönderi URL’sini girin: ")

# Microsoft Edge WebDriver başlat
options = webdriver.EdgeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)

# 1️⃣ Instagram'a giriş yap
driver.get("https://www.instagram.com/accounts/login/")
time.sleep(5)

# Kullanıcı adı ve şifreyi gir
driver.find_element(By.NAME, "username").send_keys(USERNAME)
driver.find_element(By.NAME, "password").send_keys(PASSWORD)
driver.find_element(By.NAME, "password").send_keys(Keys.ENTER)
time.sleep(10)  # Girişin tamamlanmasını bekle

print("✅ Giriş başarılı! Çerezleri manuel olarak onaylayın ve Enter'a basın.")
input()  # Kullanıcı çerezleri onayladıktan sonra devam edecek

# 2️⃣ Gönderiye git
driver.get(POST_URL)
time.sleep(5)

# 3️⃣ Tüm yorumları yükleme fonksiyonu
def load_all_comments():
    while True:
        try:
            load_more = driver.find_element(By.XPATH, "//span[contains(text(),'Yorumları gör')]")
            load_more.click()
            time.sleep(2)
        except:
            break  # Daha fazla yorum butonu yoksa çık

load_all_comments()
time.sleep(3)

# 4️⃣ Tüm yorumları al
comments = driver.find_elements(By.XPATH, "//ul[@class='_a9ym']/div/li/div/div/div/div/span")

# 5️⃣ Yorumları dosyaya kaydet
with open("yorumlar.txt", "w", encoding="utf-8") as file:
    for comment in comments:
        file.write(comment.text + "\n")

print(f"✅ {len(comments)} yorum başarıyla kaydedildi: yorumlar.txt")

# 6️⃣ Tarayıcıyı kapat
driver.quit()
