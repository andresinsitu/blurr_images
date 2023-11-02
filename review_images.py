import cv2
import argparse
import os
import numpy



parser = argparse.ArgumentParser() 
parser.add_argument('--input', type=str, default="", required=True)
parser.add_argument('--output', type=str, default="", required=True)
#parser.add_argument('--height', type=str, default="", required=False)
#parser.add_argument('--width', type=str, default="", required=False)
parser.add_argument('--fscreen', type=str, default="", required=True)

args = parser.parse_args()

input_path = args.input
output_path = args.output
print(args.fscreen)
roi_ksize = 25
scale = 1

#if (len(window_width)==0 or len(window_height)==0):
if args.fscreen=="True":
    bChangeVis = False
    cv2.namedWindow('img', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('img', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    roi_ksize = 25
else:
    bChangeVis = True

if not os.path.isdir(output_path):
    print('Creando carpeta de resultados...')
    os.mkdir(output_path)


def zoom_in(event, x, y, flags, param):
    #función zoom
    global scale
    global image
    img = image.copy()
    if event == cv2.EVENT_MOUSEWHEEL:
        if flags > 0:
            scale += 0.1
        else:
            scale -= 0.1
        if scale <= 0:
            scale = 0.1
        img_resized = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
        #cv2.namedWindow('zoom image', cv2.WND_PROP_FULLSCREEN)
        #cv2.setWindowProperty('zoom image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow('img', img_resized)
        print('zoom')


def obtain_selected_coordinates(image, image_path):
    # Blurring of zones selected by the user
    print("Manual blurring of zone")
    relative_coordinates = []
    img = image.copy()
    if not bChangeVis:
        cv2.namedWindow('Blur image', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('Blur image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.putText(img, "Editando...", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 255), 2, cv2.LINE_AA)
    height, width, _ = img.shape
    print(height)
    rois = cv2.selectROIs('Blur image', img)
    print("ROIS: %s" % rois)
    # cv2.destroyWindow('Blur image')    # Go through the bounding boxes selected y the user
    for roi in rois:
        print(rois)
        xmin, ymin, w, h = roi
        xmax = xmin + w
        ymax = ymin + h
        # Transform to relative coordinates
        xmin = xmin/width
        xmax = xmax/width
        ymin = ymin/height
        ymax = ymax/height
        relative_coordinates.append([xmin,xmax,ymin,ymax])
    cv2.destroyWindow('Blur image')
    cv2.waitKey(1)
    return relative_coordinates


def blur_zones(image,coordinates_arr, width, height):
    for coordinates in coordinates_arr:
        xmin, xmax, ymin, ymax = coordinates
        print (coordinates)
        xmin = int(xmin * width)
        xmax = int(xmax * width)
        ymin = int(ymin * height)
        ymax = int(ymax * height)
        roi = image[ymin:ymax, xmin:xmax]
        gaussian_image = cv2.GaussianBlur(roi, (roi_ksize, roi_ksize), 0)
        image[ymin:ymax, xmin:xmax] = gaussian_image
    return image

def main():
 #   for image_path in os.listdir(input_path):
    i=0
    image_list = os.listdir(input_path)
    image_list_len = len(image_list)
    while i < image_list_len and i>=0:

 #   for i in range(len(os.listdir(input_path))):
        image_path = image_list[i]

        print(input_path + "%s" % image_path)
        global image
        image = cv2.imread(input_path + "%s" % image_path)
        h, w = image.shape[:2]
        print(w)
        print(h)
        cv2.imshow('img', image)
        while(1):
            pressedkey = cv2.waitKey(1) & 0xFF

            cv2.setMouseCallback('img', zoom_in)
            
            if pressedkey == 32: #spacebar
                # Next image
                break

            if pressedkey == 8: #backspace
                # Previous image
                i=i-2
                break

            elif pressedkey == 27: #esc
                # Edit this image
                rel_coord = obtain_selected_coordinates(image, image_path)
                res_image = blur_zones(image, rel_coord, w, h)
                cv2.imshow('img', res_image)
                cv2.imwrite(output_path + "/%s" % image_path, res_image)
                continue
 
        i=i+1
if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass