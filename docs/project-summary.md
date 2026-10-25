# Proje 2 — Docker Delivery Lab v0.1.0

## Tamamlanan çıktı

FastAPI ve PostgreSQL servislerini tek Compose komutuyla başlatan, görev ekleyip
listeleyen ve container'lar yeniden oluşturulduğunda veriyi koruyan yerel uygulama.

## Uygulanan konular

- Dockerfile, image, container ve build katmanlarının önbelleği.
- Container içindeki port ile host portu arasında bağlantı kurma.
- Uygulamayı root olmayan kullanıcıyla çalıştırma.
- Compose servisleri, ağ içinde `db` adıyla veritabanına erişme.
- `.env`, örnek ayar dosyası ve gerçek parolayı Git dışında tutma.
- Healthcheck ve `depends_on: service_healthy` ile başlangıç sırası.
- Liveness (`/health`) ve veritabanı readiness (`/ready`) kontrolleri.
- Parametreli SQL ile veri ekleme, transaction ve bağlantı yönetimi.
- PostgreSQL named volume ile kalıcı veri.
- Git geçmişi, özellik dalı, PR, ana dal ve sürüm yayını.

## Kabul sonuçları

- API ve PostgreSQL servisleri healthy durumda başladı.
- Görev ekleme HTTP 201, listeleme HTTP 200 döndürdü.
- Boş başlık, ayrı doğrulamada HTTP 422 ile reddedildi.
- İki container'ın yeniden oluşturulduğu ayrı kontrolde görev verisi korundu.
- Elle yapılan `down` / `up` demosunda aynı görev ID ve oluşturulma zamanı ile geri geldi.

## Kapsam

Bu sürümün hedefi API, veritabanı, Compose ve veri kalıcılığıdır.
CI/CD, registry yayını ve buluta dağıtım sonraki çalışma paketlerine aittir.
