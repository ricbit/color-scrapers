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

def parse_colors(url, writer):
  daiara_text = requests.get(url).text
  daiara_page = BS(daiara_text, "html.parser")
  gallery = (daiara_page.find("div", class_="atributos").find("ul"))
  colors = {}
  for color_link in gallery.find_all("li"):
    color = color_link.find("a")
    en_name = color.get("data-variacao-nome")
    rgb = re.search(r"color: (?P<color>#.*?);", color.find("span").get("style")).group("color")
    colors[color.get("data-variacao-id")] = [en_name, rgb]
  for color_link in daiara_page.find_all("div", class_="acoes-produto"):
    for cl in color_link.get("class"):
      if cl.startswith("SKU"):
        code = color_link.get("data-variacao-id")
        if code in colors and len(colors[code]) < 3:
          color_id, name = cl.rsplit("-", 1)
          colors[code].extend([color_id, name])
  for en_name, rgb, code, pt_name in colors.values():
    rgb = decode_rgb(rgb)
    row = ["%s (%s)" % (en_name, pt_name), code, "Top Colors", *rgb, "#%02X%02X%02X" % rgb]
    writer.writerow(row)
    print(row)

with open("daiara.csv", "w", newline="") as csv_file:
  writer = csv.writer(csv_file)
  url_light = "https://www.daiarastore.com/tinta-acrilica-top-colors-60ml-tons-claros"
  parse_colors(url_light, writer)
  url_light = "https://www.daiarastore.com/tinta-acrilica-top-colors-60ml-tons-escuros"
  parse_colors(url_light, writer)


