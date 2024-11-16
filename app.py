import requests
from bs4 import BeautifulSoup
import re

# Yeni URL
new_url = 'https://onlineparakazanmak.org/trgoalsyeniadres.html'

# Başlangıç isteği için gerekli headers
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}

# Yeni URL'ye istek gönderme ve otomatik yönlendirmeyi takip etme
response = requests.get(new_url, headers=headers, allow_redirects=True)

# Yönlendirme sonrası son URL'yi alma
final_url = response.url
print(f"Yönlendirilmiş Son URL: {final_url}")

# Yönlendirilmiş URL'ye istek gönderme
response_href = requests.get(final_url, headers=headers)

# Meta refresh tag'ini parse etme
soup_href = BeautifulSoup(response_href.text, 'html.parser')
meta_tag_title = soup_href.find('meta', attrs={'http-equiv': 'refresh'})

if meta_tag_title:
    meta_tag_content = meta_tag_title.get('content')
    url = meta_tag_content.split('URL=')[-1]
    yayin1_url = f"{url}channel.html?id=yayin1"

    # Yeni URL'ye istek gönderme
    response_yayin1 = requests.get(yayin1_url, headers=headers)

    if response_yayin1.status_code != 200:
        print(f"Yayın 1 URL'sine erişilemedi, hata kodu: {response_yayin1.status_code}")
    else:
        # Script içeriğini parse etme
        soup_yayin1 = BeautifulSoup(response_yayin1.text, 'html.parser')
        script_tags = soup_yayin1.find_all('script')

        baseurl = None
        for script_tag in script_tags:
            # Script içeriğini alma
            script_content = script_tag.string
            if script_content:
                # baseurl değerini alma
                match = re.search(r'var baseurl\s*=\s*"([^"]+)"', script_content)
                if match:
                    baseurl = match.group(1)
                    baseurl = baseurl.rstrip('/')
                    break

        if not baseurl:
            print("Base URL değeri bulunamadı.")
        else:
            print(f"Base URL başarıyla bulundu: {baseurl}")

            # M3U dosyasını güncelleme
            m3u_file_path = "t.m3u"
            old_baseurl_pattern = r"https://[^/]+(?=/yayin\w+\.m3u8)"

            with open(m3u_file_path, 'r') as file:
                m3u_content = file.read()

            new_m3u_content = re.sub(old_baseurl_pattern, baseurl, m3u_content)

            with open(m3u_file_path, 'w') as file:
                file.write(new_m3u_content)

            print("M3U dosyası güncellendi.")
else:
    print("Meta Refresh etiketi bulunamadı.")
