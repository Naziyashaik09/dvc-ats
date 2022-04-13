from cProfile import label
from distutils.log import debug
import os
os.system("hub install deoldify==1.0.1")
import alphaui as gr
import paddlehub as hub
from pathlib import Path


model = hub.Module(name='deoldify')

def inference(image):
    model.predict(image.name)
    return './output/DeOldify/'+Path(image.name).stem+".png"

title = "De-Oldify"
description = "This is responsible for adding new life to dull and dark old images"

examples=[['./examples/ex_1.jpeg'],['./examples/ex_2.jpg']]
iface = gr.Interface(inference, inputs=gr.inputs.Image(type="file",label="INPUT"), outputs=gr.outputs.Image(type="file",label="OUTPUT"),examples=examples,enable_queue=True,title=title,description=description,theme='dark')
iface.launch(server_name="0.0.0.0", server_port=7860)