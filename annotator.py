import cv2
import argparse

# list to store the coordinates of the points
points = []

def draw_point(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        print(f'Point: ({x}, {y})')

        img_height = img.shape[0]
        img_width = img.shape[1]
        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
        cv2.line(img, (int(x), int(0)), (int(x), int(img_height)),
                 (0, 0, 255), 5)
        cv2.putText(img, str((x, y)), (int(x+20), int(y)),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2) #black color

        cv2.imshow('Image', img)

if __name__ == "__main__":
    # setting up argument parser
    parser = argparse.ArgumentParser(description="Annotating images by drawing points and lines using mouse.")
    parser.add_argument('image_path', type=str, help='Path to the image file')
    args = parser.parse_args()
    img = cv2.imread(args.image_path)

    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', draw_point)

    while True:
        cv2.imshow('Image', img)
        if cv2.waitKey(1) == ord("q"):
            break

    cv2.destroyAllWindows()
