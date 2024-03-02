import requests
from bs4 import BeautifulSoup

def kısa_acıklama_cek(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    p_etiketi = soup.find("p")
    return p_etiketi.text if p_etiketi else "Kısa açıklama bulunamadı."

def google_news(News):
    base_url = f"https://news.google.com/home?hl=tr&gl=TR&ceid=TR:tr{News}"
    response = requests.get(base_url)
    html_icerigi = response.content
    soup = BeautifulSoup(html_icerigi, "html.parser")

    haber_listesi = []

   
    if "spor" in News.lower():
        kategori = "Spor"
        baslik_prefix = "Spor Verileri: "
    elif "sağlık" in News.lower():
        kategori = "Sağlık"
        baslik_prefix = "Sağlık Verileri: "
    elif "iş" in News.lower():
        kategori = "İş"
        baslik_prefix = "İş Verileri: "
    elif "dünya" in News.lower():
        kategori = "Dünya"
        baslik_prefix = "Dünya Verileri: "
    else:
       
        print("Geçersiz kategori.")
        return

    haberler = soup.find_all("div", class_="f9uzM")

    for siralama, haber_bilgisi in enumerate(haberler, start=1):
        kaynak = haber_bilgisi.find("div", {"class":"a7P8l"}).text.strip()
        baslik = haber_bilgisi.find("a", class_="gPFEn").text.strip()
        kısa_acıklama_url = haber_bilgisi.find("a", class_="gPFEn").get("href")
        tarih_zaman = haber_bilgisi.find("time", class_="hvbAAd").get("datetime")
        url = haber_bilgisi.find("a", class_="WwrzSb").get("href")

        full_url = f"https://news.google.com{kısa_acıklama_url}"
        kısa_acıklama = kısa_acıklama_cek(full_url)

        haber_bilgi = {
            "siralama": siralama,
            "kategori": kategori,
            "baslik": baslik,
            "kısa_acıklama": kısa_acıklama,
            "kaynak": kaynak,
            "tarih_zaman": tarih_zaman,
            "url": url
        }

        haber_listesi.append(haber_bilgi)

    for haber in haber_listesi:
        print(f"{baslik_prefix}Sıralama: {haber['siralama']}")
        print(f"{baslik_prefix}Kategori: {haber['kategori']}")
        print(f"{baslik_prefix}Başlık: {haber['baslik']}")
        print(f"{baslik_prefix}Kısa Açıklama: {haber['kısa_acıklama']}")
        print(f"{baslik_prefix}Kaynak: {haber['kaynak']}")
        print(f"{baslik_prefix}Tarih/Zaman: {haber['tarih_zaman']}")
        print(f"{baslik_prefix}URL: {haber['url']}")
        print("***********************************")


google_news("spor")
google_news("sağlık") 
google_news("iş")
google_news("dünya")
