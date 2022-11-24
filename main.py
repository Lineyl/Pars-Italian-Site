import requests
from bs4 import BeautifulSoup
import openpyxl
import json
import os

def det(soup_link):
    t = ""
    for i in soup_link.find("div", class_="mrg10T mrg10B").find_all("p"):
        t += i.text+" | "
    return t
#for Exel
# def P_p(soup_link):
#     P = 0
#     Par = [j.text for j in soup_link.find("div", class_="mrg10B").find_all("div", class_="th")]
#     d = []
#     for i in soup_link.find("div", class_="mrg10B").find_all("div", class_="tr"):
#         d.append(f'{Par[P]} : {i.find("div", class_="td").text}')
#         P += 1

#    return d
#for json
def P_p(soup_link):
    P = 0
    Par = [j.text for j in soup_link.find("div", class_="mrg10B").find_all("div", class_="th")]
    d = {}
    for i in soup_link.find("div", class_="mrg10B").find_all("div", class_="tr"):
        d[Par[P]] = i.find("div", class_="td").text
        P += 1
    return d


data = {}
id = 1
P_n = 0
head = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "sec-ch-ua": '.Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103',
    "sec-ch-ua-platform": '"Windows"'
}
for page in range(7):
    print(page)
    res = requests.get(f"https://www.homesoverseas.ru/eng/search/?userid=13480&type=all&p={page}",
                       headers=head)

    soup = BeautifulSoup(res.text, "lxml")
    list_apart = soup.find('div', class_="block_list").find_all('div', class_="oh")
    for link in list_apart:
        url = "https://www.homesoverseas.ru" + link.find("a", class_="pic").get("href")
        res_link = requests.get(url, headers=head)
        soup_link = BeautifulSoup(res_link.text, "lxml")
        data[f"id_{id}"] = {
            "ID": soup_link.find("div", class_="line").findNext("div", class_="line").text.strip()[4:11],
            "Description": soup_link.find("div", class_="clear mrg10B mrg10T").find("h1").text,
            "Sale": soup_link.find("div", class_="price").find("div", class_="num").find("strong").text.strip()[0:6] + " €",
            "Sales text": soup_link.find("div", class_="blockquote line").text,
            "Property parameters and options": P_p(soup_link),
            "Detailed description": det(soup_link),

        }


        list_pr_keys = [i for i in data[f"id_{id}"]["Property parameters and options"].keys()]
        list_pr_values = [i for i in data[f"id_{id}"]["Property parameters and options"].values()]
        data[f"id_{id}"].pop("Property parameters and options")
        list_key = [i for i in data[f"id_{id}"].keys()]
        list_value = [i for i in data[f"id_{id}"].values()]
        for k in range(len(list_pr_keys)):
            list_key.insert(k+4, list_pr_keys[k])
        for v in range(len(list_pr_values)):
            list_value.insert(v+4, list_pr_values[v])


        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.append(list_key)
        sheet.append(list_value)

        os.mkdir(f"C:/Users/user/PycharmProjects/Kombarov/Scalea/{id}_apartment_ID_{data[f'id_{id}']['ID']}_")
        wb.save(f"C:/Users/user/PycharmProjects/Kombarov/Scalea/{id}_apartment_ID_{data[f'id_{id}']['ID']}_/{data[f'id_{id}']['ID']}_.xlsx")

        list_photo = soup_link.find_all("div", id="fotorama")
        for photo_link in list_photo:
            id_photo = 1
            ph = photo_link.find_all("a")
            for photo_url in ph:
                ur = photo_url.get("href")
                res_photo = requests.get(ur, headers=head).content
                with open(f"C:/Users/user/PycharmProjects/Kombarov/Scalea/{id}_apartment_ID_{data[f'id_{id}']['ID']}_/{id_photo}_photo.jpg", "wb") as ph_file:
                    ph_file.write(res_photo)
                id_photo+=1


        P_n += 1
        id+=1
        #print(data[f"id_{id}"])
# with open(f"main.json","w") as file:
#     json.dump(data, file, ensure_ascii=False, indent=2)
