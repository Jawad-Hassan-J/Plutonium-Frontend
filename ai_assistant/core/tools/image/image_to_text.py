from PIL import Image, ImageFilter, ImageOps
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def image_to_text(user_input_request=None, user_input_file=None):
    if not user_input_file:
        return "Please send picture"
    
    
    # نحفظ الصورة مؤقتا في ملف عشان اقدر اشتغل عليها 
    # join: عشان ندمح الرابط و يصير عندا رابط كامل حق نسوي اكسس للصورة
    # uploads: الملف الحالي
    #user_input_file: هو اوبجيت جاي فراح نسوي باث و اخر شيء فيه اسم الفايل
    file_path = os.path.join("uploads", user_input_file.name)
    
    # في حال الملف موجود نسويه عشان لا يعطينا ايروور
    os.makedirs("uploads", exist_ok=True)
    
    """
    # with: يفتح الملف و اذا خلص يسكؤه حتى لو صار غلط او ايرور
    # open: تفتح الملف
    # file_path: الرابط الي سويناه فوق (الباث)
    # wb+: 
        w: اكتب و سو ملف جديد لو مو موحود
        b: باينيري
        +: اكسس انه يقرا و يكتب
        
     # as destination: يسكر الملف اذا خلص
     او تستحدم destination.close() 
     اذا خلصت
    """
    with open(file_path, "wb+") as destination:
        
        # chunck: هو جزء من الملف, يعني بدال ما يجي ملف حجمه كبير و يطيح الرام نقسهم الى اجزاء
        # chunks(): دالة داخلية تسوي هذا الشيء
        for chunk in user_input_file.chunks():
                 
            # حاليا قاعدين نكتب الملف الي ارسله اليورز حبة حبة عشان لا ينضرب الحهاز
            # تخيل ملف عبارة عن 99 ام بي
            # chuncks: 33,33,33
            # نكتب اول 33 بعدها 33 بعدها 33
            destination.write(chunk)
            
    # الصورة الاصلية
    # يرجع الصورة كاوبجكت
    # يعطينا خصائص مثل
    # img.format, img.size, img,mode 
    # هذي الخطوة مهمة عشان نقدر نتعامل مع الصورة و نعدلها
    img = Image.open(file_path)
    
    # ميثود تحول لون الصورة الى الرمادي 
    gray = img.convert("L")
    

    best_text = ""
    best_img = None
    best_threshold = None
    # thresholds = [130, 150, 170, 190]
    thresholds = [200]
    for th in thresholds:

    #Threshold:  بنخلي الصورة جزئين اما ابيض او اسود في حال البكسلات اقل من 150 بيكون ابيض في حال اكثر بيكون اسود عشان نقلل النويز في الخلفية
    #lambda: عبارة عن فنكشن تسوي ريتيرن في نفس السطر  
    # lambda = anonymous function
    # الواحد هو درحة نفس ال
    # l RGB RGBA الى اخره
        processed_img = gray.point(lambda x: 0 if x < th else 255, "1")

        
        processed_img = processed_img.filter(ImageFilter.SHARPEN)
        
        
        # processed_img.show(title="Test")
        
        
        processed_img = ImageOps.invert(processed_img)
        
        
        processed_img = processed_img.filter(ImageFilter.MedianFilter(size=3))
        
        

        config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(processed_img, lang="eng", config=config)
        
        if len(text) > len(best_text):
            best_text = text
            best_img = processed_img
            best_threshold = th
        
    if best_text.strip():
        return best_text.strip()
    else:
        return "no text found"
        
    