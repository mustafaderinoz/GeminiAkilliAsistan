#https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

import os
import requests ## http istekleri yapmak için
from dotenv import load_dotenv # ortam değişkenlerini yüklemek için

load_dotenv()

api_key=os.getenv("API_KEY")

if not api_key:
    raise ValueError("api key .env dosyasında tanımlı değil")

url="https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

headers={
    "Content-Type":"application/json", # json formatında veri gönderilecek
    "X-Goog-Api-Key":api_key
}

def get_gemini_response(prompt:str)->str: # geminiye prompt göndericeğiz o da string bir response döndürecek
    #apiye gönderilecek json yapısı
    payload={
        "contents":[
            {
                "parts":[
                    {"text":prompt}
                ]
            } 
        ]
    }

    # gemini ye http post isteği gönderilecek
    response=requests.post(url,headers=headers,json=payload)

    # istek basariliysa (http 200)
    if response.status_code == 200:
        try:
            result = response.json() # json formatindaki yaniti sozluge ceviririz
            return result["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            # eger json yapisi beklenildigi gibi degilse hata dondurur
            return f"Yanit hatasi: {e}"
    else:
        return f"api hatasi {response.status_code}: {response.text}"
    


def detect_intent(message):
    #gemini için özel bir görev promtu oluştur mesajın hangi kategori 

    prompt=f"""
            Kullanıcının aşağıdaki cümlesini sınıflandır:
            Etiketlerden sadece birini döndür:
            - not_ozet (eğer notları görmek ya da özetlemesini istiyorsa)
            - etkinlik_ozet (eğer etkinlikleri görmek ya da özet istiyorsa)
            - normal (diğer her şey)

            Cümle: "{message}"
            Yalnızca etiket döndür: (örnek:not_ozet)
    
    """

    response=get_gemini_response(prompt)
    return response.strip().lower()




if __name__=="__main__":
    user_input=input("Kullanici sorusu:")
    yanit=get_gemini_response(user_input)
    print(f"Akilli Asistan:{yanit}")




