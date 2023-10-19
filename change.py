import os
import pydub
import moviepy.editor as mpeditor


dir = "./Hakka_ge30_slice/"
target = "./Hakka_ge30_fin/"
for file in os.scandir(dir):
    print(file.name)
    try:
        audio = mpeditor.AudioFileClip(dir + file.name)
        audio1 = audio.subclip(0, audio.duration / 2)
        audio2 = audio.subclip(audio.duration / 2, audio.duration)
        audio1.write_audiofile(filename=target + "tmp_file1.wav", fps=16000, nbytes=2, logger=None)
        audio.write_audiofile(filename=target + "tmp_file2.wav", fps=16000, nbytes=2, logger=None)
        sound = pydub.AudioSegment.from_wav(target + "tmp_file1.wav")
        sound = sound.set_channels(1)
        sound.export(target + file.name, format="wav")
        os.remove(target + "tmp_file1.wav")
        sound = pydub.AudioSegment.from_wav(target + "tmp_file2.wav")
        sound = sound.set_channels(1)
        sound.export(target + file.name, format="wav")
        os.remove(target + "tmp_file2.wav")
    except Exception as e:
        print(e)
        continue