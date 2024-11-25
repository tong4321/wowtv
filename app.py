import requests

# Base URL'yi çekmek için istek yap
base_url_source = 'https://mehmetey3.serv00.net/gdomin.php'
try:
    response = requests.get(base_url_source)
    response.raise_for_status()
    base_url = response.text.strip()  # Gelen URL'yi temizle
except requests.RequestException as e:
    print(f"Base URL alınamadı: {e}")
    exit()

# Dinamik M3U dosyasını oluşturma
m3u_content = "#EXTM3U\n"

channels = [
    {
        'name': 'beIN Sports 1',
        'logo': 'https://raw.githubusercontent.com/scatterradarcsv/tv_app/main/kanal_logolari/bein1.png',
        'path': 'yayinzirve.m3u8'
    },
    {
        'name': 'beIN Sports 1',
        'logo': 'https://raw.githubusercontent.com/scatterradarcsv/tv_app/main/kanal_logolari/bein1.png',
        'path': 'yayin1.m3u8'
    }
]

for channel in channels:
    m3u_content += f"#EXTINF:0 tvg-name='{channel['name']}' tvg-logo='{channel['logo']}',{channel['name']}\n"
    m3u_content += "#EXTVLCOPT:http-referrer=https://trgoals957.xyz\n"
    m3u_content += "#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36\n"
    m3u_content += f"{base_url}/{channel['path']}\n"

# Dosyayı kaydet
file_name = 'metv.m3u'
try:
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(m3u_content)
    print(f"M3U dosyası başarıyla oluşturuldu: {file_name}")
except IOError as e:
    print(f"M3U dosyası oluşturulamadı: {e}")
