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
  d = sum(abs(a-b) for a,b in zip(image.getpixel((0, h-1)), image.getpixel((w-1, 00))))
  text = pytesseract.image_to_string(image)
  text = re.search(r"NM\s*(?P<code>\d+)", text)
  if text is None:
    text = ""
  else:
    text = "NM%s" % text.group("code")
  if d <= 3:
    return image.getpixel((w // 2, h * 40 // 100))[:3], text
  else:
    return image.getpixel((w - 1, 0))[:3], text

def decode_rgb(rgb):
  return tuple(int(rgb[1 + x * 2 : 3 + x * 2], 16) for x in range(3))



def parse_url(url, writer):
  silverb_text = requests.get(url).text
  silverb_page = BS(silverb_text, "html.parser")
  gallery = silverb_page.find("div", class_="catalog-content")
  for color_link in gallery.find_all("div", class_="product"):
    name = color_link.find("div", class_="product-name")
    name = re.search(r" - (?P<name>.*) 30ml", name.text).group("name")
    alink = color_link.find("a", class_="space-image")
    img = alink.find("img", class_="second-image")
    if img is None:
      rgb, code = (0,0,0), ""
    else:
      url = img.get("data-src")
      rgb, code = middle_color(url)
    row = [name, code, "Aquacolor", *rgb, "#%02X%02X%02X" % rgb]
    writer.writerow(row)
    print(row)

with open("silverb.csv", "w", newline="") as csv_file:
  writer = csv.writer(csv_file)
  url = "https://www.mercadorpg.com.br/pintura/silverbright?loja=599593&categoria=903&categories%5B%5D=Tintas+Aquacolor"
  parse_url(url, writer)
  url = "https://www.mercadorpg.com.br/pintura/silverbright?loja=599593&categoria=903&categories%5B%5D=Tintas+Aquacolor&pg=2"
  parse_url(url, writer)


