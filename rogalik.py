import arcade
from random import randint
from time import time

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
TITLE = "ROGALIK"
# Тож костанты но это характеристики их можно менять)
MOVE_MAX_SPEED = 4
BULET_SPEED = 49
BOOST_PLAYER = 0.2
ZOMBEE_MAX_SPEED = 1
ZOMBEE_KOLVO = 50

score = 0
timer = 0

class Game(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color([50, 50, 50])
        self.player = Player()
        self.bulet = Bulet()
        self.scene = arcade.Scene()
        self.zombee_list = []
        self.time = time()

    def setup(self):
        self.scene.add_sprite("Bulet", self.bulet)
        self.scene.add_sprite("Player", self.player)
        # Спавн зомби
        for i in range(ZOMBEE_KOLVO):
            self.zombee = Zombee()
            self.lst = random_spawn()
            self.zombee.center_x = self.lst[0]
            self.zombee.center_y = self.lst[1]
            self.zombee_list.append(self.zombee)
            self.scene.add_sprite(f"Zombee{i}", self.zombee_list[i])

    def on_draw(self):
        self.clear()
        self.scene.draw()
        arcade.draw_text(f"health: {self.player.health//10}", 10, 50, [255, 255, 255], 15)
        arcade.draw_text(f"score: {score//100}", 10, 30, [255, 255, 255], 15)
        arcade.draw_text(f"time: {(time() - self.time)//1}", 10, 10, [255, 255, 255], 15)

    def update(self, delta_time: float):
        self.scene.update()

        # Ходьба
        if self.player.walk_w and self.player.change_y < self.player.max_speed:
            self.player.change_y += BOOST_PLAYER
        if not self.player.walk_w and self.player.change_y > 0:
            self.player.change_y -= BOOST_PLAYER
        if self.player.walk_a and self.player.change_x > -self.player.max_speed:
            self.player.change_x -= BOOST_PLAYER
        if not self.player.walk_a and self.player.change_x < 0:
            self.player.change_x += BOOST_PLAYER
        if self.player.walk_s and self.player.change_y > -self.player.max_speed:
            self.player.change_y -= BOOST_PLAYER
        if not self.player.walk_s and self.player.change_y < 0:
            self.player.change_y += BOOST_PLAYER
        if self.player.walk_d and self.player.change_x < self.player.max_speed:
            self.player.change_x += BOOST_PLAYER
        if not self.player.walk_d and self.player.change_x > 0:
            self.player.change_x -= BOOST_PLAYER
        # Фикс багов пайтона или моих))
        if BOOST_PLAYER > self.player.change_y > 0 and not self.player.walk_w:
            self.player.change_y = 0
        if -BOOST_PLAYER < self.player.change_y < 0 and not self.player.walk_s:
            self.player.change_y = 0
        if BOOST_PLAYER > self.player.change_x > 0 and not self.player.walk_d:
            self.player.change_x = 0
        if -BOOST_PLAYER < self.player.change_x < 0 and not self.player.walk_a:
            self.player.change_x = 0
        # print(self.player.change_x, self.player.change_y)

        # Передвижение зомби
        for j in range(ZOMBEE_KOLVO):
            if self.player.center_x - 2 < self.zombee_list[j].center_x < self.player.center_x + 2:
                self.zombee_list[j].change_x = 0
            if self.player.center_y - 2 < self.zombee_list[j].center_y < self.player.center_y + 2:
                self.zombee_list[j].change_y = 0
            if self.zombee_list[j].center_x > self.player.center_x + 2:
                self.zombee_list[j].change_x = -self.zombee_list[j].speed
            if self.zombee_list[j].center_x < self.player.center_x - 2:
                self.zombee_list[j].change_x = self.zombee_list[j].speed
            if self.zombee_list[j].center_y > self.player.center_y + 2:
                self.zombee_list[j].change_y = -self.zombee_list[j].speed
            if self.zombee_list[j].center_y < self.player.center_y - 2:
                self.zombee_list[j].change_y = self.zombee_list[j].speed

        # Смерть зомби
        for l in range(ZOMBEE_KOLVO):
            if self.zombee_list[l].health < 1:
                self.lst = random_spawn()
                self.zombee_list[l].center_x = self.lst[0]
                self.zombee_list[l].center_y = self.lst[1]
                self.zombee_list[l].health = 1000
                global score
                score += 200

        # Смерть игрока
        if self.player.health < 0:
            view = GameOverView()
            self.window.show_view(view)
            global timer
            timer = time() - self.time

        # Очки
        score += 1

        # Колизии
        for i in range(ZOMBEE_KOLVO):
            if arcade.check_for_collision(self.player, self.zombee_list[i]):
                self.player.health -= 1
            if arcade.check_for_collision(self.bulet, self.zombee_list[i]):
                self.zombee_list[i].health -= 400


    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.W:
            self.player.walk_w = True
        if symbol == arcade.key.A:
            self.player.walk_a = True
        if symbol == arcade.key.S:
            self.player.walk_s = True
        if symbol == arcade.key.D:
            self.player.walk_d = True
        # Стрельба
        if symbol == arcade.key.SPACE and self.bulet.out_of:
            self.bulet.center_x = self.player.center_x
            self.bulet.center_y = self.player.center_y
            if self.player.texture == self.player.w_texture:
                self.bulet.angle = 0
                self.bulet.change_x = 0
                self.bulet.change_y = BULET_SPEED
            if self.player.texture == self.player.s_texture:
                self.bulet.angle = 180
                self.bulet.change_x = 0
                self.bulet.change_y = -BULET_SPEED
            if self.player.texture == self.player.d_texture:
                self.bulet.angle = 270
                self.bulet.change_x = BULET_SPEED
                self.bulet.change_y = 0
            if self.player.texture == self.player.a_texture:
                self.bulet.angle = 90
                self.bulet.change_x = -BULET_SPEED
                self.bulet.change_y = 0
            if self.player.texture == self.player.wd_texture:
                self.bulet.angle = 315
                self.bulet.change_x = BULET_SPEED
                self.bulet.change_y = BULET_SPEED
            if self.player.texture == self.player.sd_texture:
                self.bulet.angle = 225
                self.bulet.change_x = BULET_SPEED
                self.bulet.change_y = -BULET_SPEED
            if self.player.texture == self.player.as_texture:
                self.bulet.angle = 135
                self.bulet.change_x = -BULET_SPEED
                self.bulet.change_y = -BULET_SPEED
            if self.player.texture == self.player.wa_texture:
                self.bulet.angle = 45
                self.bulet.change_x = -BULET_SPEED
                self.bulet.change_y = BULET_SPEED

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.W:
            self.player.walk_w = False
        if symbol == arcade.key.A:
            self.player.walk_a = False
        if symbol == arcade.key.S:
            self.player.walk_s = False
        if symbol == arcade.key.D:
            self.player.walk_d = False


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.s_texture = arcade.load_texture("1.png")
        self.sd_texture = arcade.load_texture("2.png")
        self.d_texture = arcade.load_texture("3.png")
        self.wd_texture = arcade.load_texture("4.png")
        self.w_texture = arcade.load_texture("5.png")
        self.wa_texture = arcade.load_texture("6.png")
        self.a_texture = arcade.load_texture("7.png")
        self.as_texture = arcade.load_texture("8.png")
        self.texture = self.s_texture
        self.center_x = 400
        self.center_y = 400
        self.change_x = 0
        self.change_y = 0
        self.walk_w = False
        self.walk_a = False
        self.walk_s = False
        self.walk_d = False
        self.health = 1000
        self.max_speed = MOVE_MAX_SPEED

    def update(self):
        # Передвижение
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.center_x <= 25:
            self.center_x = 25
        if self.center_x >= SCREEN_WIDTH - 25:
            self.center_x = SCREEN_WIDTH - 25
        if self.center_y >= SCREEN_HEIGHT - 25:
            self.center_y = SCREEN_HEIGHT - 25
        if self.center_y <= 25:
            self.center_y = 25
        # Изменение текстур
        if self.walk_w and self.walk_d:
            self.texture = self.wd_texture
        if self.walk_w and self.walk_a:
            self.texture = self.wa_texture
        if self.walk_s and self.walk_d:
            self.texture = self.sd_texture
        if self.walk_a and self.walk_s:
            self.texture = self.as_texture
        if self.walk_d and not self.walk_w and not self.walk_a and not self.walk_s:
            self.texture = self.d_texture
        if self.walk_a and not self.walk_w and not self.walk_d and not self.walk_s:
            self.texture = self.a_texture
        if self.walk_w and not self.walk_d and not self.walk_a and not self.walk_s:
            self.texture = self.w_texture
        if self.walk_s and not self.walk_w and not self.walk_a and not self.walk_d:
            self.texture = self.s_texture


class Bulet(arcade.Sprite):
    def __init__(self):
        super().__init__("bulet.png", 0.8)
        self.center_x = -10
        self.center_y = -10
        self.change_y = 0
        self.change_x = 0
        self.out_of = True

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.center_x < 0 or self.center_x > SCREEN_WIDTH or self.center_y < 0 or self.center_y > SCREEN_HEIGHT:
            self.out_of = True
        else:
            self.out_of = False


class Zombee(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.s_texture = arcade.load_texture("z1.png")
        self.sd_texture = arcade.load_texture("z2.png")
        self.d_texture = arcade.load_texture("z3.png")
        self.wd_texture = arcade.load_texture("z4.png")
        self.w_texture = arcade.load_texture("z5.png")
        self.wa_texture = arcade.load_texture("z6.png")
        self.a_texture = arcade.load_texture("z7.png")
        self.as_texture = arcade.load_texture("z8.png")
        self.texture = self.s_texture
        self.center_x = 100
        self.center_y = 100
        self.change_x = 0
        self.change_y = 0
        self.health = 1000
        self.speed = randint(1, ZOMBEE_MAX_SPEED*10)/10

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        # Изменение текстур
        if self.change_x > 0 and self.change_y > 0:
            self.texture = self.wd_texture
        if self.change_x < 0 < self.change_y:
            self.texture = self.wa_texture
        if self.change_x > 0 > self.change_y:
            self.texture = self.sd_texture
        if self.change_x < 0 and self.change_y < 0:
            self.texture = self.as_texture
        if self.change_x > 0 and self.change_y == 0:
            self.texture = self.d_texture
        if self.change_x < 0 and self.change_y == 0:
            self.texture = self.a_texture
        if self.change_x == 0 and self.change_y > 0:
            self.texture = self.w_texture
        if self.change_x == 0 and self.change_y < 0:
            self.texture = self.s_texture


def random_spawn():
    a = randint(1, 4)
    lst = []
    if a == 1:
        lst.append(randint(-300, -50))
        lst.append(randint(100, 700))
    if a == 2:
        lst.append(randint(800, 1050))
        lst.append(randint(100, 700))
    if a == 3:
        lst.append(randint(100, 700))
        lst.append(randint(-300, -50))
    if a == 4:
        lst.append(randint(100, 700))
        lst.append(randint(800, 1050))
    return lst


class InstructionView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color([50, 50, 50])
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        self.clear()
        arcade.draw_text("ИГРА ПРО ЗОМБИ", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 200, [255, 255, 255], font_size=50, anchor_x="center")
        arcade.draw_text("В игре нужно бегать от зомби и убивать их", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, [255, 255, 255], font_size=20, anchor_x="center")
        arcade.draw_text("Бег на wasd, стрельба на пробел", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40, [255, 255, 255], font_size=20, anchor_x="center")
        arcade.draw_text("Что-бы продолжить нажмите на SPACE", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 80, [255, 255, 255], font_size=20, anchor_x="center")

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            game_view = Game()
            game_view.setup()
            self.window.show_view(game_view)


class GameOverView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color([50, 50, 50])
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
        global score, timer

    def on_draw(self):
        self.clear()
        arcade.draw_text("Ты умер", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 200, [255, 255, 255], font_size=50,anchor_x="center")
        arcade.draw_text(f"Твой счёт: {score//100}", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, [255, 255, 255], font_size=20, anchor_x="center")
        arcade.draw_text(f"Время жизни {timer//1} сек", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40, [255, 255, 255], font_size=20, anchor_x="center")
        arcade.draw_text("Нажми SPACE что-бы отомстить", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 80, [255, 255, 255], font_size=20, anchor_x="center")
        arcade.draw_text("Нажми Esc что-бы сдаться", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 120, [255, 255, 255], font_size=20, anchor_x="center")

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            global score
            score = 0
            game_view = Game()
            game_view.setup()
            self.window.show_view(game_view)
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    start_view = InstructionView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()