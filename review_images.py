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
scale=1


zoom = 1
min_zoom = 0.1
max_zoom = 5
x_offset = 0
y_offset = 0

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
    global image,image_o, zoom, min_zoom, max_zoom, x_offset, y_offset,new_width,new_height
    if event == cv2.EVENT_MOUSEWHEEL:
        if flags > 0:
            zoom *= 1.1
            zoom = min(zoom, max_zoom)
        else:
            zoom /= 1.1
            zoom = max(zoom, min_zoom)

        img = image_o.copy()

        # Calculate zoomed-in image size
        new_width = round(img.shape[1] / zoom)
        new_height = round(img.shape[0] / zoom)

        # Calculate offset
        x_offset = round(x - (x / zoom))
        y_offset = round(y - (y / zoom))

        # coordinates
        x_coord = [x_offset , x_offset + new_width]
        y_coord = [y_offset , y_offset + new_height]

        # Crop image
        img = img[
            y_coord[0]: y_coord[1],
            x_coord[0]:x_coord[1],
        ]

        # Stretch image to full size
        image = cv2.resize(img, (image_o.shape[1], image_o.shape[0]))
        print(f'zoom\nimage height: {new_height}\nimage width: {new_width}')
        cv2.imshow("img", image)


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
    print(f'h: {height}, w: {width}')
    rois = cv2.selectROIs('Blur image', img)
    print("ROIS: %s" % rois)
    # cv2.destroyWindow('Blur image')    # Go through the bounding boxes selected y the user
    for roi in rois:
        print(rois)
        xmin, ymin, w, h = roi
        xmax = xmin + w
        ymax = ymin + h
        # Transform to relative coordinates
        xmin = (xmin)/width
        xmax = (xmax)/width
        ymin = (ymin)/height
        ymax = (ymax)/height
        relative_coordinates.append([xmin,xmax,ymin,ymax])
    cv2.destroyWindow('Blur image')
    cv2.waitKey(1)
    return relative_coordinates


def blur_zones(image,coordinates_arr, width, height):
    global x_offset, y_offset,new_width,new_height
    for coordinates in coordinates_arr:
        xmin, xmax, ymin, ymax = coordinates
        print (f'coordinadas {coordinates}\nx_offset: {x_offset} y_offset: {y_offset}')
        xmin = int(xmin* new_width) + x_offset
        xmax = int(xmax* new_width) + x_offset
        ymin = int(ymin* new_height)+ y_offset
        ymax = int(ymax* new_height)+ y_offset
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

        global x_offset,y_offset,new_width,new_height
        x_offset=0
        y_offset=0
        new_width=0
        new_height=0

        global image, image_o
        image_o = cv2.imread(input_path + "%s" % image_path)
        image = image_o.copy()
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
                res_image = blur_zones(image_o, rel_coord, w, h)
                cv2.imshow('img', res_image)
                cv2.imwrite(output_path + "/%s" % image_path, res_image)
                continue
 
        i=i+1
if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass