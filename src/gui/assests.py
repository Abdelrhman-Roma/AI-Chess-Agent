import pygame
# مكتبة pygame علشان نتعامل مع الصور والرسم

import os
# مكتبة os علشان نتعامل مع المسارات (paths) بتاعت الملفات

def load_images(square_size):
    # دي فانكشن بتحميل صور القطع وترجعهم في dictionary

    pieces =["wp","bp","wr","br","wn","bn","wb","bb","wq","bq","wk","bk"]
    # ليستة بكل أنواع القطع
    # w = white , b = black
    # p = pawn , r = rook , n = knight , b = bishop , q = queen , k = king

    images ={}
    # dictionary فاضي هنخزن فيه الصور

    base_path = os.path.dirname(__file__)
    # ده بيجيب المسار الحالي للملف (folder اللي فيه الكود ده)

    image_path =os.path.join(base_path,"image")
    # بيركب المسار بتاع فولدر الصور (لازم يكون اسمه image)

    for piece in pieces:
        # نلف على كل قطعة في الليستة
        
        path = os.path.join(image_path,f"{piece}.png")
        # نحدد مسار الصورة (زي wp.png , bk.png ...)
        
        images[piece] = pygame.transform.scale(
            pygame.image.load(path),
            (square_size ,square_size)
        )
        # يحمل الصورة من الملف
        # وبعدين يصغرها/يكبرها حسب حجم المربع
        # ويخزنها في dictionary بالمفتاح بتاع القطعة

    return images
    # يرجع كل الصور جاهزة للاستخدام