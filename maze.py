from pygame import *
import random

# sprite'lar için ebeveyn sınıfı
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()  # Sprite sınıfının init metodunu çağırıyoruz
        self.image = transform.scale(image.load(player_image), (55, 55))  # Resmi yüklüyoruz ve boyutunu ayarlıyoruz
        self.speed = player_speed  # Sprite'ın hızını ayarlıyoruz
        self.rect = self.image.get_rect()  # Sprite'ın dikdörtgenini alıyoruz
        self.rect.x = player_x  # Sprite'ın x koordinatını ayarlıyoruz
        self.rect.y = player_y  # Sprite'ın y koordinatını ayarlıyoruz

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))  # Sprite'ı ekrana çiziyoruz

# Oyuncu sınıfı
class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_lives):
        super().__init__(player_image, player_x, player_y, player_speed)  # GameSprite'ın init metodunu çağırıyoruz
        self.lives = player_lives  # Oyuncunun can sayısını ayarlıyoruz

    def update(self):
        keys = key.get_pressed()  # Basılan tuşları alıyoruz
        if keys[K_a] and self.rect.x > 5:  # Sol tuşa basıldıysa ve oyuncu sol sınırda değilse
            self.rect.x -= self.speed  # Oyuncuyu sola hareket ettiriyoruz
        if keys[K_d] and self.rect.x < win_width - 80:  # Sağ tuşa basıldıysa ve oyuncu sağ sınırda değilse
            self.rect.x += self.speed  # Oyuncuyu sağa hareket ettiriyoruz
        if keys[K_w] and self.rect.y > 5:  # Yukarı tuşa basıldıysa ve oyuncu üst sınırda değilse
            self.rect.y -= self.speed  # Oyuncuyu yukarı hareket ettiriyoruz
        if keys[K_s
        ] and self.rect.y < win_height - 80:  # Aşağı tuşa basıldıysa ve oyuncu alt sınırda değilse
            self.rect.y += self.speed  # Oyuncuyu aşağı hareket ettiriyoruz

# Düşman sınıfı
class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)  # GameSprite'ın init metodunu çağırıyoruz
        self.side = "left"  # Düşmanın hareket yönünü ayarlıyoruz

    def update(self):
        if self.rect.x <= 470:  # Düşman sol sınırda ise
            self.side = "right"  # Hareket yönünü sağa çeviriyoruz
        if self.rect.x >= win_width - 85:  # Düşman sağ sınırda ise
            self.side = "left"  # Hareket yönünü sola çeviriyoruz
        if self.side == "left":  # Eğer yön sol ise
            self.rect.x -= self.speed  # Düşmanı sola hareket ettiriyoruz
        else:  # Eğer yön sağ ise
            self.rect.x += self.speed  # Düşmanı sağa hareket ettiriyoruz

# Duvar sınıfı
class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()  # Sprite sınıfının init metodunu çağırıyoruz
        self.color_1 = color_1  # Duvarın rengini ayarlıyoruz
        self.color_2 = color_2  # Duvarın rengini ayarlıyoruz
        self.color_3 = color_3  # Duvarın rengini ayarlıyoruz
        self.width = wall_width  # Duvarın genişliğini ayarlıyoruz
        self.height = wall_height  # Duvarın yüksekliğini ayarlıyoruz
        self.image = Surface((self.width, self.height))  # Duvar için bir yüzey oluşturuyoruz
        self.image.fill((color_1, color_2, color_3))  # Yüzeyi renklendiriyoruz
        self.rect = self.image.get_rect()  # Duvarın dikdörtgenini alıyoruz
        self.rect.x = wall_x  # Duvarın x koordinatını ayarlıyoruz
        self.rect.y = wall_y  # Duvarın y koordinatını ayarlıyoruz

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))  # Duvarı ekrana çiziyoruz

# Labirent oluşturma fonksiyonu
def create_labyrinth(layout):
    walls = []  # Duvarları saklayacak bir liste oluşturuyoruz
    for wall_data in layout:  # Her duvar verisi için
        walls.append(Wall(205, 50, 153, *wall_data))  # Bir duvar oluşturup listeye ekliyoruz
    return walls  # Duvarlar listesini döndürüyoruz

# Farklı labirent düzenleri
labyrinths = [
    [(100, 20, 450, 10), (100, 480, 350, 10), (100, 20, 10, 380), (200, 200, 10, 100), (300, 300, 100, 10), (400, 100, 10, 150)],
    [(150, 100, 500, 10), (50, 300, 100, 10), (500, 200, 10, 100), (300, 400, 10, 100), (200, 50, 200, 10), (400, 300, 10, 200)],
    [(50, 50, 100, 10), (200, 100, 10, 100), (400, 50, 10, 200), (300, 250, 100, 10), (100, 300, 10, 100), (500, 400, 100, 10)]
]

# Oyun sahnesi ayarları
win_width = 700  # Pencere genişliği
win_height = 500  # Pencere yüksekliği
window = display.set_mode((win_width, win_height))  # Pencereyi oluşturuyoruz
display.set_caption("Maze")  # Pencerenin başlığını ayarlıyoruz
background = transform.scale(image.load("background.jpg"), (win_width, win_height))  # Arka plan resmini yüklüyor ve ölçeklendiriyoruz

# Oyunun karakterlerini oluşturuyoruz
player = Player('hero.png', 5, win_height - 80, 4, 3)  # Oyuncu karakteri
monster1 = Enemy('cyborg.png', win_width - 80, 280, 2)  # Düşman karakteri 1
final = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)  # Hazine karakteri

walls = create_labyrinth(labyrinths[0])  # İlk labirenti oluşturuyoruz
labyrinth_index = 0  # İlk labirentin indeksini ayarlıyoruz

# Oyun döngüsü değişkenleri
game = True  # Oyun devam ediyor mu
finish = False  # Oyun bitti mi
clock = time.Clock()  # Saat objesi
FPS = 60  # Kare hızı
score = 0  # Başlangıç puanı
max_score = 80  # Kazanmak için gereken puan

# Yazı tipleri ve yazılar
font.init()  # Yazı tiplerini başlatıyoruz
main_font = font.Font(None, 90)  # Ana yazı tipi
win = main_font.render('VAMOSSS!!!', True, (255, 215, 0))  # Kazanma yazısı
lose = main_font.render('You Lost!', True, (180, 0, 0))  # Kaybetme yazısı
lives_font = font.Font(None, 35)  # Can yazı tipi
score_font = font.Font(None, 35)  # Puan yazı tipi

# Müzik ve ses efektleri
mixer.init()  # Ses mikserini başlatıyoruz
mixer.music.load('jungles.ogg')  # Arka plan müziğini yüklüyoruz
mixer.music.play()  # Arka plan müziğini çalıyoruz

money = mixer.Sound('money.ogg')  # Para ses efekti
kick = mixer.Sound('kick.ogg')  # Tekme ses efekti

# Çarpışma kontrol fonksiyonu
def check_collisions():
    global score, finish, walls, labyrinth_index  # Global değişkenler
    if sprite.collide_rect(player, monster1)  or any(sprite.collide_rect(player, wall) for wall in walls):  # Çarpışma kontrolü
        player.lives -= 1  # Oyuncunun canını azalt
        player.rect.x = 5  # Oyuncuyu başlangıç pozisyonuna taşı
        player.rect.y = win_height - 80  # Oyuncuyu başlangıç pozisyonuna taşı
        kick.play()  # Tekme sesini çal
        if player.lives == 0:  # Eğer can kalmadıysa
            finish = True  # Oyunu bitir
            window.blit(lose, (200, 200))  # Kaybetme yazısını göster
    if sprite.collide_rect(player, final):  # Eğer oyuncu hazineye ulaştıysa
        score += 10  # Puanı artır
        money.play()  # Para sesini çal
        final.rect.x = random.randint(50, win_width - 100)  # Hazineyi rastgele bir konuma taşı
        final.rect.y = random.randint(50, win_height - 100)  # Hazineyi rastgele bir konuma taşı
        labyrinth_index = (labyrinth_index + 1) % len(labyrinths)  # Sıradaki labirenti seç
        walls = create_labyrinth(labyrinths[labyrinth_index])  # Labirentleri değiştir
        if score >= max_score:  # Eğer puan yeterli ise
            finish = True  # Oyunu bitir
            window.blit(win, (200, 200))  # Kazanma yazısını göster

# Arka plan hareket fonksiyonu
def move_background(offset):
    window.blit(background, (0, offset))  # Arka planı çizer
    window.blit(background, (0, offset - win_height))  # Arka planı tekrar çizer

offset = 0  # Başlangıç offseti

# Ana oyun döngüsü
while game:
    for e in event.get():  # Olayları kontrol et
        if e.type == QUIT:  # Eğer çıkış olayı varsa
            game = False  # Oyunu bitir

    if not finish:  # Eğer oyun bitmediyse
        offset = (offset + 1) % win_height  # Offseti artır
        move_background(offset)  # Arka planı hareket ettir

        player.update()  # Oyuncuyu güncelle
        monster1.update()  # Düşman 1'i güncelle
        
        player.reset()  # Oyuncuyu çiz
        monster1.reset()  # Düşman 1'i çiz
        final.reset()  # Hazineyi çiz

        for wall in walls:  # Her duvar için
            wall.draw_wall()  # Duvarı çiz

        lives_text = lives_font.render(f'Lives: {player.lives}', True, (255, 255, 255))  # Can yazısını oluştur
        score_text = score_font.render(f'Score: {score}', True, (255, 255, 255))  # Puan yazısını oluştur
        window.blit(lives_text, (5, 5))  # Can yazısını ekrana çiz
        window.blit(score_text, (5, 35))  # Puan yazısını ekrana çiz

        check_collisions()  # Çarpışmaları kontrol et

    display.update()  # Ekranı güncelle
    clock.tick(FPS)  # FPS'yi ayarla
