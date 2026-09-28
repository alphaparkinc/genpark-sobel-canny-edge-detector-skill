from client import SobelCannyEdgeDetector

def main():
    detector = SobelCannyEdgeDetector()
    img = [[0]*20 for _ in range(10)] + [[255]*20 for _ in range(10)]
    res = detector.detect_edges(img)
    print("Sobel & Canny Edge Detection Verification:")
    print(f"Image Size: {res['width']}x{res['height']}")
    print(f"Strong Edges: {res['strong_edges_count']}, Max Gradient: {res['max_gradient']}")

if __name__ == "__main__":
    main()
