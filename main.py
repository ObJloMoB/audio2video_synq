import os

import numpy as np
from scipy import signal

from pydub import AudioSegment
from moviepy.editor import VideoFileClip, AudioFileClip

import argparse

# import matplotlib.pyplot as plt


def get_np_data(path, start=600.0, dur=5.0, fr=48000):
    data = AudioSegment.from_file(path, start_second=start, duration=dur)
    data = data.set_frame_rate(fr)
    data_mono = data.split_to_mono()[0]

    # fn = os.path.basename(path)
    # fn = os.path.splitext(fn)[0]
    # data_mono.export(f'{fn}.wav', format='wav')

    data_np = np.array(data_mono.get_array_of_samples())
    return data_np


def get_delay(ref, sig, fr):
    corr = signal.correlate(sig, ref, mode='full') / len(ref)

    delay_arr = np.linspace(-1 * len(ref)/fr,
                            len(ref)/fr,
                            2 * len(ref) + 1)

    idx = np.argmax(corr)
    delay = delay_arr[idx]

    # x = np.linspace(0, corr.shape[0], corr.shape[0])
    # plt.plot(x, corr)
    # plt.savefig("some_graph.png")

    return delay


def combine(audio_p, video_p, delay):
    video = VideoFileClip(video_p)
    audio = AudioFileClip(audio_p)

    if delay > 0:
        audio = audio.subclip(t_start=delay)
    else:
        video = video.subclip(t_start=abs(delay))

    video = video.set_audio(audio)
    fn = os.path.splitext(video_p)[0]
    video.write_videofile(f'{fn}_res.mp4')


def main(args):
    # Read audio data as np arrays
    sec_duration = args.min_duration * 60.0
    vid_np = get_np_data(args.video,
                         args.sec_start,
                         sec_duration,
                         args.resample_fr)
    audio_np = get_np_data(args.audio,
                           args.sec_start,
                           sec_duration,
                           args.resample_fr)

    # Normalize to [-1, 1] range
    coef = max([*abs(vid_np), *abs(audio_np)])
    vid_np = vid_np / coef
    audio_np = audio_np / coef

    # Get delay from cross corelation
    print('Synq started')
    delay = get_delay(vid_np, audio_np, args.resample_fr)
    print(f'Delay {delay} sec')

    # Write final video
    print('Final encode started')
    combine(args.audio, args.video, delay)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--video', default='data/test0_video.mp4')
    parser.add_argument('--audio', default='data/test0_audio.mp3')
    parser.add_argument('--sec_start', default=0.0, type=float)
    parser.add_argument('--min_duration', default=15.0, type=float)
    parser.add_argument('--resample_fr', default=16000)

    args = parser.parse_args()

    main(args)
