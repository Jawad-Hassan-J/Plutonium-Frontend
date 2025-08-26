from ultralytics import YOLO
import cv2
import os

def object_detection(user_input_request=None, user_input_file=None):
    if not user_input_file:
        return "(object_detection) please send picture"
    
   # نحمل الموديل في منهم قوي و بطيئ و سريع لكن بطيء
    model = YOLO("yolov10m.pt")    

    # ناخذ الصورة
    file_path = os.path.join("uploads", user_input_file.name)

    # اذا ملف uploads مو موحود نسويه
    os.makedirs("uploads", exist_ok=True)

    """
    w: اكتب
    b: binary
    as current_file: يخزن التعيلات في هذا المتغيرر
    """
    with open(file_path, "wb") as current_file:

        # ننسخ محتوى الصورة عشان نشتغل عليها
        # الملف الجديد بنكتب فيه بيانات الصورة الي رفعها اليوزر
        current_file.write(user_input_file.read())

    # imread: ترجع الصورة array
    # ارقام في ارقام كل بكسل له قيمة
    image = cv2.imread(file_path)

    # في حال الصورة مو موجودة ملف غلط مو موجود اصلا الى اخره
    if image is None:
        return "error in uploaded image"

    # model: YOLO("yolov10m.pt")  
    # نشغل الموديل سبب اننا عرفناه في متغير عشان اذا غيرنا المودل يكون في مكان واحد مو كل الكود
    results = model(image)

    # r: هو عدد الاشياء الي اكتشفها المودل
    for r in results:

        #r.boxes: الشغلة الي اكتشفها المودل
        #box: واجد من محموعة الاشياء الي اكتشفها المودل
        for box in r.boxes:

            # xy: الاحداثيات في الصورة
            # x1: يسار  
            # y1: فوق  
            # x2: يمين  
            # y2: تحت  

            # box.xyxy: هي الاحداثيات
            # retrun float number so we convert it into int
            # ليش؟ عشان الرسم لازم تكون اعداد بدون فواصل
            # بيرحع كل الاعداد int 
            # [0]: لانه يرجع  مصفوفة ثناىية الابعاد
            x1, y1, x2, y2 = map(int, box.xyxy[0])  

            """
            # الداتا ترحع ك Tensor .0, .2, .5
            # [0] ناخذ اول رقم
            # نحوله الى انتجر
            # model.names: عبارة عن اوبحت اسم الشيء و انكس للي اكتشفه 
            0:person, 1:car
            
            label: بيكون اوبجيكت فيه الانكس و السم
            """
            label = model.names[int(box.cls[0])]    

            # نسبة الثقة شكثر المودل متاكد ان هذا المربع هو هذا الشيء
            conf = box.conf[0]                      

            # نرسم على الصورة
            """
            # rectangle(First,second,third,fourth,fith)
            # rectangle: اسم الشكل
            # First(x1,y1): فوق في الزاوية على اليمين
            # Second(x2,y2): تحت في الزاوية على اليسار
            # (0,255,0): لون المستطيل, في هذي الحالة اخضر
            # 2: سمك الخط
            """
            cv2.rectangle(image, (x1,y1), (x2,y2), (0,255,0), 1)

            """
            # putText(image,text, startLocation, font_family, color, font_size): دالة مدمحة تكتب كلام على الصورة
            #image: الصورة الي تبغاها
            # text: النص
            في حالتنا النص مع نسبة الثقة بشكل عشري

            # startLocation: المكان الي يبدء منه الكلام
            # font_family: نوع الخط
            # color: لون الخط
            # font_size: حجم الخط
            """
            cv2.putText(image,f"{label} {conf:.2f}",(x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,255,0), 1)

            # نطبع الاشياء الي اكتشفها المودل في التيرنيمال
            print(f"Detected {label} with confidence {conf:.2f} at [{x1},{y1},{x2},{y2}]")


    # overwiter للصورة القديمة بالصورة الجديدة
    # imwrite: حق تحفظ الملف
    # اذا حفظنا الملف على نفس اللوكشين بيصير overwiter
    cv2.imwrite(file_path, image)

    # return f"object_detection success "

    output_path = os.path.join("uploads", "result.jpg")
    cv2.imwrite(output_path, image)
    return output_path
