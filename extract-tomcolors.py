import csv
import io
import re
import requests
from bs4 import BeautifulSoup as BS
from PIL import Image

def middle_color(url):
  image = Image.open(io.BytesIO(requests.get(url).content))
  w, h = image.size
  return image.getpixel((w // 2, h // 2))[:3]

def decode_rgb(rgb):
  return tuple(int(rgb[1 + x * 2 : 3 + x * 2], 16) for x in range(3))

tomcolors_web = "https://www.tomcolors.com.br/up"

tomcolors_text = requests.get(tomcolors_web).text
tomcolors_page = BS(tomcolors_text, "html.parser")

with open("tomcolors.csv", "w", newline="") as csv_file:
  gallery = tomcolors_page.find("div", class_="showcase-catalog")
  writer = csv.writer(csv_file)
  for color_link in gallery.find_all("div", class_="product"):
    color = color_link.find("div", class_="product-name")
    if not color.text.startswith("TCUP"):
      continue
    tomcolors_id = re.search(r"(?P<code>TCUP-\d{2})\s(?P<name>.*)", color.text)
    tomcolors_code, tomcolors_name = [tomcolors_id.group(x) for x in ["code", "name"]]
    print(tomcolors_code, tomcolors_name)
    a_link = color_link.find("a", class_="space-image")
    all_img = a_link.find_all("img")
    url = all_img[1].get("data-src")
    print(all_img)
    rgb = "#%02x%02x%02x" % middle_color(url)
    rgb = decode_rgb(rgb)
    row = [tomcolors_name, tomcolors_code, "Ultra Pigmentada", *rgb, "#%02X%02X%02X" % rgb]
    writer.writerow(row)
    print(row)



