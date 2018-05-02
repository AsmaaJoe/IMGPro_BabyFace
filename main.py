'''
Camera Example
==============

This example demonstrates a simple use of the camera. It shows a window with
a buttoned labelled 'play' to turn the camera on and off. Note that
not finding a camera, perhaps because gstreamer is not installed, will
throw an exception during the kv language processing.

'''

# Uncomment these lines to see all the messages
from kivy.logger import Logger
import logging
Logger.setLevel(logging.TRACE)

from kivy.app import App
from kivy.lang import Builder
from kivy.app import platform
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.camera import CameraBase

from sklearn import svm
import cv2
import sys
from matplotlib import pyplot as plt

import time
Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (480, 640)
        play: False
    ToggleButton:
        text: 'Play'
        on_press: camera.play = not camera.play
        size_hint_y: None
        height: '48dp'
    Button:
        text: 'Load Image'
        size_hint_y: None
        height: '68dp'
        on_press: root.load()
''')

class CameraClick(BoxLayout):
    def load(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        #camera.export_to_png("IMG_{}.png".format(timestr))
        #camera.texture.save()
       # tex=Image(camera)
      #  m = Image.load('3.jpg', keep_data=True)
        cascPath = "haarcascade_frontalface_default.xml"
        
        
  #############################################################3      
        img=cv2.imread("IMG_{}.png".format(timestr))
  #############################################################3
  
        faceCascade = cv2.CascadeClassifier(cascPath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
# Detect faces in the image
        faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,
            minNeighbors=5,minSize=(30, 30),flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
# Draw a rectangle around the faces
        padding=25
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x-padding, y-padding),
                (x+w+padding, y+h+padding), (0, 255, 0), 2)
      #  cv2.imshow("Faces found", img)
        img_out= cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
      
         # convert it to texture
        buf1 = cv2.flip(img_out, 0)
        buf = buf1.tostring()
        image_texture = Texture.create(
            size=(img_out.shape[1], img_out.shape[0]), colorfmt='rgb')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        camera.texture = image_texture
        
class TestCamera(App):

    def build(self):
        return CameraClick()


TestCamera().run()


