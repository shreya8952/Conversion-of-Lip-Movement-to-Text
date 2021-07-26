import wx
import streamer
import threading
import time
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import cv2
import glob
import os
from gtts import gTTS
import virtualAudio

iteration = 1
mirror = True
width, height = (30, 30)


class webcamPanel(wx.Panel):

    def __init__(self, parent, camera, fps=10):
        global mirror

        wx.Panel.__init__(self, parent)

        self.camera = camera
        return_value, frame = self.camera.read()
        height, width = frame.shape[:2]

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
        if mirror:
            frame = cv2.flip(frame, 1)

        self.bmp = wx.BitmapFromBuffer(width, height, frame)

        self.SetSize((width, height))

        self.timer = wx.Timer(self)
        self.timer.Start(1000./fps)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.NextFrame)

    def OnPaint(self, e):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)

    def NextFrame(self, e):
        return_value, frame = self.camera.read()
        if return_value:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if mirror:
                frame = cv2.flip(frame, 1)
            self.bmp.CopyFromBuffer(frame)
            self.Refresh()


class MyFrame(wx.Frame):
    def __init__(self, camera):
        super().__init__(parent=None, title='Lip2Text Translator',
                         size=(900, 650))  # width,height

        panel = wx.Panel(self)

        # main_window_sizer = wx.BoxSizer(wx.VERTICAL)
		

        self.webcampanel = webcamPanel(panel, camera)

        # start button
        start_button = wx.Button(panel, label='Start', pos=(150, 45))
        start_button.Bind(wx.EVT_BUTTON, self.on_start_press)
        start_button.SetForegroundColour((0,0,0)) # set text color
        start_button.SetBackgroundColour((89, 197, 247))

        # stop button
        stop_button = wx.Button(panel, label='Stop', pos=(150, 85))
        stop_button.Bind(wx.EVT_BUTTON, self.on_stop_press)
        stop_button.SetForegroundColour((0,0,0)) # set text color
        stop_button.SetBackgroundColour((89, 197, 247))

        # textlabel
        # CREATE STATICTEXT AT POINT (20, 20)
        self.outputLabel = wx.StaticText(panel, id=1, label="", pos=(120, 200),
                                         size=wx.DefaultSize, style=0, name="statictext")
        

        font = wx.Font(25, wx.MODERN , wx.NORMAL, wx.NORMAL)
        self.outputLabel.SetFont(font)
        self.outputLabel.SetForegroundColour((255,0,0)) # set text color

        # self.SetMaxSize(wx.Size(400, 300))
        # self.SetMinSize(wx.Size(400, 300))
        self.Centre()  # centres it on the screen
        self.Show()
        self.stop = False

    def create_thread(self, target):
        thread = threading.Thread(target=target)
        self.started_thread = thread
        thread.daemon = True
        thread.start()

    def stop_thread(self):
        self.started_thread._stop()

    def on_start_press(self, event):
        print("Start clicked")
         #processing animation
        outputText = "Recording.."
        self.outputLabel.SetLabel(outputText)
        self.create_thread(self.start_translating)

    def on_stop_press(self, event):
        print("Stop clicked")
        self.stop = True

        #processing animation
        outputText = "Processing.."
        self.outputLabel.SetLabel(outputText)

        self.create_thread(self.stop_translating)

    vs = WebcamVideoStream(src=0)
    fps = FPS()

    def start_translating(self):
        self.stop = False
        streamer.clean_pictures()
        print("[INFO] sampling THREADED frames from webcam...")
        self.vs.start()
        self.fps.start()
        record_index = 0
        while self.fps._numFrames < 1000 and not(self.stop):
            frame = self.vs.read()
            print("frames: "+str(self.fps._numFrames) +
                  " record_index: "+str(record_index))
            cv2.imwrite("pictures/"+str(record_index)+".jpg", frame)
            record_index = record_index+1

            key = 0xFF & cv2.waitKey(35)
            self.fps.update()
            self.fps.stop()

    def stop_translating(self):

        try:
            # do a bit of cleanup, remove 0th image as is it always black
            files = glob.glob('pictures/0.jpg')
            os.remove(files[0])
        except:
            pass

        self.vs.stop()
        streamer.processImages()
        outputfile = open("result_lip/text.txt", 'w')
        outputfile.write("Processing")
        outputfile.close()
        
        outputText = streamer.displayText()
        self.outputLabel.SetLabel(outputText)
        language = 'en'
        myobj = gTTS(text=outputText, lang=language, slow=False)
        # Saving the converted audio in a mp3 file named
        # welcome 
        myobj.save("outputAudio.mp3")
        time.sleep(2)
        virtualAudio.streamAudio()


if __name__ == '__main__':
    camera = cv2.VideoCapture(0)
    app = wx.App()
    frame = MyFrame(camera)
    app.MainLoop()
