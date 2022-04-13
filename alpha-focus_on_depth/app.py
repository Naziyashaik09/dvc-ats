from distutils.log import debug
from importlib.resources import path
import torch
import alphaui as gr
import numpy as np

import requests
from PIL import Image
from io import BytesIO
from torchvision import transforms

from transformers import AutoConfig, AutoModel
from transformers import AutoModel

from focusondepth.model_config import FocusOnDepthConfig
from focusondepth.model_definition import FocusOnDepth

AutoConfig.register("focusondepth", FocusOnDepthConfig)
AutoModel.register(FocusOnDepthConfig, FocusOnDepth)

transform = transforms.Compose([
    transforms.Resize((384, 384)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
])
model = AutoModel.from_pretrained('model/', trust_remote_code=True)

@torch.no_grad()
def inference(input_image):
    global model, transform
    
    model.eval()
    input_image = Image.fromarray(input_image)
    original_size = input_image.size
    tensor_image = transform(input_image)
    
    depth, segmentation = model(tensor_image.unsqueeze(0))
    depth = 1-depth

    depth = transforms.ToPILImage()(depth[0, :])
    segmentation = transforms.ToPILImage()(segmentation.argmax(dim=1).float())

    return [depth.resize(original_size, resample=Image.Resampling.BICUBIC), segmentation.resize(original_size, resample=Image.Resampling.NEAREST)]

description = """
<center>
In this project, we use a DPT model to predict the depth and the segmentation mask of the class human, of an image.<br>
</center>
"""
title="""
FocusOnDepth
"""
css = """
"""
article = """
<center>
Example image taken from <a href="https://www.flickr.com/photos/17423713@N03/29129350066">here</a>. The image is free to share and use. <br>
</center>
<div style='text-align: center;'><a href='https://github.com/isl-org/DPT' target='_blank'>Original Paper</a> | <a href='https://github.com/antocad/FocusOnDepth' target='_blank'>Extended Version</a></div>
"""

iface = gr.Interface(
    fn=inference, 
    inputs=gr.inputs.Image(label="Input Image"), 
    outputs = [
        gr.outputs.Image(label="Depth Map:"),
        gr.outputs.Image(label="Segmentation Map:"),
    ],
    examples=[['./examples/example1.jpg'],['./examples/example4.jpg'],['./examples/example2.jpg'],['./examples/example3.jpg']],
    description=description,
    title=title,
    css=css,
    theme='dark',
)
iface.launch(server_name='0.0.0.0',server_port=7860)