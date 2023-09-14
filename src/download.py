import urllib.request as request

EMBED_URL = "http://fast.wistia.net/embed/iframe/"

if __name__ == "__main__":
  print("The txt file containing the IDs must be in the same directory as this program!")
  file = input("Enter file name: ")
  print()

  with open(file, "r", encoding="utf-8") as file_open:
    lines = file_open.readlines()

  for line in lines:
    # TODO: this should probably really be a try block
    # the video is found at line 63 in the html that is returned
    line = line.rstrip()
    print("Downloading video ID: " + line + "... ", end="", flush=True)

    html = request.urlopen(EMBED_URL + line).read().decode("utf-8").split("\n")[63]

    link_start = html.find("url") + 6
    link_end = html.find(".bin", link_start) 

    video_link = html[link_start : link_end] + ".mp4"
    video = request.urlopen(video_link)

    with open((line + ".mp4"), "wb") as save_video:
      save_video.write(video.read())
    print("done!")
