# Audio to video synq

Just simple synq app to automaticly synqronize audio and video by cross-corelating audio. Usefull when you have bad quality audio inside videofile and just need to replace it with good audio from different recorder.

## Use
Install all you need.
```sh
pip install -r requirements.txt
```
 And pass video, audio and time frame to synq. Added sec_start and min_diration just to make synq take less time.
```sh
python main.py --video YOUR_VIDEO_PATH --audio YOUR_AUDIO_PATH --sec_start SECOND_IN_FILES_WHERE_SEARCH_STARTS --min_duration DURATION_OF_SEARCH_INTERVAL
```
For example if you want to check first 10 minutes of audio and video to find synq point
```sh
python main.py --video data/video.mp4 --audio data/audio.mp3 --sec_start 0.0 --min_duration 10.0
```
Result will appear next to original video.