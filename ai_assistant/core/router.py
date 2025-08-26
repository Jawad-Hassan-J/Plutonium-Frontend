from sentence_transformers import SentenceTransformer, util

from core.tools import functions

from core.tools.image import image_to_text

from core.tools.voice import voice_clone

# simple model to understand the meaning of text
model = SentenceTransformer("all-MiniLM-L6-v2")

# هذا عشان نخلي فيه تلميحات التولز و على اي اساس نختار التولز
TOOLS = {
    "image_to_text": [
        "حول الصورة لنص",
        "استخرج النص من الصورة",
        "ابغى الكلام الي في الصورة",
        "اقرأ النص من الصورة",
        "ocr",
        "image to text",
        "extract text from image",
        "read text from image"
    ],
    "add_five": [
        "زود خمسة",
        "جمع 5",
        "add five",
        "plus 5"
    ],
      "voice_clone": [
        "استنسخ صوت",
        "قلد الصوت",
        "voice clone",
        "نسخ صوت"
    ],
}

"""
# الفنكشن ماب الغاية منها تسوي ماتش ويا اسم الفنكشن و لوكيشن الفنكشن عشان في اخر فنكشن نقدر نسوي لها رن
في حال مثلا عرفت متغير
function_test = FUNCTION_MAP.get(add_five(user_input_requesrt_request, user_input_file))
# ملاحظة هذا الكود بيصير له رن دايركت لازم نستحدم anonymous function 
# بس للشرح و التبسيط اخترت هذا المثال
الي بيصير ان بنبحث عن المفتاح اذا موجود او لا و قاعدين نرسل له البراميتر المطلوبة, في حال الفنكشن موجودة راح يسوي رن للفنشكن الي في لوكيشن ثاني و يرجع الي ترجع الفنكشن فبهذي الطرييقة نقدر نسوي رن حق اي فنكشن و الملفات منظمة
"""

FUNCTION_MAP = {
    "add_five": functions.add_five,
    "image_to_text": image_to_text,
    "voice_clone": voice_clone,
}



# threshold هي نسبة الدقة
# اشوف الاغلب يستخدم 0.70
def choose_tool(user_text, threshold=0.50):
    # التاكد ان النص مو فاضي, التاكد انه مو بس مسافات
    if not user_text or not user_text.strip():
        return {"ok": False, "tool": None, "reason": "empty input"}
    # تحويل النص الكلام الى ارقام, الكمبوتر مايفهم  المدخلات نفس ماهي لازم نحولها الى صيغة يقدر يتعامل وياها
    # convert_to_tensor
    # الهدف منها هو تحويل الكلام الى صيغة يفهمها المودل, بدونها راح ينطبع لست عادي مصفوفة من الارقام لكن هذي الدالة المدمجة تحولها الى صيغة يفهما المودل نفسه و فيه بعض الحسابات الدفيقة ما تصير الى بواسطة التجويل الى هذي الصيغة
    # is special type "'torch.Tensor'"

    query_emb= model.encode(user_text, convert_to_tensor=True)

    # راح نسوي لووب على كل الدوال الموجودة و نقيس نسبة التشابه و نختار اقوه توول, الدالة تقرا من 0 الين 1 , ما بدينا من سالب لان اذا كان صفر راح نختار اول فنكشن
    best_tool= None
    best_score= -1.0

    # نمشي على التولز الي فوق الاسم و الامقلة عشان نحسب اقوه دقة
    # .items retrun object of key and value, there are in python .keys,.values to return specif type
    for tool_name, examples in TOOLS.items():

        # convert_to_tensor عشان نحول الداتا الى مصفوفة نقدر نستخدم الدوال الجاهزة
        # util.cos_sim دالة جاهزة و نقدر تسخدمها لان جولناها الى صيغة يفهمها المودل
        example_embs= model.encode(examples, convert_to_tensor=True)

        # util.cos_sim تحسب الدفة او التشابه من بين واجد الى صفر
        # 1: exact much, 0: not much, -1: opesit
        # query_emb: تمثيل جملة البوزر
        # example_embs: تمثيل الجملة المخزنة في التول
        # ليش ناخذ اول قيمة؟
        # السبب انه يرجع مصفوفة ثنائية الابعاد
        # [[]]
        # فناخذ اول مصفوفة الي هي نفسها
        scores= util.cos_sim(query_emb, example_embs)[0]

        """
        الاوت بوت بيكون عبارة عن مصفةفة فيها ارفام تشابه جملة اليوزر و جملة المثال و بناحذ الماكس عشان نجسب اكبر تشابه
        # سبب استخدام دوت ايتم هو ان الدالة بتنطبع بشكل ثانية
        # tensor (0.someting)
        # .item
        بتطبع الرفم الى فولت طبيعي
        """
        max_score= scores.max().item()

        # simple sort function every loop change max number if its > than max
        if max_score > best_score:
            best_score= max_score
            best_tool= tool_name

    # threshold: الحد الادنى
    # ترجع التول مع السكور
    # اذا مافي تطابق ترجع ان مافي فنكشن تسوي هذي الخدمة او الطلب مو واضح
    if best_score >= threshold:
        return {"ok": True, "tool": best_tool, "score": float(best_score)}
    else:
        return {"ok": False, "tool": None, "reason": f"no tool matched ({best_score:.2f})"}


def execute(user_text, user_file=None, threshold=0.50):
    # نستدعي الفنشكن الي فوق و نسيفها في متغير عشان نسوي اكسس حق الداتا
    choice = choose_tool(user_text, threshold=threshold)
    
    # الدالة ترجع اوبجكت فيه معلومات من ضمنها هل حصل الفنكشن او لا؟
    # في حال كان الجواب لا, نرجع المتغير و نسوي اكسس على السبب الي هو الاوبجكت الي رجعته الفنكشن
    if not choice["ok"]:
        return f"{choice['reason']}"

    # retrun stop code so this is like else statement
    # نسوي اكسس على بعض العناصر الي في الاوبجكت
    tool_name = choice["tool"]
    score = choice['score']
    
    
    """
    تكلمة للي فوق, في الاوبجكت كلمة قت يعني دور عن هذا المفتاح و رجع القيمة
    في هذي الحالة القيمة هي عبارة عن فنشكن سوينا لها امبورت من ملف ثاني فراح يسوي لها 
    exexute 
    """
    func = FUNCTION_MAP.get(tool_name)

    # في حالة ان الفنشكن مو موجودة راح نرجع رسالة بسيطة بان التول مو موجودة
    if not func:
        return f"{tool_name} not availabe"
    
    # هذي عشان انا اشوف الي صاير كم سنية التشابه اسم التول الرسالة شلون يستلمها الكود الى اخره
    print("-"*100)
    print(f"user_text= {user_text}, user_file= {user_file}, tool_name= {tool_name}, score= {score}")
    print("-"*100)
    
    ## اهني بيسوي رن للفنشكن
    # كل فنكشن تاخذ  نفس البراميتر
    return func(user_text, user_file)
