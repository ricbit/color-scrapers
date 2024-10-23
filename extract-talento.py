import cv2
import re
import csv
import os
import sys
import math
from PIL import Image
import pytesseract

files = [
    ("talento/game.png", "Acrylic Color Game"),
    ("talento/modelismo1.png", "Acrylic Color Modelismo"),
    ("talento/modelismo2.png", "Acrylic Color Modelismo"),
    ("talento/metallic1.png", "Acrylic Color Metallic"),
    ("talento/artes1.png", "Acrylic Color Artes"),
    ("talento/artes2.png", "Acrylic Color Artes"),
    ("talento/metallic2.png", "Acrylic Color Artes Metallic"),
    ("talento/speed.png", "Speed"),
]

def traverse():
  for file_name, paint_type in files:
    image = Image.open(file_name)
    w, h = image.size
    dw, dh = 168, 139
    sw, sh = math.floor(w / dw + 0.5), math.floor(h / dh + 0.5)
    for j in range(sh):
      for i in range(sw):
        # Calculate the coordinates of the sub-image
        left = i * dw
        upper = j * dh
        right = min((i + 1) * dw, w)  # Ensure we don't go out of bounds
        lower = min((j + 1) * dh, h)
        
        # Crop the sub-image
        sub_image = image.crop((left, upper, right, lower))
        mw, mh = sub_image.size
        rgb = sub_image.getpixel((mw // 2, mh // 2))[:3]
        yield (rgb, pytesseract.image_to_string(sub_image), paint_type)

with open("talento.csv", "w", newline="") as csv_file:
  writer = csv.writer(csv_file)
  for rgb, text, ptype in traverse():
    text = " ".join(text.split("\n"))
    text = re.sub(r"\s+"," ", text).strip()
    text = re.search(r"(?P<code>\w+)\s+(?P<name>.*)", text)
    if text:
      row = [text.group("name"), text.group("code"), ptype, *rgb, "#%02X%02X%02X" % rgb]
      print(row)
      writer.writerow(row)
      
