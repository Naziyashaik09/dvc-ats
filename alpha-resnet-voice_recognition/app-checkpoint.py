import alphaui as gr


import argparse
import functools

import numpy as np
import torch
from infer_contrast import run

from utils.reader import load_audio
from utils.utility import add_arguments, print_arguments


STYLE = """
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" integrity="sha256-YvdLHPgkqJ8DVUxjjnGVlMMJtNimJ6dYkowFFvp4kKs=" crossorigin="anonymous">
"""
OUTPUT_OK = (
    STYLE
    + """
    <div class="container">
        <div class="row"><h1 style="text-align: center">Speaker1 and Speaker2</h1></div>
        <div class="row"><h1 class="display-1 text-success" style="text-align: center">the same person</h1></div>
        <div class="row"><h1 style="text-align: center">Similarity is:</h1></div>
        <div class="row"><h1 class="display-1 text-success" style="text-align: center">{:.1f}%</h1></div>
        <div class="row"><small style="text-align: center">(A similarity of more than 70% can be considered as the same person)</small><div class="row">
    </div>
"""
)
OUTPUT_FAIL = (
    STYLE
    + """
    <div class="container">
        <div class="row"><h1 style="text-align: center">Speaker1 and Speaker2</h1></div>
        <div class="row"><h1 class="display-1 text-danger" style="text-align: center">not the same person</h1></div>
        <div class="row"><h1 style="text-align: center">Similarity is:</h1></div>
        <div class="row"><h1 class="text-danger" style="text-align: center">{:.1f}%</h1></div>
        <div class="row"><small style="text-align: center">(A similarity of more than 70% can be considered as the same person)</small><div class="row">
    </div>
"""
)

THRESHOLD = 0.70
def voiceRecognition(audio1,audio2):
    score = run(audio1,audio2)
    if score >= THRESHOLD:
        output = OUTPUT_OK.format(score * 100)
    else:
        output = OUTPUT_FAIL.format(score * 100)
    return output


title = "Voice Recognition"
description = "This voice recognition demo(Chinese Format) is a simple implementation based on ResNet. It used ArcFace Loss and an open source Chinese voice corpus - zhvoice."

inputs = [gr.inputs.Audio(source="upload",type="filepath", label="Speaker1"),
          gr.inputs.Audio(source="upload",type="filepath", label="Speaker2")]

output = gr.outputs.HTML(label="")
          
article = (
    "<p style='text-align: center'>"
    "<a href='https://github.com/yeyupiaoling/VoiceprintRecognition-Pytorch' target='_blank'>???? Code Repository</a> | "
    "<a href='https://github.com/fighting41love/zhvoice' target='_blank'>??????? zhvoice Dataset</a> | "
    "</p>"
)

examples = [
    ["samples/?????????1.wav", "samples/?????????2.wav"],
    ["samples/?????????1.wav", "samples/?????????2.wav"],
    ["samples/?????????1.wav", "samples/?????????2.wav"],
    ["samples/????????????1.wav", "samples/?????????.wav"],
    ["samples/????????????1.wav", "samples/????????????2.wav"],
    ["samples/?????????.wav", "samples/?????????.wav"]]

interface = gr.Interface(
    fn=voiceRecognition,
    inputs=inputs,
    outputs=output,
    title=title,
    description=description,
    examples=examples,
    examples_per_page=3,
    article=article,
    enable_queue=True)
interface.launch(debug=True,share=True)