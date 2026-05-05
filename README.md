Əsas Funksiyalar
​Təhlükəsiz Giriş: İstifadəçi adı və şifrə ilə giriş; 3 yanlış cəhddən sonra 10 saniyəlik bloklanma (cooldown).  
​Məhsul Kataloqu: Kateqoriyalar üzrə qruplaşdırılmış məhsul siyahısı (Geyimlər, Elektronika və s.).  
​Səbət və Favoritlər: Məhsulları səbətə əlavə etmək, miqdarı redaktə etmək və ya favorit siyahısına salmaq.  
​Checkout (Ödəniş): Səbətdəki məhsulların ümumi məbləğinin hesablanması və balans kifayət edərsə alışın tamamlanması.  
​Tarixçə (Log): Uğurlu/uğursuz girişlər, alış-verişlər və şifrə dəyişikliklərinin timestamp ilə qeydi.  
​Parametrlər: Köhnə şifrəni təsdiqləməklə yeni şifrə təyin etmək imkanı.  
​ Fayl Sistemi (Data Storage)
​Sistem bütün məlumatları aşağıdakı fayllarda saxlayır:  
​users.json: İstifadəçi hesabı və balans məlumatları.  
​products.json: Mağazadakı mövcud məhsullar.  
​basket_<user>.json: İstifadəçinin səbətindəki gözləyən sifarişlər.  
​history_<user>.log: Sistem hadisələrinin jurnalı.  
​ Texniki Tələblər
​Dil: Python 3.x
​Kitabxanalar: json, os, time, datetime (standart kitabxanalar)
​Saxlama: Yalnız fayllar (Database tələb olunmur).  
​ Başlamaq üçün
​Repozitoriyanı klonlayın.
​main.py faylını işə salın: python main.py.
​Default Giriş: * Username: student1
​Password: 1234
