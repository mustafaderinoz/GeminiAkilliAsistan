 # 🤖 Akıllı Asistan

Yapay Zekâ destekli not ve etkinlik yönetim uygulamasıdır, Gemini 2.5 Flash API kullanarak sohbet özelliği sunar ve yerel SQLite veritabanı ile verileri saklar.
---


## 🚀 Özellikler

- 📝 Not ekleme, listeleme ve özetleme
- 📅 Etkinlik ekleme, sıralama ve gösterme
- 🤖 Gemini 2.5 Flash API ile yapay zekâ sohbeti
- 🧠 Mesaj niyet analizi (not özeti, etkinlik özeti, normal sohbet)
- 💽 SQLite veritabanı kullanımı
- 🎨 Modern arayüz (Streamlit + CSS)
---

## 🛠️ Kullanılan Teknolojiler
| Teknoloji                                                                                              | Açıklama                      |
| ------------------------------------------------------------------------------------------------------ | ----------------------------- |
| <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white">          | Projenin ana programlama dili |
| <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white">    | Web arayüzü oluşturma         |
| <img src="https://img.shields.io/badge/SQLite-07405E?style=flat&logo=sqlite&logoColor=white">          | Yerel veritabanı              |
| <img src="https://img.shields.io/badge/Requests-000000?style=flat">                                    | API istekleri gönderme        |
| <img src="https://img.shields.io/badge/Google%20Gemini-4285F4?style=flat&logo=google&logoColor=white"> | Yapay zekâ modeli             |
| <img src="https://img.shields.io/badge/python--dotenv-4E9A06?style=flat">                              | API anahtarı yönetimi         |

## 📦 Proje Yapısı
```
📦 Proje Klasörü
│
├── __pycache__/          # Derlenmiş Python cache dosyaları
│
├── data/                 # Veri klasörü
│   └── assistant.db      # SQLite veritabanı
│
├── venv/                 # Sanal ortam
│
├── .env                  # API anahtarlarını içeren çevre değişkenleri
│
├── assistant.py          # Yapay zeka isteklerini yöneten dosya
├── database.py           # Veritabanı işlemleri
└── main.py               # Uygulamanın ana çalıştırma dosyası
```

## 🛠️ Gerekli Kurulumlar

### 1️⃣ Sanal Ortam Oluşturma

Proje klasörünüzü açtıktan sonra aşağıdaki komutları sırayla çalıştırın:
```bash
python -m venv venv
```

### 2️⃣ Sanal Ortamı Aktif Etme 

```bash
Windows için:
.\venv\Scripts\activate
```
```bash
Mac / Linux için:
source venv/bin/activate
```
### 3️⃣ Gerekli Kütüphanelerin Kurulumu
```bash
pip install streamlit requests python-dotenv
```
### 🔑 API Anahtarı Ekleme

Proje klasörüne .env adında bir dosya oluşturun ve içine aşağıdaki satırı ekleyin:
```bash
API_KEY="YOUR_API_KEY"
```
### ▶️ Uygulamayı Çalıştırma
```bash
streamlit run main.py
```
---

## 📱 Ekran Görüntüleri

|  | 
|----------------------|
| ![Login](screenshots/ozet.png) 



| |  
|----------------------|
| ![Login](screenshots/ozet2.png) |

---
