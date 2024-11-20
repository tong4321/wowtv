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

# 1. İlk isteği gönder ve yönlendirmeyi takip et
response_initial = requests.get(new_url, headers=headers, allow_redirects=True)
if response_initial.status_code == 200:
    final_url = response_initial.url  # Yönlendirilmiş URL'yi al
    print(f"Yönlendirilmiş Son URL: {final_url}")
else:
    print(f"İlk istekte hata oluştu: {response_initial.status_code}")
    exit()

# 2. Yönlendirilmiş URL'ye istek gönder
response_redirect = requests.get(final_url, headers=headers)

# 3. Meta refresh tag'ini parse et
soup = BeautifulSoup(response_redirect.text, 'html.parser')
meta_refresh_tag = soup.find('meta', attrs={'http-equiv': 'refresh'})

if meta_refresh_tag:
    # Meta tag'den URL'yi al
    meta_content = meta_refresh_tag.get('content', '')
    url_match = re.search(r'URL=(https?://[^\s]+)', meta_content, re.IGNORECASE)
    if url_match:
        base_url = url_match.group(1)
        print(f"Yönlendirme URL'si: {base_url}")

        # 4. Yayın 1 URL'sine istek gönder
        yayin1_url = f"{base_url}/channel.html?id=yayin1"
        response_yayin1 = requests.get(yayin1_url, headers=headers)

        if response_yayin1.status_code == 200:
            print(f"Yayın 1 URL başarılı: {yayin1_url}")

            # 5. Script tag'lerden baseurl değerini bul
            soup_yayin1 = BeautifulSoup(response_yayin1.text, 'html.parser')
            script_tags = soup_yayin1.find_all('script')

            extracted_baseurl = None
            for script in script_tags:
                if script.string:
                    match = re.search(r'var baseurl\s*=\s*"([^"]+)"', script.string)
                    if match:
                        extracted_baseurl = match.group(1).rstrip('/')
                        print(f"Base URL bulundu: {extracted_baseurl}")
                        break

            if extracted_baseurl:
                # 6. M3U dosyasını güncelle
                m3u_file_path = "t.m3u"
                old_baseurl_pattern = r"https://[^/]+(?=/yayin\w+\.m3u8)"

                try:
                    with open(m3u_file_path, 'r') as file:
                        m3u_content = file.read()

                    updated_m3u_content = re.sub(old_baseurl_pattern, extracted_baseurl, m3u_content)

                    with open(m3u_file_path, 'w') as file:
                        file.write(updated_m3u_content)

                    print("M3U dosyası başarıyla güncellendi.")
                except Exception as e:
                    print(f"M3U dosyasını güncellerken hata oluştu: {e}")
            else:
                print("Base URL değeri bulunamadı.")
        else:
            print(f"Yayın 1 URL'sine erişilemedi, hata kodu: {response_yayin1.status_code}")
    else:
        print("Meta tag içinde geçerli bir URL bulunamadı.")
else:
    print("Meta refresh etiketi bulunamadı.")
