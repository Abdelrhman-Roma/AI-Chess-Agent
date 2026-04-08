import os  # بنستورد os عشان المسارات
import pygame  # بنستورد pygame عشان الصور

def load_images(square_size):  # دالة تحميل صور القطع
    pieces = ["wp", "bp", "wr", "br", "wn", "bn", "wb", "bb", "wq", "bq", "wk", "bk"]  # ليستة كل القطع
    images = {}  # ديكشنري هنحفظ فيه الصور

    base_path = os.path.dirname(__file__)  # مسار الملف الحالي
    image_path = os.path.join(base_path, "image")  # مسار فولدر الصور

    for piece in pieces:  # بنلف على كل قطعة
        path = os.path.join(image_path, f"{piece}.png")  # بنكون مسار الصورة

        if not os.path.exists(path):  # لو الصورة مش موجودة
            raise FileNotFoundError(f"Missing chess piece image: {path}")  # نطلع خطأ واضح

        img = pygame.image.load(path).convert_alpha()  # بنحمّل الصورة مع الشفافية
        img = pygame.transform.smoothscale(img, (square_size, square_size))  # بنعمل resize مناسب
        images[piece] = img  # بنخزن الصورة في الديكشنري

    return images  # بنرجع كل الصور
