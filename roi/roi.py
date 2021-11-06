import numpy as np
import cv2


class ROI:
    def __init__(self, cornerX, cornerY, width, height, theta=0, offsetX=0, offsetY=0):
        self.x = cornerX
        self.y = cornerY
        self.width = width
        self.height = height
        self.theta = theta
        self.offsetX = offsetX
        self.offsetY = offsetY

    def getROICorners(self):
        # top-left, top-right, bottom-right, bottom-left
        offset_origin = (self.x + self.offsetX, self.y + self.offsetY)
        rect = [
            (offset_origin[0], offset_origin[1]),
            (offset_origin[0] + self.width, offset_origin[1]),
            (offset_origin[0] + self.width, offset_origin[1] + self.height),
            (offset_origin[0], offset_origin[1] + self.height)
        ]

        return rect

    def getROI(self, image):
        roi_rect = self.getROICorners()
        return image[roi_rect[0]:roi_rect[3], roi_rect[0]:roi_rect[1]]
