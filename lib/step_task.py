import os


import cv2
import PIL
import pydub
import pytesseract
import moviepy.editor as mpeditor
import moviepy.video.fx.all as mpfx


import lib.util as util


def get_subtitle(in_path, out_path):
    video = cv2.VideoCapture(in_path)
    total_frame = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video.get(cv2.CAP_PROP_FPS)
    subtitle = open(out_path, "w")

    pre_text = ""
    duration_time = []
    start_time = 0
    end_time = 0
    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    for i in range(total_frame):
        success, img = video.read()
        if not success:
            break
        
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);
        ret, img = cv2.threshold(img, 240, 255, cv2.THRESH_BINARY)
        img = cv2.bitwise_not(img)  

     
        img = cv2.erode(img, kernel3)
        img = cv2.dilate(img, kernel2)

        # cv2.imshow("video", img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        img = PIL.Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        text = pytesseract.image_to_string(img, lang='chi_tra', config="--psm 7")

        text = util.cleartext(text)

        if util.text_is_differ(text, pre_text):
            if not util.is_space(pre_text):
                end_time = round(i / fps, 2)
                subtitle.write("\"" + str(start_time) + "-" + str(end_time) + "\",\"" + pre_text + "\"\n")
                duration_time.append([start_time, end_time])
            start_time = round(i / fps, 2)


        pre_text = text

    if not util.is_space(text):
        end_time = round(total_frame / fps, 2)
        subtitle.write(str(start_time) + "~" + str(end_time) + ":" + pre_text + "\n")
        duration_time.append([start_time, end_time])

    
    subtitle.close()
    return duration_time


def processing(idx, video, video_fps, target_dir):
    print(idx, video.title, "running")
    tmp_video = target_dir + "/mp4/tmp" + str(idx) + ".mp4"
    mp4_path = target_dir + "/mp4/" + str(idx) + ".mp4"
    wav_path = target_dir + "/wav/" + str(idx) + ".wav"
    txt_path = target_dir + "/csv/" + str(idx) + ".csv"

    if not os.path.isfile(mp4_path):
        try:
            video.streams.filter().get_highest_resolution().download(filename="tmp" + str(idx) + ".mp4", output_path=target_dir + "/mp4")
            mp4 = mpeditor.VideoFileClip(tmp_video)
            mp4 = mpfx.crop(mp4, x1=350, y1=550, width=600, height=50)
            mp4 = mp4.subclip(0, mp4.duration - 2)
            mp4.write_videofile(filename=mp4_path, fps=video_fps, logger=None)
            os.remove(tmp_video)

        except:
            print(video.title, " cant downlaod")
            failfile = open(target_dir + "/fail.txt", "a")
            failfile.write(video.title + " cant downlaod.\n")
            failfile.close()
            return
    

    if not os.path.isfile(wav_path):
        try:
            audio = mpeditor.AudioFileClip(mp4_path)
            audio.write_audiofile(filename=wav_path, fps=16000, nbytes=2, logger=None)
            sound = pydub.AudioSegment.from_wav(wav_path)
            sound = sound.set_channels(1)
            sound.export(wav_path, format="wav")
        except:
            print(video.title, " cant convert")
            failfile = open(target_dir + "/fail.txt", "a")
            failfile.write(video.title + " cant convert.\n")
            failfile.close()
            return 

    
    if not os.path.isfile(txt_path):
        try:
            get_subtitle(mp4_path, txt_path)
        except:
            print(video.title, " cant get subtitle")
            failfile = open(target_dir + "/fail.txt", "a")
            failfile.write(video.title + "  get subtitle.\n")
            failfile.close()
            return
        
    print(idx, "success")
