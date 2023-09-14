import urllib.request as request

EMBED_URL = "http://fast.wistia.net/embed/iframe/"
LINE_NUM = 63
CHARS_TO_H = 6

# TODO: modularity - change this to work as a module as well, not just as a standalone program
if __name__ == "__main__":
  print("The txt file containing the IDs must be in the same directory as this program!")
  file = input("Enter file name: ")
  print()

  with open(file, "r", encoding="utf-8") as file_open:
    lines = file_open.readlines()

  # keeps track of the video downloaded out of the total videos
  video_num = 1

  # TODO: really need to handle cases where video is not able to download. try blocks, maybe.
  for line in lines:
    line = line.rstrip()
    print(f"Downloading video ID [{video_num}/{len(lines)}]: {line}... ", end="", flush=True)

    # the video is found at line 63 in the html that is returned. 63 is defined in global const
    html = request.urlopen(EMBED_URL + line).read().decode("utf-8").split("\n")[LINE_NUM]

    # http:// begins after finding "url" and then skipping 6 chars. 6 is defined in global const
    link_start = html.find("url") + CHARS_TO_H
    link_end = html.find(".bin", link_start) 

    video_link = html[link_start : link_end] + ".mp4"
    video = request.urlopen(video_link)

    with open((line + ".mp4"), "wb") as save_video:
      save_video.write(video.read())

    print("done!")
    video_num += 1
