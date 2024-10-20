import numpy as np
from PIL import Image
import math
import os

# Константы
horiz = 220  # Увеличено разрешение
vert = 170   # Увеличено разрешение

# Генерация палитры
pal = np.zeros((256, 3), dtype=np.uint8)
for a in range(255):
    # Получаем оттенки синего и фиолетового
    pal[a][0] = round(50 + 50 * math.sin(2 * math.pi * (a + 16) / 255))  # Красный компонент
    pal[a][1] = round(50 + 50 * math.cos(2 * math.pi * (a + 16) / 255))  # Зеленый компонент
    pal[a][2] = round(150 + 100 * math.sin(2 * math.pi * (a + 16) / 255))  # Синий компонент
pal[255] = [255, 255, 255]  # Белый цвет для последней палитры

# Создание изображения множества Мандельброта
def generate_mandelbrot(horiz, vert, absc, ordi, size):
    image = np.zeros((vert, horiz), dtype=np.float32)
    step = size / horiz
    absc2 = absc - step * (horiz - 1) / 2
    ordi2 = ordi - step * (vert - 1) / 2

    max_iter = 1000  # Увеличенное количество итераций для улучшения детализации

    for b in range(vert):
        n = ordi2 + b * step
        for a in range(horiz):
            m = absc2 + a * step
            c = complex(m, n)
            z = complex(0, 0)
            t = 0
            while abs(z) <= 2.0 and t < max_iter:
                z = z * z + c
                t += 1
            if t < max_iter:
                # Сглаженное значение
                mu = t - math.log(math.log(abs(z))) / math.log(2)
                image[b, a] = mu
            else:
                image[b, a] = max_iter

    return image

# Функция для сохранения изображений в папку
def save_images(frames, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    for i, frame in enumerate(frames):
        filename = os.path.join(directory, f"frame_{i+1:03}.png")
        frame.save(filename)
        print(f"Изображение {filename} сохранено.")

# Создание анимации
frames = []
num_frames = 100  # Количество кадров в анимации

# Генерируем случайные значения для параметров
absc = -0.743643887037158704752191506114774  # -1.96680095
ordi = 0.131825904205311970493132056385139  # 0.00000478
start_size = 0.01000000 # 0.00000014
end_size = 0.0000000001   # 0.00000001

for i in range(num_frames):
    # Рассчитываем размер для текущего кадра
    size = start_size * (end_size / start_size) ** (i / (num_frames - 1))

    # Генерация изображения
    mandelbrot_image = generate_mandelbrot(horiz, vert, absc, ordi, size)

    # Нормализация и применение палитры
    mandelbrot_image = mandelbrot_image / mandelbrot_image.max() * 255
    mandelbrot_image = mandelbrot_image.astype(np.uint8)

    colored_image = np.zeros((vert, horiz, 3), dtype=np.uint8)
    for j in range(256):
        colored_image[mandelbrot_image == j] = pal[j]

    # Добавление кадра в список
    frames.append(Image.fromarray(colored_image, 'RGB'))
    print(f"Кадр {i + 1}/{num_frames} готов")

# Добавление первого кадра в конец для бесшовной анимации
frames.append(frames[0])
print("Первый кадр добавлен в конец для создания эффекта бесконечной анимации.")

# Сохранение изображений в папку
save_images(frames, "Mandelbrot_Frames")

# Сохранение анимации в виде GIF
frames[0].save('Mandelbrot_animation08.gif', save_all=True, append_images=frames[1:], loop=0, duration=30)
print("Анимация сохранена как Mandelbrot_animation08.gif")