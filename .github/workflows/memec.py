from kivy.app import App
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.label import Label
from random import randint, choice
import os

class CryptoMemeApp(App):
    def build(self):
        # Настройка окна приложения
        Window.clearcolor = (0.1, 0.1, 0.1, 1)  # Темный фон
        Window.title = "Crypto Meme Miner"      # Заголовок окна
        
        # Основной контейнер для элементов
        self.layout = FloatLayout()
        
        # Добавляем изображение криптовалюты
        self.crypto_img = Image(
            source='assets/bitcoin.png',
            size_hint=(None, None),
            size=(150, 150),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            opacity=0.9  # Небольшая прозрачность
        )
        self.crypto_img.bind(on_touch_down=self.spawn_meme)
        self.layout.add_widget(self.crypto_img)
        
        # Счетчик мемов
        self.counter = 0
        self.counter_label = Label(
            text='Memes mined: 0',
            pos_hint={'x': 0.02, 'top': 0.98},
            color=(0.3, 0.7, 0.2, 1),
            font_size='20sp',
            bold=True
        )
        self.layout.add_widget(self.counter_label)
        
        return self.layout

    def spawn_meme(self, instance, touch):
        # Проверяем, что клик был по изображению крипты
        if not self.crypto_img.collide_point(*touch.pos):
            return
        
        # Обновляем счетчик
        self.counter += 1
        self.counter_label.text = f'Memes mined: {self.counter}'
        
        # Создаем мем
        meme = Image(
            source=choice(self.get_memes_list()),
            size_hint=(None, None),
            size=(300, 300),
            pos=(randint(20, Window.width-320), -300),  # Начальная позиция
            opacity=0
        )
        self.layout.add_widget(meme)
        
        # Анимация появления и исчезновения
        anim = Animation(
            y=randint(100, Window.height-400),
            opacity=1,
            duration=0.7,
            transition='out_quad'
        ) + Animation(
            opacity=0,
            duration=1.2,
            transition='in_quad'
        )
        
        # Запускаем анимацию и удаляем мем после завершения
        anim.start(meme)
        anim.bind(on_complete=lambda *x: self.layout.remove_widget(meme))

    def get_memes_list(self):
        # Получаем список доступных мемов
        memes_folder = 'memes'
        try:
            return [os.path.join(memes_folder, f) for f in os.listdir(memes_folder) 
                    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        except FileNotFoundError:
            print(f"Error: Folder '{memes_folder}' not found!")
            return []

if __name__ == '__main__':
    CryptoMemeApp().run()