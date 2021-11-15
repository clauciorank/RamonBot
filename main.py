import cv2
import numpy as np
from PIL import Image, ImageDraw


def reading_image(image_file):
    image = Image.open(image_file)
    new_size = (640, 360)
    image = image.resize(new_size)
    img_cv2 = np.array(image)

    # Warping
    pts1 = np.float32([[0, 0], [0, 360], [640, 0], [640, 360]])
    pts2 = np.float32([[614, 523], [605, 823], [1212, 607], [1154, 962]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    output = cv2.warpPerspective(img_cv2, matrix, (1300, 1600))
    output_pil = Image.fromarray(output)

    # Read Ramon and Paste

    ramon = Image.open('ramon.png')

    # Mask image
    mask_im = Image.new("L", ramon.size, 0)

    draw = ImageDraw.Draw(mask_im)
    draw.polygon(((614, 523), (1212, 607), (1154, 962), (605, 823)), fill=255)
    ramon.paste(output_pil, mask_im)

    # Crop and save
    crop = (0, 0, 1200, 1600)
    ramon = ramon.crop(crop)

    ramon.save('montagem.png')


if __name__ == '__main__':
    reading_image('19923.jpg')
