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

decorfix_web = "https://www.corfix.com.br/decorfix-fosca-2/"

decorfix_text = requests.get(decorfix_web).text
decorfix_page = BS(decorfix_text, "html.parser")

with open("decorfix.csv", "w", newline="") as csv_file:
  gallery = decorfix_page.find("div", id="produto-single")
  writer = csv.writer(csv_file)
  for color_link in gallery.find_all("div", class_="box_cor"):
    color = color_link.find("h2").text
    decorfix_id = re.search(r"(?P<name>\w.*?)\s(?P<code>\d{3})( -)?", color)
    decorfix_code, decorfix_name = [decorfix_id.group(x) for x in ["code", "name"]]
    print(decorfix_code, decorfix_name)
    style = color_link.find("div", class_="cor").get("style")
    rgb = re.search(r"background: (?P<color>.*)", style).group("color")
    if rgb.startswith("url"):
      url = re.search(r"\((?P<url>.*)\)", rgb).group("url")
      rgb = "#%02x%02x%02x" % middle_color(url)
    rgb = decode_rgb(rgb)
    row = [decorfix_name, decorfix_code, "Decorfix Fosca", *rgb, "#%02X%02X%02X" % rgb]
    writer.writerow(row)
    print(row)



