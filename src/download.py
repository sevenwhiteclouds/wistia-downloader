import urllib.request as request
import asyncio

EMBED_URL = "http://fast.wistia.net/embed/iframe/"
LINE_NUM = 63
CHARS_TO_H = 6

async downloader():
  print("Hello, World!")

# if running as a module, this expects a list to be passed in
async def main(ids):
  async with asyncio.TaskGroup() as tasks:
    for vid_id in ids:
      tasks.create_task(downloader())

  print("All videos have been downloaded!")

if __name__ == "__main__":
  print("The txt file containing the IDs must be in the same directory as this program!")
  file = input("Enter file name: ")
  print()

  with open(file, "r", encoding="utf-8") as file_open:
    ids = file_open.readlines()

  asyncio.run(main(ids))

  # keeps track of the video downloaded out of the total videos
  #video_num = 1

  ## TODO: really need to handle cases where video is not able to download. try blocks, maybe.
  #for id in ids:
  #  id = id.rstrip()
  #  print(f"Downloading video ID [{video_num}/{len(ids)}]: {id}... ", end="", flush=True)

  #  # the video is found at line 63 in the html that is returned. 63 is defined in global const
  #  html = request.urlopen(EMBED_URL + id).read().decode("utf-8").split("\n")[LINE_NUM]

  #  # http:// begins after finding "url" and then skipping 6 chars. 6 is defined in global const
  #  link_start = html.find("url") + CHARS_TO_H
  #  link_end = html.find(".bin", link_start) 

  #  video_link = html[link_start : link_end] + ".mp4"
  #  video = request.urlopen(video_link)

  #  with open((id + ".mp4"), "wb") as save_video:
  #    save_video.write(video.read())

  #  print("done!")
  #  video_num += 1
