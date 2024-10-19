import csv
import io
import re
import requests
from bs4 import BeautifulSoup as BS
from PIL import Image

acrilex_web = "https://acrilex.com.br/produto/linha-manualidades/produtos-para-artesanato/tinta-acrilica-fosca/"

acrilex_text = requests.get(acrilex_web).text
acrilex_page = BS(acrilex_text, "html.parser")

with open("acrilex.csv", "w", newline="") as csv_file:
  gallery = acrilex_page.find("div", class_="avia-gallery-thumb")
  writer = csv.writer(csv_file)
  for color_link in gallery.find_all("a"):
    color_url = color_link.get("href")
    acrilex_id = re.search(r"/(?P<code>\d{3})_(?P<name>.*?)(-\d+)?\.png", color_url)
    acrilex_code, acrilex_name = [acrilex_id.group(x) for x in ["code", "name"]]
    acrilex_name = acrilex_name.replace("_", " ").title()
    image = Image.open(io.BytesIO(requests.get(color_url).content))
    w, h = image.size
    rgb = image.getpixel((w // 2, h // 2))[:3]
    row = [acrilex_name, acrilex_code, "Acrilica Fosca", *rgb, "#%02X%02X%02X" % rgb]
    writer.writerow(row)
    print(row)



