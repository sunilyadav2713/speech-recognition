# -*- coding: utf-8 -*-
"""Speech_Recognition.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10LshESpnqYwFIp7H6Wce_svSjpStRLzb
"""

!pip install transformers

!pip install -U datasets

!pip install gradio

!pip install librosa

!pip install soundfile

from datasets import load_dataset

dataset=load_dataset("librispeech_asr",split='train.clean.100',streaming=True,trust_remote_code=True)

example = next(iter(dataset))

dataset_head = dataset.take(5)
list(dataset_head)

list(dataset_head) [2]

example

from IPython.display import Audio as IPythonAudio
IPythonAudio(example["audio"] ["array"],rate=example["audio"]["sampling_rate"])

from transformers import pipeline
asr = pipeline(task="automatic-speech-recognition",
               model="openai/whisper-large-v3")

asr.feature_extractor.sampling_rate

example ['audio'] ['sampling_rate']

asr(example["audio"]["array"])

example["text"]

import os
import gradio as gr

demo = gr.Blocks()

def transcribe_speech(filepath):
    if filepath is None:
        gr.Warning("No audio found, please retry.")
        return ""
    output = asr(filepath)
    return output["text"]

mic_transcribe = gr.Interface(
    fn=transcribe_speech,
    inputs=gr.Audio(sources="microphone",
                    type="filepath"),
    outputs=gr.Textbox(label="Transcription",
                       lines=3),
    allow_flagging="never")

file_transcribe = gr.Interface(
    fn=transcribe_speech,
    inputs=gr.Audio(sources="upload",
                    type="filepath"),
    outputs=gr.Textbox(label="Transcription",
                       lines=3),
    allow_flagging="never",
)

with demo:
    gr.TabbedInterface(
        [mic_transcribe,
         file_transcribe],
        ["Transcribe Microphone",
         "Transcribe Audio File"],
    )

demo.launch(debug=True)

demo.close()

import soundfile as sf
import io

audio, sampling_rate = sf.read('/gudilo_badilo_song.mp3')

sampling_rate

asr.feature_extractor.sampling_rate

audio.shape

import numpy as np

audio_transposed = np.transpose(audio)

audio_transposed.shape

import librosa

audio_mono = librosa.to_mono(audio_transposed)

IPythonAudio(audio_mono,
             rate=sampling_rate)

asr(audio_mono)

sampling_rate

asr.feature_extractor.sampling_rate

audio_16KHz = librosa.resample(audio_mono,
                               orig_sr=sampling_rate,
                               target_sr=16000)

asr(
    audio_16KHz,
    chunk_length_s=30, # 30 seconds
    batch_size=4,
    return_timestamps=True,
)["chunks"]

import gradio as gr
demo = gr.Blocks()

def transcribe_long_form(filepath):
    if filepath is None:
        gr.Warning("No audio found, please retry.")
        return ""
    output = asr(
      filepath,
      max_new_tokens=256,
      chunk_length_s=30,
      batch_size=8,
    )
    return output["text"]

mic_transcribe = gr.Interface(
    fn=transcribe_long_form,
    inputs=gr.Audio(sources="microphone",
                    type="filepath"),
    outputs=gr.Textbox(label="Transcription",
                       lines=3),
    allow_flagging="never")

file_transcribe = gr.Interface(
    fn=transcribe_long_form,
    inputs=gr.Audio(sources="upload",
                    type="filepath"),
    outputs=gr.Textbox(label="Transcription",
                       lines=3),
    allow_flagging="never",
)

with demo:
    gr.TabbedInterface(
        [mic_transcribe,
         file_transcribe],
        ["Transcribe Microphone",
         "Transcribe Audio File"],
    )
demo.launch(debug=True)

demo.close()