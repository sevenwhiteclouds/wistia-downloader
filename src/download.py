import urllib.request as request

EMBED_URL = "http://fast.wistia.net/embed/iframe/"

if __name__ == "__main__":
  file = input("Enter file name: ")

  with open(file, "r", encoding="utf-8") as file_open:
    lines = file_open.readlines()

  # TODO: this should be a try block
  # the video is found at line 63 in the html that is returned
  html = request.urlopen(EMBED_URL + lines[0].rstrip()).read().decode("utf-8").split("\n")[63]

  link_start = html.find("url") + 6
  link_end = html.find(".bin", link_start) 

  video_link = html[link_start : link_end] + ".mp4"

  print(video_link)
