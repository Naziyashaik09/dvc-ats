from cProfile import label
import imghdr
import cv2
import sys
from matplotlib.pyplot import title
import numpy as np
import datetime
import os
import glob
from retinaface import RetinaFace
import alphaui as gr

#thresh = 0.8


count = 1

gpuid = -1
detector = RetinaFace('./model/R50', 0, gpuid, 'net3')
num_faces=""


def inference(img,thresh):
    # img = cv2.imread('./examples/example2.jpg')
    #print(img.shape)
    
    scales = [1024, 1980]
    im_shape = img.shape
    target_size = scales[0]
    max_size = scales[1]
    im_size_min = np.min(im_shape[0:2])
    im_size_max = np.max(im_shape[0:2])
    #im_scale = 1.0
    #if im_size_min>target_size or im_size_max>max_size:
    im_scale = float(target_size) / float(im_size_min)
    # prevent bigger axis from being more than max_size:
    if np.round(im_scale * im_size_max) > max_size:
        im_scale = float(max_size) / float(im_size_max)

   # print('im_scale', im_scale)

    scales = [im_scale]
    flip = False

    for c in range(count):
        faces, landmarks = detector.detect(img,
                                        thresh,
                                        scales=scales,
                                        do_flip=flip)
       # print(c, faces.shape, landmarks.shape)

    if faces is not None:
        num_faces="Found :"+str(faces.shape[0]) +" Faces"
        
        print('find', faces.shape[0], 'faces')
        for i in range(faces.shape[0]):
            #print('score', faces[i][4])
            box = faces[i].astype(np.int)
            #color = (255,0,0)
            color = (0, 0, 255)
            cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), color, 2)
            if landmarks is not None:
                landmark5 = landmarks[i].astype(np.int)
                #print(landmark.shape)
                for l in range(landmark5.shape[0]):
                    color = (0, 0, 255)
                    if l == 0 or l == 3:
                        color = (0, 255, 0)
                    cv2.circle(img, (landmark5[l][0], landmark5[l][1]), 1, color,
                            2)

        #filename = './detector_test.jpg'
        #print('writing', filename)
        #cv2.imwrite(filename, img)

        return img ,num_faces
image = gr.inputs.Image(label='INPUT')
slider  = gr.inputs.Slider(default=0.75, minimum=0,maximum=1,step=0.01, label='Threshold')
output=[gr.outputs.Image(label='OUTPUT'),gr.outputs.HTML(label=num_faces)]
ex=[["./examples/example1.jpg",0.7],['./examples/example2.jpg',0.2],['./examples/example3.jpg',0.6]]



inface=gr.Interface(fn=inference, inputs=[image,slider] ,outputs=output,interpretation='default',examples=ex,theme='dark',title="Face Detection")

inface.launch(share=True,debug=True,server_name="0.0.0.0", server_port=7860)