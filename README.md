# Sosyal Medya Büyüme Paneli

YouTube, Instagram, TikTok ve Facebook paylaşımları için **gerçek izleyiciye erişim ve organik büyüme planlama** aracı.

## Çalıştırma (OpenCode ile)

1. Bu depoyu OpenCode'da açın: `https://github.com/medya-tr2tv/sosyal-medya-buyume`.
2. `index.html` dosyasını tarayıcıda açın. Node.js, Python, paket kurulumu ve ücretli servis gerekmez.
3. İsterseniz GitHub Pages'i Settings → Pages → Deploy from a branch → main → /(root) şeklinde etkinleştirin.

## İlk sürümün çalışan özellikleri

- Yalnızca paylaşım URL'si girilir; video veya fotoğraf yüklenmez.
- YouTube, Instagram, TikTok, Facebook bağlantıları tanınır.
- Müzik (arabesk, pop, rap vb.), film/dizi, komedi, haber ve diğer alt türler seçilir.
- İçerik türü ve büyüme hedefine göre hedef kitle, yayın ve tanıtım önerileri oluşturulur.
- Kampanya kaydedilir, seçilir, silinir.
- Gerçek verilere dayanan **manuel** istatistik girişi: görüntülenme, beğeni, yorum, paylaşım, yeni abone/takipçi, izleme süresi.
- Beğeni/izlenme ve abone/izlenme oranları hesaplanır.
- Bağlantı ve tanıtım metni kopyalanabilir; X, WhatsApp ve Telegram'da kullanıcı onayıyla paylaşım açılabilir.
- Veriler sadece bu tarayıcının localStorage alanında tutulur; JSON yedeği indirilebilir ve geri yüklenebilir.

## Şimdilik yapılmayanlar

Bu sürüm **gerçek görüntülenme, beğeni, yorum veya abonelik göndermez**. Platform hesaplarına bağlanmaz, harici API kullanmaz ve 7/24 bulut otomasyonu değildir. Hesaplar için OAuth, sunucu, ilgili API izinleri ve güvenli gizli anahtar yönetimi ayrıca geliştirilmelidir. Özellikle YouTube'da geçerli izleme saatlerini sadece YouTube Studio doğrular.

Sahte hesap, toplu otomatik beğeni, otomatik abonelik, döngüsel oynatma veya yapay izlenme saati üretilmez. İçerikleri yalnızca izinli kanallarda duyurmayı ve gerçek kullanıcıların gönüllü katılımını hedefler.

## Sonraki aşamalar

1. Güvenli sunucu + veritabanı + giriş.
2. YouTube Analytics resmi OAuth bağlantısı ve kanal sahibinin yetkilendirmesi.
3. Meta/Instagram Graph API için uygun profesyonel hesap bağlantısı.
4. TikTok/Facebook için erişilebilen resmi API yetkileri.
5. İzinli paylaşım planlama, zamanlama, raporlama ve hata kayıtları.

## Gizlilik

Depo herkese açıktır. Şifre, access token, API anahtarı, kişisel bilgi veya müşteri verisi GitHub'a commit edilmemelidir.
