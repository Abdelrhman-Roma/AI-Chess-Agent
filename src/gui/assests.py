import os
import pygame

def load_images(square_size):
    # دي فانكشن بتحميل صور القطع باستخدام pygame

    pieces = ["wp","bp","wr","br","wn","bn","wb","bb","wq","bq","wk","bk"]

    images = {}

    base_path = os.path.dirname(__file__)
    image_path = os.path.join(base_path, "image")

    for piece in pieces:
        path = os.path.join(image_path, f"{piece}.png")

        # تحميل الصورة
        img = pygame.image.load(path).convert_alpha()

        # عمل resize باستخدام pygame
        img = pygame.transform.scale(img, (square_size, square_size))

        images[piece] = img

    return images