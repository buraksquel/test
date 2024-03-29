import requests
from bs4 import BeautifulSoup

def kısa_acıklama_cek(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    p_etiketi = soup.find("p")
    return p_etiketi.text if p_etiketi else "Kısa açıklama bulunamadı."

def google_news(News, dosya_adı):
    if "spor" in News.lower():
        kategori = "Spor"
        baslik_prefix = "Spor Verileri: "
        base_url = "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FuUnlHZ0pVVWlnQVAB?hl=tr&gl=TR&ceid=TR%3Atr"
    elif "sağlık" in News.lower():
        kategori = "Sağlık"
        baslik_prefix = "Sağlık Verileri: "
        base_url = "https://news.google.com/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNR3QwTlRFU0FuUnlLQUFQAQ?hl=tr&gl=TR&ceid=TR%3Atr"
    elif "iş" in News.lower():
        kategori = "İş"
        baslik_prefix = "İş Verileri: "
        base_url = "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FuUnlHZ0pVVWlnQVAB?hl=tr&gl=TR&ceid=TR%3Atr"
    elif "dünya" in News.lower():
        kategori = "Dünya"
        baslik_prefix = "Dünya Verileri: "
        base_url = "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FuUnlHZ0pVVWlnQVAB?hl=tr&gl=TR&ceid=TR%3Atr"
    else:
        print("Geçersiz kategori.")
        return

    response = requests.get(base_url)
    if response.status_code != 200:
        return
    html_icerigi = response.content
    soup = BeautifulSoup(html_icerigi, "html.parser")

    haberler = soup.find_all("div", class_="f9uzM")

    with open(dosya_adı, 'a', encoding='utf-8') as dosya: 
        for siralama, haber_bilgisi in enumerate(haberler, start=1):
            kaynak = haber_bilgisi.find("div", {"class": "a7P8l"}).text.strip()
            baslik = haber_bilgisi.find("a", class_="gPFEn").text.strip()
            kısa_acıklama_url = haber_bilgisi.find("a", class_="gPFEn").get("href")
            tarih_zaman = haber_bilgisi.find("time", class_="hvbAAd").get("datetime")
            url = haber_bilgisi.find("a", class_="WwrzSb").get("href")

            full_url = f"https://news.google.com{kısa_acıklama_url}"
            kısa_acıklama = kısa_acıklama_cek(full_url)

            dosya.write(f"{baslik_prefix}Sıralama: {siralama}\n")
            dosya.write(f"{baslik_prefix}Kategori: {kategori}\n")
            dosya.write(f"{baslik_prefix}Başlık: {baslik}\n")
            dosya.write(f"{baslik_prefix}Kısa Açıklama: {kısa_acıklama}\n")
            dosya.write(f"{baslik_prefix}Kaynak: {kaynak}\n")
            dosya.write(f"{baslik_prefix}Tarih/Zaman: {tarih_zaman}\n")
            dosya.write(f"{baslik_prefix}URL: {url}\n")
            dosya.write("***********************************\n")

google_news("spor", "spor_haberler.txt")
google_news("sağlık", "saglik_haberler.txt")
google_news("iş", "is_haberler.txt")
google_news("dünya", "dunya_haberler.txt")
