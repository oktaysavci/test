from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Kullanıcı bilgilerini al
username = input("Instagram kullanıcı adınızı girin: ")
password = input("Instagram şifrenizi girin: ")
post_url = input("Instagram gönderi URL’sini girin: ")

# Chrome WebDriver başlat
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.instagram.com/accounts/login/")

# Giriş yap
time.sleep(3)
driver.find_element(By.NAME, "username").send_keys(username)
driver.find_element(By.NAME, "password").send_keys(password + Keys.RETURN)

time.sleep(7)

driver.get(post_url)
time.sleep(5)

for i in range(20):  # Yeterli yorum yüklenene kadar artırılabilir
    try:
        load_more_button = driver.find_element(By.XPATH, "//span[contains(text(),'Yorumları gör')]")
        load_more_button.click()
        time.sleep(2)
    except:
        break

# Tüm yorumları al
comments = driver.find_elements(By.XPATH, "//ul[@class='_a9ym']/div/li/div/div/div/div/span")

# Yorumları dosyaya kaydet
with open("yorumlar.txt", "w", encoding="utf-8") as file:
    for comment in comments:
        file.write(comment.text + "\n")

print(f"✅ {len(comments)} yorum başarıyla kaydedildi: yorumlar.txt")

# Tarayıcıyı kapat
driver.quit()
