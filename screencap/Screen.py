from screencap.video_capture2 import CaptureScreen
import cv2

class Screen:
    def __init__(self, cornerX, cornerY, width, height):
        self.cornerX = cornerX
        self.cornerY = cornerY
        self.width = width
        self.height = height
        self.screen = None
        
    def updateScreen(self):
        screen = CaptureScreen((self.width, self.height), (self.cornerX, self.cornerY))
        screen = cv2.cvtColor(screen, cv2.COLOR_RGBA2RGB)  #remove alpha channel        
        self.screen = screen
    
    def getScreen(self):
        return self.screen
    
    def showScreen(self, duration=0):
        if self.screen is None:
            self.updateScreen()
        cv2.imshow('screen', self.screen)
        cv2.waitKey(duration)
        
    def __str__(self):
        return "Screen object: corner({0},{1}) | w,h: ({2},{3})".format(self.cornerX, self.cornerY, self.width, self.height)
    
    def updateDimensions(self, cornerX, cornerY, width, height):
        self.cornerX = cornerX
        self.cornerY = cornerY
        self.width = width
        self.height = height

if __name__ == "__main__":
    screen = Screen(0, 0, 1920, 1080)
    screen.showScreen(0)
