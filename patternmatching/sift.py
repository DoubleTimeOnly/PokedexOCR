from patternmatching import matcher
from utils import logger
import cv2
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth



log = logger.get_logger(__name__)
log.setLevel(logger.DEBUG_WITH_IMAGES)


class SIFTMatcher(matcher.Matcher):
    def __init__(self):
        super().__init__()
        self.sift = cv2.SIFT_create(nOctaveLayers=1, sigma=2)

    def find_matches(self, query, pattern):
        if query is None or pattern is None:
            raise ValueError(f"One of query or pattern is None. Query: {type(query)}. Pattern: {type(pattern)}.")
        # pattern = cv2.resize(pattern, (0, 0), fx=4, fy=4)
        # query = cv2.resize(query, (0, 0), fx=4, fy=4)
        outputs = self.detect_keypoints_and_descriptors(query, pattern)
        query_keypoints, query_descriptors = outputs[0]
        pattern_keypoints, pattern_descriptors = outputs[1]

        x = np.array([pattern_keypoints[0].pt])

        for i in range(len(pattern_keypoints)):
            x = np.append(x, [pattern_keypoints[i].pt], axis=0)

        x = x[1:len(x)]

        bandwidth = estimate_bandwidth(x, quantile=0.5)

        ms = MeanShift(bandwidth=bandwidth, bin_seeding=False, cluster_all=True)
        ms.fit(x)
        labels = ms.labels_
        cluster_centers = ms.cluster_centers_

        labels_unique = np.unique(labels)
        n_clusters_ = len(labels_unique)
        print(f"number of estimated clusters: {n_clusters_}")
        s = [None] * n_clusters_
        for i in range(n_clusters_):
            l = ms.labels_
            d, = np.where(l == i)
            print(d.__len__())
            s[i] = list(pattern_keypoints[xx] for xx in d)

        pattern_descriptors_ = pattern_descriptors

        for i in range(n_clusters_):
            pattern_keypoints2 = s[i]
            l = ms.labels_
            d, = np.where(l == i)
            pattern_descriptors = pattern_descriptors_[d, ]

            good_matches, matches_mask, descriptor_matches = self.match_descriptors(query_descriptors, pattern_descriptors)

            if log.level <= logger.DEBUG_WITH_IMAGES:
                self.draw_keypoint_matches(matches_mask, query, query_keypoints, pattern, pattern_keypoints, descriptor_matches)

    def match_descriptors(self, query_descriptors, pattern_descriptors):
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=100)

        flann = cv2.FlannBasedMatcher(index_params, search_params)

        descriptor_matches = flann.knnMatch(query_descriptors, pattern_descriptors, k=2)

        good_matches = []
        matchesMask = [[0, 0] for i in range(len(descriptor_matches))]

        # Reduce number of false positives using lowe's ratio test
        for i, (m, n) in enumerate(descriptor_matches):
            if m.distance < 0.5 * n.distance:
                good_matches.append(m)
                matchesMask[i] = [1, 0]

        return good_matches, matchesMask, descriptor_matches

    def detect_keypoints_and_descriptors(self, query, pattern):
        query_keypoints, query_descriptors = self.sift.detectAndCompute(query, None)
        pattern_keypoints, pattern_descriptors = self.sift.detectAndCompute(pattern, None)

        outputs = [
            (query_keypoints, query_descriptors),
            (pattern_keypoints, pattern_descriptors)
        ]
        return outputs

    @staticmethod
    def draw_keypoint_matches(matches_mask, query, query_keypoints, pattern, pattern_keypoints, descriptor_matches):
        draw_params = dict(matchColor=(0, 255, 0),
                           singlePointColor=(255, 0, 0),
                           matchesMask=matches_mask,
                           flags=0)
        img3 = cv2.drawMatchesKnn(query, query_keypoints, pattern, pattern_keypoints, descriptor_matches, None,
                                  **draw_params)
        img3 = cv2.resize(img3, (0, 0), fx=0.5, fy=0.5)
        cv2.imshow("keypoint matches", img3)
        cv2.waitKey(0)


