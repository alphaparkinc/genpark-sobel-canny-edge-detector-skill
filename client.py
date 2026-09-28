"""Sobel & Canny Edge Detection Engine
100% Python Standard Library (math).
"""

import math

class SobelCannyEdgeDetector:
    """2D spatial convolution and gradient-based edge extraction."""
    def __init__(self, low_threshold=20.0, high_threshold=50.0):
        self.low_threshold = low_threshold
        self.high_threshold = high_threshold

    def convolve2d(self, image, kernel):
        h, w = len(image), len(image[0])
        kh, kw = len(kernel), len(kernel[0])
        pad_h, pad_w = kh // 2, kw // 2
        out = [[0.0 for _ in range(w)] for _ in range(h)]
        for y in range(h):
            for x in range(w):
                s = 0.0
                for ky in range(kh):
                    for kx in range(kw):
                        iy = min(max(y + ky - pad_h, 0), h - 1)
                        ix = min(max(x + kx - pad_w, 0), w - 1)
                        s += image[iy][ix] * kernel[ky][kx]
                out[y][x] = s
        return out

    def detect_edges(self, image):
        h, w = len(image), len(image[0])
        kx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
        ky = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
        gx = self.convolve2d(image, kx)
        gy = self.convolve2d(image, ky)

        magnitude = [[0.0 for _ in range(w)] for _ in range(h)]
        direction = [[0.0 for _ in range(w)] for _ in range(h)]
        for y in range(h):
            for x in range(w):
                magnitude[y][x] = math.hypot(gx[y][x], gy[y][x])
                direction[y][x] = math.atan2(gy[y][x], gx[y][x])

        edges = [[0 for _ in range(w)] for _ in range(h)]
        for y in range(h):
            for x in range(w):
                if magnitude[y][x] >= self.high_threshold:
                    edges[y][x] = 255
                elif magnitude[y][x] >= self.low_threshold:
                    edges[y][x] = 128

        return {
            "height": h,
            "width": w,
            "strong_edges_count": sum(row.count(255) for row in edges),
            "weak_edges_count": sum(row.count(128) for row in edges),
            "max_gradient": round(max(max(row) for row in magnitude), 2)
        }
