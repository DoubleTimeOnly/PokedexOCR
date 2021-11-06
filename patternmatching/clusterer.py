from sklearn_extra.cluster import KMedoids
import cv2
import numpy as np


class Clusterer:
    def __init__(self):
        pass

    def fit(self, dataset):
        raise NotImplementedError()


class KMedoids_Clusterer(Clusterer):
    def __init__(self):
        super().__init__()
        self.clusterer = None
        self.centers = None
        self.labels = None
        self.fit_data = None

    def fit(self, data, n_clusters=1, init="heuristic"):
        self.clusterer = KMedoids(n_clusters=n_clusters,
                                  init=init)
        self.clusterer.fit(data)
        self.fit_data = data
        self.centers = self.clusterer.cluster_centers_
        self.labels = self.clusterer.labels_

    def draw_clusters(self, canvas):
        colors = {}
        for label, point in zip(self.labels, self.fit_data):
            if label not in colors:
                color = (np.random.random(3) * 255).astype(int).tolist()
                colors[label] = color
            canvas = cv2.circle(canvas, (int(point[0]), int(point[1])), radius=5, color=colors[label], thickness=-1)
        return canvas

    def draw_cluster_centers(self, canvas):
        for point in self.centers:
            color = (np.random.random(3) * 255).astype(int).tolist()
            canvas = cv2.circle(canvas, (int(point[0]), int(point[1])), radius=5, color=color, thickness=-1)
        return canvas


