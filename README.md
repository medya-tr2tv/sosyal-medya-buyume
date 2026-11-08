# Sosyal Medya Büyüme ve Yönetim Paneli

**Ücretsiz ilk sürüm:** YouTube, Instagram, TikTok ve Facebook için linkten organik kampanya planlama, ayrı gerçek hesap envanteri ve manuel analiz paneli.

## Kurulum / OpenCode

1. OpenCode'da `https://github.com/medya-tr2tv/sosyal-medya-buyume` deposunu klonla veya aç.
2. `index.html` dosyasını Chrome'da aç. Başka paket veya sunucu gerekmiyor.
3. Dilersen GitHub > Settings > Pages > Deploy from a branch > main > /(root) yoluyla statik web sayfası olarak açabilirsin. (Depo şu anda public.)

## İki birbirinden bağımsız bölüm

### Büyüme Botu
- Video/fotoğraf dosyası **yüklenmez**, yalnızca gönderi URL'si girilir.
- URL'den YouTube, Instagram, TikTok veya Facebook algılanır.
- Müzik (arabesk, pop, rap vb.), film/dizi (komedi vb.), haber, spor ve diğer alt kategoriler seçilir.
- Gerçek abone/takipçi, izleyici tutma, gerçek beğeni/yorum veya dengeli büyüme hedefi seçilir.
- Hedef kitle açıklaması, kategoriye özel erişim adımları, 7 günlük ücretsiz görevler ve paylaşım metni oluşturulur.
- Kampanyalar kaydedilir ve silinir. Bağlantılar ve tanıtım metinleri kopyalanabilir; hedef platformlara otomatik gönderim henüz aktif değildir.

### Gerçek Hesaplarım
- YouTube, Instagram, TikTok ve Facebook hesaplarını ayrı bölümde listele.
- Kendi hesabının adını, URL'sini ve yönetim yetkisi onayını kaydet; **programda yapay sayı sınırı yoktur**. Tarayıcı depolama sınırı geçerlidir.
- Bu bölüm OAuth yetkilendirmesi veya canlı oturum bağlantısı yapmaz. Şifre, token ve oturum bilgisi girilmez.
- Hesapları kaydetmek otomatik beğeni, izleme, abone olma ya da yorum yazma başlatmaz.

### Sonuç ve Analiz
- Gerçek performans verilerini YouTube Studio / Instagram Insights / TikTok Analytics / Meta Business Suite üzerinden manuel gir.
- Beğeni/izlenme, abone/izlenme, etkileşim/izlenme ve ortalama izleme sürelerini hesaplar.
- Veriler yalnızca kendi tarayıcında (localStorage) tutulur; JSON yedeği indirilebilir/geri yüklenebilir.

## Gerçek etkileşim için öneriler
- Türle ilgili gerçek topluluklarda grup kurallarına uyarak içerik duyurusu
- Kısa kesit ve orijinal içerikle uzun videoya doğal yönlendirme
- Kanal bitiş ekranı, sabit yorum, oynatma listesi ve açık gönüllü abonelik çağrısı
- İçerik üreticileriyle izinli işbirliği ve ilgili izleyicilerle gerçek yorumlar
- Haftalık analize göre paylaşım saati, giriş ve başlık iyileştirmesi

## Sınırlar / sonraki geliştirme
Bu sürüm **izlenme, beğeni, abone veya takipçi göndermez**; gerçek kullanıcıları doğrudan keşfetmez; hesaplara otomatik bağlanmaz; API bağlantısı, 7/24 sunucu ve arka plan paylaşımı içermez. Resmi platform OAuth, API izinleri, güvenli backend ve zamanlama daha sonra geliştirilebilir. İzin verilse bile yapay izlenme döngüsü, toplu otomatik beğeni, otomatik abonelik ve izinsiz hesap kullanımı eklenmez. YouTube'un para kazanmaya uygun izlenme saatleri yalnızca resmi YouTube Studio verileriyle doğrulanabilir.

**Güvenlik:** Depo şu anda herkese açık. GitHub'a parola, API anahtarı veya kişisel müşteri verisi yükleme.
