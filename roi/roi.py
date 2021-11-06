import numpy as np
import cv2


class ROI:
    def __init__(self, cornerX, cornerY, width, height, theta=0, offsetX=0, offsetY=0):
        self.x = int(cornerX)
        self.y = int(cornerY)
        self.width = int(width)
        self.height = int(height)
        self.theta = int(theta)
        self.offsetX = int(offsetX)
        self.offsetY = int(offsetY)

    def getROICorners(self):
        # top-left, top-right, bottom-right, bottom-left
        offset_origin = (self.x + self.offsetX, self.y + self.offsetY)
        rect = [
            (int(offset_origin[0]), int(offset_origin[1])),
            (int(offset_origin[0] + self.width), int(offset_origin[1])),
            (int(offset_origin[0] + self.width), int(offset_origin[1] + self.height)),
            (int(offset_origin[0]), int(offset_origin[1] + self.height))
        ]

        return rect

    def getROI(self, image):
        roi_rect = self.getROICorners()
        return image[roi_rect[0][1]:roi_rect[2][1], roi_rect[0][0]:roi_rect[2][0]]
