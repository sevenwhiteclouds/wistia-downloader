import urllib.request as req
import asyncio

CHARS_TO_H = 6
LINE_NUM = 63
EVENT_LOOP = asyncio.get_event_loop()
EMBED_URL = "http://fast.wistia.net/embed/iframe/"

# this expects the video id to download
## TODO: really need to handle cases where video is not able to download. try blocks, maybe.
async def downloader(vid_id):
  vid_id = vid_id.rstrip()
  write_file = await EVENT_LOOP.run_in_executor(None, open, f"{vid_id}.mp4", "wb")

  # the video is found at line 63 in the html that is returned. 63 is defined in global const
  html = await EVENT_LOOP.run_in_executor(None, req.urlopen, EMBED_URL + vid_id)
  html = await EVENT_LOOP.run_in_executor(None, html.read)
  html.close()
  html = html.decode().split("\n")[LINE_NUM]

  # # http:// begins after finding "url" and then skipping 6 chars. 6 is defined in global const
  link_start = html.find("url") + CHARS_TO_H
  link_end = html.find(".bin", link_start) 

  video_link = html[link_start : link_end] + ".mp4"
  video = await EVENT_LOOP.run_in_executor(None, req.urlopen, video_link)

  while True:
    chunk = await EVEN_LOOP.run_in_executor(None, video.read, 1_000_000)
    if not chunk:
      break

    await EVENT_LOOP.run_in_executor(write_file.write(chunk))

# if running as a module, this expects a list of video ids to be passed in
async def main(ids):
  async with asyncio.TaskGroup() as tasks:
    for vid_id in ids:
      tasks.create_task(downloader(vid_id))

  print("All videos have been downloaded!")

if __name__ == "__main__":
  print("The txt file containing the IDs must be in the same directory as this program!")
  file = input("Enter file name: ")
  print()

  with open(file, "r", encoding="utf-8") as file_open:
    ids = file_open.readlines()

  asyncio.run(main(ids))
