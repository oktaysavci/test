import psutil
import platform
from datetime import datetime

# İşletim sistemi bilgileri
system_info = platform.uname()
print("İşletim Sistemi:", system_info.system)
print("Sürüm:", system_info.release)
print("Platform:", system_info.version)
print("Makine Adı:", system_info.node)
print("Mimari:", system_info.machine)

# CPU bilgileri
print("\nCPU:")
print("Fiziksel Çekirdek Sayısı:", psutil.cpu_count(logical=False))
print("Toplam Çekirdek Sayısı:", psutil.cpu_count(logical=True))
print("CPU Frekansı:", psutil.cpu_freq().current, "MHz")
print("CPU Yüzde Kullanımı:", psutil.cpu_percent(interval=1), "%")

# Bellek (RAM) bilgileri
memory_info = psutil.virtual_memory()
print("\nRAM:")
print("Toplam RAM:", round(memory_info.total / (1024 ** 3), 2), "GB")
print("Kullanılan RAM:", round(memory_info.used / (1024 ** 3), 2), "GB")
print("Boş RAM:", round(memory_info.available / (1024 ** 3), 2), "GB")
print("RAM Kullanım Yüzdesi:", memory_info.percent, "%")

# Disk bilgileri
print("\nDisk:")
disk_info = psutil.disk_usage('/')
print("Toplam Disk:", round(disk_info.total / (1024 ** 3), 2), "GB")
print("Kullanılan Disk:", round(disk_info.used / (1024 ** 3), 2), "GB")
print("Boş Disk:", round(disk_info.free / (1024 ** 3), 2), "GB")
print("Disk Kullanım Yüzdesi:", disk_info.percent, "%")

# Ağ bilgileri
print("\nAğ:")
net_info = psutil.net_if_addrs()
for interface, addresses in net_info.items():
    for address in addresses:
        if address.family == psutil.AF_INET:
            print(f"{interface} - IP Adresi: {address.address}, Netmask: {address.netmask}")
