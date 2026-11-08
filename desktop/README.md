# Windows Çoklu Hesap Yöneticisi

Bu klasör, masaüstünde **kendi hesabın veya açık izin aldığın hesaplar** için ayrı Chrome/Edge tarayıcı profilleri oluşturup aynı hesapları tekrar açan Python/Tkinter uygulamasıdır.

## Başlatma (Windows)

1. Ücretsiz Python 3.10+ yükle. Kurulum sırasında **Add python.exe to PATH** seçeneğini aç.
2. GitHub deposunu indir: **Code → Download ZIP** veya OpenCode içinde klonla.
3. ZIP'i çıkart; `desktop` klasöründeki `baslat.bat` dosyasına çift tıkla. Alternatif: `py -3 account_manager.py`.
4. Hesaplarını platform + bir etiket adı ile kaydet (YouTube, Instagram, TikTok, Facebook).
5. Hesabı seç ve **Tarayıcı profilini aç** düğmesine bas. Tarayıcının **kendi giriş ekranında** oturum açıp gerekiyorsa SMS/2FA doğrulamasını tamamla.
6. Aynı hesabı tekrar açtığında aynı profil klasörü kullanılır. Giriş oturumu hâlâ geçerliyse oturum açma sayfası tekrar gerekmez. Tarayıcı kendi şifre yöneticisini kullanabilir.
7. Video/gönderi bağlantısı girip **Gönderiyi seçili hesapta aç** diyerek o hesap profiliyle gönderiye git. Gerekli işlemleri platformda kendin yap.
8. Kullanıcı tarafından başlatılıp durdurulan süre ölçeri ve **Beğendim / Yorum yaptım / Takip ettim** işaretlerini, hesap bazlı sayaçlarda takip et.

## Güvenlik ve teknik sınırlar

- Şifre, SMS kodu, erişim belirteci veya çerez **uygulamanın veriler.json dosyasına yazılmaz**. Tarayıcı profilindeki oturumları Chrome/Edge kendi mekanizmasıyla saklar.
- Profil dizinleri: `%LOCALAPPDATA%\SosyalHesapYonetimi\tarayici_profilleri\<kimlik>`
- Liste ve elle işaretlenmiş sayaçlar: `%LOCALAPPDATA%\SosyalHesapYonetimi\veriler.json`
- Tarayıcı profilleri hassas giriş bilgisi barındırabilir. Bu klasörü GitHub'a yükleme veya başkalarıyla paylaşma. Arkadaşların hesabını yalnızca açık izinleri varsa yönet.
- Program kapansa bile açık olan Chrome/Edge pencerelerini otomatik kapatmaz. Ancak bilgisayarın açık kalması hesapların **çevrimiçi görüneceği** anlamına gelmez. Platform gerektiğinde yeniden giriş veya güvenlik kontrolü isteyebilir.
- Programda **sabit hesap sayısı sınırı yoktur**; 100 ayrı açık tarayıcı profili cihazın RAM/CPU kapasitesini zorlayabilir. Tümünü tek seferde başlatmak yerine ihtiyaç duyulanları açmak uygundur.
- Sayaçtaki süre **manuel başlat/durdur aralığıdır**; video oynatımı veya platform tarafından sayılan izlenme süresi **doğrulanmaz**.
- Beğeni/yorum/takip sütunları **kullanıcının manuel işaretleridir**, platformdan çekilmiş doğrulanmış etkileşim verisi değildir.
- Otomatik izleme döngüsü, toplu beğeni, otomatik abonelik, yorum spam'i, güvenlik doğrulamasını atlama ya da sahte çevrimiçi görünme sistemi içermez.

## Gereksinimler

- Windows 10 veya Windows 11
- Python 3.10+ (Tkinter standart kütüphane)
- Microsoft Edge veya Google Chrome
- Üçüncü taraf pip paketi gerekmez; program ücretsizdir.

## Programı sadece OpenCode ile düzenlemek

GitHub deposunu OpenCode'a aç; `desktop/account_manager.py` dosyasını düzenle. Python kurulu olduğunda aynı klasörde `py -3 account_manager.py` ile dene.

## Sorun giderme

- **Python bulunamadı:** Python'u PATH ekleyerek kur veya `python account_manager.py` çalıştır.
- **Tarayıcı açılmadı:** Edge/Chrome kurulu olduğundan ve listede seçildiğinden emin ol.
- **Tekrar doğrulama istiyor:** Kararı platform verir. Güvenlik aşamalarını uygulama devre dışı bırakamaz.
- **Profil kullanılıyor:** Aynı hesap profilini iki farklı tarayıcı türünde veya bağımsız iki ana süreçte aynı anda açma; profil dosyaları kilitli olabilir.
