# Hakka_news_crawler

python: 3.10.11

## Installation

You can use pyenv and venv to create python environment.
Need to instll ffmpeg first and set the Path.
Then, `poetry install` to add package

## Usage

1. You can use [Youtube List](https://jolantahuba.github.io/YT-Backup/) to get youtube playlist csv file and name `url.csv`.
2. Create a folder and set `target_dir`.
3. Set `os.environ["IMAGEIO_FFMPEG_EXE"]` path to your ffmpeg.
4. Run `crawler.ipynb` to get all mp4 file.

## Result

`mp4` folder will save the video with only sound.
`mp3` folder will save the whole audio.
`description` folder will save the audio which success to cut.
`train.csv` save the description audio and it text.
`fail.txt` save the vidoe which fail to convert.
