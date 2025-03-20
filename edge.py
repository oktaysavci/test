from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time

# Kullanıcıdan giriş bilgilerini al
USERNAME = input("Instagram Kullanıcı Adı: ")
PASSWORD = input("Instagram Şifresi: ")
TARGET_USERNAME = input("Mesaj göndermek istediğin kişinin kullanıcı adı: ")
MESSAGE_TEXT = input("Göndermek istediğin mesaj: ")

# Edge WebDriver'ı başlat
options = webdriver.EdgeOptions()
options.add_argument("start-maximized")  # Tarayıcıyı tam ekran aç

# Edge WebDriver yolunu al
driver_path = EdgeChromiumDriverManager().install()

# WebDriver'ı başlat
driver = webdriver.Edge(executable_path=driver_path, options=options)

# Instagram'a giriş yap
driver.get("https://www.instagram.com/accounts/login/")
time.sleep(5)  # Sayfanın yüklenmesini bekle

# Kullanıcı adı ve şifreyi gir
username_input = driver.find_element(By.NAME, "username")
password_input = driver.find_element(By.NAME, "password")

username_input.send_keys(USERNAME)
password_input.send_keys(PASSWORD)
password_input.send_keys(Keys.RETURN)

time.sleep(10)  # Giriş işleminin tamamlanmasını bekle

# DM kutusuna git
driver.get("https://www.instagram.com/direct/inbox/")
time.sleep(5)

# Yeni mesaj butonuna bas
new_message_button = driver.find_element(By.XPATH, "//div[text()='Yeni mesaj']")
new_message_button.click()
time.sleep(3)

# Kullanıcıyı arat
search_box = driver.find_element(By.XPATH, "//input[@placeholder='Ara...']")
search_box.send_keys(TARGET_USERNAME)
time.sleep(3)

# Kullanıcıyı seç
first_result = driver.find_element(By.XPATH, f"//div[contains(text(), '{TARGET_USERNAME}')]")
first_result.click()
time.sleep(3)

# İleri butonuna bas
next_button = driver.find_element(By.XPATH, "//div[text()='İleri']")
next_button.click()
time.sleep(5)

# Mesajı yaz ve gönder
message_box = driver.find_element(By.TAG_NAME, "textarea")
message_box.send_keys(MESSAGE_TEXT)
message_box.send_keys(Keys.RETURN)

time.sleep(3)  # Mesajın gönderilmesini bekle

print("✅ Mesaj başarıyla gönderildi!")

# Tarayıcıyı kapat
driver.quit()
