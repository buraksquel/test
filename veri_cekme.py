import requests
from bs4 import BeautifulSoup

def dünya_kısa_acıklama_cek(url):
    # Verilen URL'den içeriği çekiyorum
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    # Sayfadaki ilk <p> etiketini bul ve metnini alıyorum
    p_etiketi = soup.find("p")
    return p_etiketi.text if p_etiketi else "Kısa açıklama bulunamadı."
    # test

def google_haber_dünya_haber_cekici(Dünya):
    # Google Haberler'in Dünya kategorisine giderek sayfa içeriğini çekiyorum
    base_url = f"https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FuUnlHZ0pVVWlnQVAB?hl=tr&gl=TR&ceid=TR%3Atr&topic={Dünya}"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "html.parser")

    haber_listesi = []

    # Dünya'daki Tüm haber bilgilerini aldım
    haberler = soup.find_all("div", class_="f9uzM")

    for siralama, haber_bilgisi in enumerate(haberler, start=1):
        # Her bir haberin kaynağı, başlığı, kısa açıklaması URL'si, tarihi/zamanı ve tam URL'si
        kaynak = haber_bilgisi.find("div", {"class":"a7P8l"}).text.strip()
        baslik = haber_bilgisi.find("a", class_="gPFEn").text.strip()
        kısa_acıklama_url = haber_bilgisi.find("a", class_="gPFEn").get("href")
        tarih_zaman = haber_bilgisi.find("time", class_="hvbAAd").get("datetime")
        url = haber_bilgisi.find("a", class_="WwrzSb").get("href")

        # Kısa açıklama URL'sini tam bir URL olarak oluşturdum
        full_url = f"https://news.google.com{kısa_acıklama_url}"

        # kısa_acıklama_cek fonksiyonu ile içeriği çektim
        kısa_acıklama = dünya_kısa_acıklama_cek(full_url)

        # Her bir haber bilgisini sözlük olarak kaydettim
        haber_bilgi = {
            "siralama": siralama,
            "baslik": baslik,
            "kısa_acıklama": kısa_acıklama,
            "kaynak": kaynak,
            "tarih_zaman": tarih_zaman,
            "url": url
        }

        # Haber listesini ekledim
        haber_listesi.append(haber_bilgi)

    return haber_listesi

# Dünya haberlerini çekip ekrana yazdırdım
dunya_haberleri = google_haber_dünya_haber_cekici("Dünya")
for haber in dunya_haberleri:
    print("Sıralama:", haber["siralama"])
    print("Başlık:", haber["baslik"])
    print("Kısa_acıklama:", haber["kısa_acıklama"])
    print("Kaynak:", haber["kaynak"])
    print("Tarih/Zaman:", haber["tarih_zaman"])
    print("URL:", haber["url"])
    print("***********************************")