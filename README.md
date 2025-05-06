# 📌 Deprem Yardım Eleştirme ve Afet Yönetim Sistemi

## 📖 Proje Tanımı

**Deprem Yardım Eleştirme ve Afet Yönetim Sistemi**, afet sonrası ihtiyaç tespiti, yardım dağıtımı, geri bildirim, anlık deprem takibi ve bağış yönetimi gibi süreçleri bir araya getiren yapay zekâ destekli bir platformdur. Kullanıcılar sistem üzerinden yardım talebinde bulunabilir, yardımları değerlendirebilir, bağış yapabilir ve acil durumlara göre en uygun toplanma alanına yönlendirilebilir.

## 🎯 Amaçlar

- 🎯 Afet yardım süreçlerini **şeffaf, hızlı ve etkili** hâle getirmek  
- 🧭 Gerçek zamanlı veriyle hareket eden **karar destek sistemleri** sunmak  
- 🙌 Yardım alanların deneyim ve ihtiyaçlarını sistematik olarak değerlendirmek  
- 🧠 Yapay zekâ ile **önceliklendirme** ve kaynak optimizasyonu sağlamak  
- 💬 Vatandaşları, bağışçıları ve yetkilileri tek platformda buluşturmak  

## 🛠️ Özellikler

- ✅ Yardım başvuru formu (kişisel, konum, ihtiyaç ve sağlık bilgileri)  
- ✅ Yardım memnuniyet / eleştiri / öneri bildirimi  
- ✅ Gerçek zamanlı **deprem verisi ve harita entegrasyonu** (AFAD / Kandilli API)  
- ✅ Kullanıcının konumuna göre **en yakın toplanma alanını gösterme**  
- ✅ Harita üzerinde **navigasyon yönlendirmesi** (Google Maps API ile)  
- ✅ Bağış yapabilme
- ✅ Yapay zekâ destekli otomatik **önceliklendirme ve sınıflandırma** (örneğin: çocuklu aile, hasta birey vb.)  

## 🧠 Yapay Zekâ Entegrasyonu
 
- 🤖 **Önceliklendirme Motoru**: Yaş, kişi sayısı, sağlık durumu, barınma ihtiyacı gibi değişkenlere göre yardım taleplerini sıralar  ()
- 🗺️ **Kritik Bölge Tespiti**: Yoğun yardım çağrılarının geldiği bölgeleri işaretler  
- 🧭 **Toplanma Alanı Tahminleme**: Alternatif alan önerileri sunar (toplanma alanı doluysa)  
- 💡 **Yapay Zekâ Karar Asistanı**: Yetkili kullanıcıya en uygun müdahale sıralamasını önerir  

## 🖥️ Kullanılan Teknolojiler

| Katman             | Teknoloji                                  |
|--------------------|---------------------------------------------|
| Backend            | Python (FastAPI) |
| Frontend           | Bootstrap                                   |
| Veritabanı         | SQL                                         |
| Harita & Navigasyon| Leaflet.js, Google Maps API, OpenStreetMap  |
| Deprem API         | AFAD, Kandilli Rasathanesi                  |
| Yapay Zekâ         | Gemini API ve Langchain Entegrasyonu        |


## 🚀 Kurulum

```bash
git clone https://github.com/Melihemin/AidBridge/
cd AidBridge
!pip install -r requirements.txt
python main.py OR uvicorn main:app --reload 
