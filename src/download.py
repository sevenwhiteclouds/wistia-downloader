# TODO: logging instead of printing
import logging
import urllib.request as req
import asyncio

CHARS_TO_H = 6
LINK_LINE_NUM = 63
TITLE_LINE_NUM = 7
END_TITLE_EXTENSION = 4
CHARS_TO_TITLE = 6
EMBED_URL = "http://fast.wistia.net/embed/iframe/"

# TODO: really need to handle cases where video is not able to download. try blocks, maybe.
# this expects the video id to download
async def downloader(vid_id, progress, progress_size):
  event_loop = asyncio.get_event_loop()

  vid_id = vid_id.rstrip()

  html = await event_loop.run_in_executor(None, req.urlopen, EMBED_URL + vid_id)
  html = await event_loop.run_in_executor(None, html.read)

  # the video is found at line 63 in the html that is returned. 63 is defined in global const
  video_link = html.decode().split("\n")[LINK_LINE_NUM]
  # http:// begins after finding "url" and then skipping 6 chars. 6 is defined in global const
  start = video_link.find("url") + CHARS_TO_H
  end = video_link.find(".bin", start) 
  video_link = video_link[start : end] + ".mp4"

  # grabbing the video title
  video_title = html.decode().split("\n")[TITLE_LINE_NUM]
  # title begins after finding "video/" and then skipping 6 chars. 6 is defined in global const
  start = video_title.find("video/") + CHARS_TO_TITLE
  # don't need the extension or anything else, only need title
  end = video_title.rfind('"') - END_TITLE_EXTENSION
  video_title = video_title[start : end] + ".mp4"

  # this is the video download
  video = await event_loop.run_in_executor(None, req.urlopen, video_link)

  file_write = await event_loop.run_in_executor(None, open, video_title, "wb")

  while True:
    chunk = await event_loop.run_in_executor(None, video.read, 1_000_000)
    if not chunk:
      break

    await event_loop.run_in_executor(None, file_write.write, chunk)

  progress[0] = progress[0] + 1
  print(f"{video_title} (id: {vid_id}) downloaded! [{progress[0]}/{progress_size}]")
  await event_loop.run_in_executor(None, file_write.close)

# if running as a module, this expects a list of video ids to be passed in
async def main(ids):
  # used for tracking how many vidoes have downloaded based on the length of ids passed in
  progress = [0];

  async with asyncio.TaskGroup() as tasks:
    for vid_id in ids:
      tasks.create_task(downloader(vid_id, progress, len(ids)))

    print("Downloads have started. Completed video downloads will appear below...\n")

  print("All videos have been downloaded!")

if __name__ == "__main__":
  print("The txt file containing the IDs must be in the same directory as this program!")
  file = input("Enter file name: ")

  with open(file, "r") as file_open:
    ids = file_open.readlines()

  asyncio.run(main(ids))
