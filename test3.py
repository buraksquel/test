import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def verileri_cekme(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    etiket = soup.find("div", {"class": "p"})
    return etiket.text.strip() if etiket else "Kısa açıklama bulunamadı."

def google_news(News):
    base_url = f"https://news.google.com/home?hl=tr&gl=TR&ceid=TR:tr={News}"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "html.parser")

    haber_listesi = []

    haberler = soup.find_all("div", class_="VCnfNe")

    for sıralama, haber_bilgisi in enumerate(haberler, start=1):
        world_link_relative = haber_bilgisi.find("a", {"class": "brSCsc", "aria-label": "Dünya"}).get("href")
        world_link_absolute = urljoin(base_url, world_link_relative)
        world_response = requests.get(world_link_absolute)
        world_soup = BeautifulSoup(world_response.content, "html.parser")

        world_source = world_soup.find("div", {"class": "a7P8l"}).text.strip()
        world_title = world_soup.find("a", class_="gPFEn").text.strip()

        world_comment_relative = world_soup.find("a", class_="gPFEn").get("href")
        world_comment_absolute = urljoin(world_link_absolute, world_comment_relative)
        
      
        kisa_aciklama = verileri_cekme(world_comment_absolute)

        world_date_time = world_soup.find("time", class_="hvbAAd").get("datetime")
        world_url = world_soup.find("a", class_="WwrzSb").get("href")

        haber_bilgi = {
            "sıralama": sıralama,
            "baslik": world_title,
            "kısa_acıklama": kisa_aciklama,
            "kaynak": world_source,
            "tarih_zaman": world_date_time,
            "url": world_url
        }

        haber_listesi.append(haber_bilgi)

    return haber_listesi

dunya_haberleri = google_news("News")

for haber in dunya_haberleri:
    print("Sıralama:", haber["sıralama"])
    print("Başlık:", haber["baslik"])
    print("Kısa Açıklama:", haber["kısa_acıklama"])
    print("Kaynak:", haber["kaynak"])
    print("Tarih/Zaman:", haber["tarih_zaman"])
    print("URL:", haber["url"])
    print("***********************************")





        spor = haber_bilgisi.find("a", {"class": "brSCsc", "aria-label": "Spor"}).get("href")
        




    """work = haber_bilgisi.find("a", {"class": "brSCsc", "aria-label": "İş"}).get("href")






        health = haber_bilgisi.find("a", {"class": "brSCsc", "aria-label": "Sağlık"}).get("href")"""









