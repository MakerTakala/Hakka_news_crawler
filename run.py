import os

import pytube
import multiprocessing

import lib.step_task as step_task


if __name__ == "__main__":
    os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/bin/ffmpeg"
    

    list_url = "https://www.youtube.com/playlist?list=PL96kIIcXJpMtmsQGlsNVqWduASZnh4HnE"
    target_dir = "/Users/takala/Documents/GitHub/Hakka_news_crawler/all_data"


    if not os.path.isdir(target_dir + "/mp4"):
        os.makedirs(target_dir + "/mp4")
    if not os.path.isdir(target_dir + "/wav"):
        os.makedirs(target_dir + "/wav")
    if not os.path.isdir(target_dir + "/txt"):
        os.makedirs(target_dir + "/txt")

    playlist = pytube.Playlist(list_url)
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() // 2)
    data = [(idx, video, 5, target_dir) for [idx, video] in enumerate(playlist.videos)]

    pool.starmap(step_task.processing, data)