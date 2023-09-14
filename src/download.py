import urllib.request as request
import json

EMBED_URL = "http://fast.wistia.net/embed/iframe/"

if __name__ == "__main__":
  file = input("Enter file name: ")

  with open(file, "r", encoding="utf-8") as file_open:
    lines = file_open.readlines()

  http = request.urlopen(EMBED_URL + lines[0].rstrip()).read().decode("utf-8")

