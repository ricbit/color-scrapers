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

smooth3d_web = "https://smooth3d.com.br/tinta-acrilica-branca"

smooth3d_text = requests.get(smooth3d_web).text
smooth3d_page = BS(smooth3d_text, "html.parser")

with open("smooth3d.csv", "w", newline="") as csv_file:
  gallery = smooth3d_page.find_all("ul", class_="text-thumbs")
  writer = csv.writer(csv_file)
  for color_link in gallery[1].find_all("a"):
    style = color_link.get("style")
    rgb = re.search(r"background-color: (?P<color>.*?);", style).group("color")
    rgb = decode_rgb(rgb)
    smooth3d_name = color_link.get("data-color-name")
    smooth3d_code = ""
    print(smooth3d_code, smooth3d_name)
    row = [smooth3d_name, smooth3d_code, "Acrylic Paint", *rgb, "#%02X%02X%02X" % rgb]
    writer.writerow(row)
    print(row)



