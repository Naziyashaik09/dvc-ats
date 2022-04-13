import datetime
from uuid import uuid4
import numpy as np
import os
import os.path as osp
import glob
import cv2
import insightface
import alphaui as gr
import uuid
assert insightface.__version__>='0.4'


def detect_person(img, detector):
    bboxes, kpss = detector.detect(img)
    bboxes = np.round(bboxes[:,:4]).astype(np.int)
    kpss = np.round(kpss).astype(np.int)
    kpss[:,:,0] = np.clip(kpss[:,:,0], 0, img.shape[1])
    kpss[:,:,1] = np.clip(kpss[:,:,1], 0, img.shape[0])
    vbboxes = bboxes.copy()
    vbboxes[:,0] = kpss[:, 0, 0]
    vbboxes[:,1] = kpss[:, 0, 1]
    vbboxes[:,2] = kpss[:, 4, 0]
    vbboxes[:,3] = kpss[:, 4, 1]
    return bboxes, vbboxes

def inference(img,nms_thresh):
    
    detector = insightface.model_zoo.get_model('person.onnx', download=False)
    detector.prepare(0, nms_thresh=nms_thresh, input_size=(640, 640))
    bboxes, vbboxes = detect_person(img, detector)
    print(bboxes.shape[0])
    for i in range(bboxes.shape[0]):
        bbox = bboxes[i]
        vbbox = vbboxes[i]
        x1,y1,x2,y2 = bbox
        vx1,vy1,vx2,vy2 = vbbox
        cv2.rectangle(img, (x1,y1)  , (x2,y2) , (0,255,0) , 1)
        alpha = 0.8
        color = (255, 0, 0)
        for c in range(3):
            img[vy1:vy2,vx1:vx2,c] = img[vy1:vy2, vx1:vx2, c]*alpha + color[c]*(1.0-alpha)
        cv2.circle(img, (vx1,vy1) , 1, color , 2)
        cv2.circle(img, (vx1,vy2) , 1, color , 2)
        cv2.circle(img, (vx2,vy1) , 1, color , 2)
        cv2.circle(img, (vx2,vy2) , 1, color , 2)
    filename = str(uuid.uuid4())+".jpg"
    cv2.imwrite('./outputs/%s'%filename, img)
    num_person="Found :"+str(bboxes.shape[0]) +" Person"
    return img, num_person

num_person=""
image = gr.inputs.Image(label='INPUT')
ex=[["./examples/example2.jpg",0.7],['./examples/example3.jpg',0.5],['./examples/example5.webp',0.6],['./examples/example4.jpg',0.56]]
slider  = gr.inputs.Slider(default=0.56, minimum=0,maximum=1,step=0.01, label='nms_thresh')
output=[gr.outputs.Image(label='OUTPUT'),gr.outputs.HTML(label=num_person)]


inface=gr.Interface(fn=inference, inputs=[image,slider] ,outputs=output,interpretation='default',examples=ex,theme='dark',title="Person Detection")

inface.launch(server_name="0.0.0.0", server_port=7860)