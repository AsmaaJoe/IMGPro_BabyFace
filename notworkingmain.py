'''
Camera Example
==============

This example demonstrates a simple use of the camera. It shows a window with
a buttoned labelled 'play' to turn the camera on and off. Note that
not finding a camera, perhaps because gstreamer is not installed, will
throw an exception during the kv language processing.

'''

# Uncomment these lines to see all the messages
# from kivy.logger import Logger
# import logging
# Logger.setLevel(logging.TRACE)

from kivy.app import App
from kivy.lang import Builder
from kivy.app import platform
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

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
        resolution: (640, 480)
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

class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture
class CamApp(App):
    def build(self):
        self.capture = cv2.VideoCapture(1)
        self.my_camera = KivyCamera(capture=self.capture, fps=30)
        return self.my_camera

    def on_stop(self):
        #without this, app will not exit even if the window is closed
		self.capture.release()




class CameraClick(BoxLayout):
    def load(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        #img = cv2.imread("3.jpg")
        #cascPath = "haarcascade_frontalface_default.xml"
        #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      #  m = Image.load('3.jpg', keep_data=True)
        cascPath = "haarcascade_frontalface_default.xml"
        img=cv2.imread('3.jpg')
# Create the haar cascade
        faceCascade = cv2.CascadeClassifier(cascPath)
# Read the image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Detect faces in the image
        faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,
            minNeighbors=5,minSize=(30, 30),flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
# Draw a rectangle around the faces
        padding=25
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x-padding, y-padding),
                (x+w+padding, y+h+padding), (0, 255, 0), 2)
        cv2.imshow("Faces found", img)
        img_out= cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.imshow(img_out)
        plt.show()
        #imgKivy = (
		
       # if platform() == 'android':
    	#	DATA_FOLDER = os.getenv('EXTERNAL_STORAGE') or os.path.expanduser("~")
       # timestr = time.strftime("%Y%m%d_%H%M%S")
       # path =os.mkdir(App.user_data_dir) #/sdcard/kivyexamples/ +"/IMG_{}.png".format(timestr)
        #camera.export_to_png("IMG_{}.png".format())
        #print("Captured")
        
class TestCamera(App):

    def build(self):
        return CameraClick()


TestCamera().run()

if __name__ == '__main__':
	CamApp().run()


