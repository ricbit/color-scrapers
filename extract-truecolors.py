import csv
import io
import re
import requests
import pytesseract
from bs4 import BeautifulSoup as BS
from PIL import Image

def middle_color(url):
  image = Image.open(io.BytesIO(requests.get(url).content))
  w, h = image.size
  text = pytesseract.image_to_string(image, lang="por")
  return image.getpixel((w // 2, h // 2))[:3], text

def decode_rgb(rgb):
  return tuple(int(rgb[1 + x * 2 : 3 + x * 2], 16) for x in range(3))

truecolors_web = "https://www.truecolors.com.br/portfolio/art-colors/"

truecolors_text = requests.get(truecolors_web).text
truecolors_page = BS(truecolors_text, "html.parser")

with open("truecolors.csv", "w", newline="") as csv_file:
  gallery = truecolors_page.find("div", class_="gallery")
  writer = csv.writer(csv_file)
  for color_link in gallery.find_all("img"):
    url = color_link.get("src")
    rgb, text = middle_color(url)
    text = text.replace("\n", " ").strip()
    text_r = re.search(r"(?P<code>\d{4})(?:,|\.)? (?P<name>.*)", text)
    if text_r is None:
      print(text)
      continue
    row = [text_r.group("name"), text_r.group("code"), "Art Colors", *rgb, "#%02X%02X%02X" % rgb]
    writer.writerow(row)
    print(row)



