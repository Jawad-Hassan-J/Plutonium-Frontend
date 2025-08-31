import requests, re
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("PLUTONIUM_URL")

def execute(user_input_request=None, user_input_file=None):
    data = {"user_input_request": user_input_request}
    print("PLUTONIUM_URL",url)
    print()
    
    if user_input_file:
         files = {"user_input_file": user_input_file} 
    else:
        files = None

    page_requests = requests.post(url, data=data, files=files)
    
    # response.status_code
    # response.headers
    # response.content
    # response.text
    # نحتاج نص الهشتمل
    html_page = page_requests.text


    """
    re.search(pattern, string, flags=0)
    # pattern: النمط
    # string: النص الي نبغاه
    # flags: ex  re.S
    الي تعطينا المحتوى الموزع على عدة اسطر
    
    return response or None
    
    """
    # السيرفر رحع صورة 
    # re.search: دالة داخليا تدور عن النص
    # r'': نستخدمها لان اذا السلاش حاء بعده حرف له معنى مثل المسافة /n
    # ([^"]+)": نمط التطابق يعني اي حرف ماعدا الي في القوس
    # +": عشان ينتهي بالكوتيشن
    response = re.search(r'data:image/jpeg;base64,([^"]+)"', html_page)
    
    ## response.group(0): كل شيء بدون الاستثناء
    ## response.group(1): بالاستثناء
    if response:
        return {"type": "image", "value": response.group(1)}

    # كلام
    # .: اي حرف
    # *: اي عدد
    # ?: يوقف في نهاية ال div 
    
    # re.s or re.DOTALL: نستخدمها عشان تجيب المختوى كامل بدونها راح يوقف في نهاية السطر, غاليا المختوى موزع على اكثر من سطر فنحتاجها
    response = re.search(r'<div class="message bot">(.*?)</div>', html_page, re.S)
    if response:
        # strip(): تخلي الاوت بوت نظيف بدون مسافات زايدة
        return response.group(1).strip()

    return {"type": "text", "value": "No response"}

