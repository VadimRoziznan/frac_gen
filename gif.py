import sys
import numba
import numpy as np
from PIL import Image
import math
import os
import colorsys

# Константы
horiz = 360  # Увеличено разрешение
vert = 640   # Увеличено разрешение


# Создаем палитру с 256 цветами
pal = np.zeros((256, 3), dtype=np.uint8)

# Генерируем цвета спектра
for a in range(255):
    # Меняем оттенок от 0 до 1 (соответствующий 0-360 градусам)
    hue = a / 255.0
    # Конвертируем HSV в RGB (с полной насыщенностью и яркостью)
    r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    # Переводим значения из диапазона 0-1 в 0-255 и сохраняем в палитру
    pal[a] = [int(r * 255), int(g * 255), int(b * 255)]

# Последний цвет белый
pal[255] = [0, 0, 0]


# # Генерация палитры
# pal = np.zeros((256, 3), dtype=np.uint8)
# for a in range(255):
#     # Получаем оттенки синего и фиолетового
#     pal[a][0] = round(50 + 50 * math.sin(2 * math.pi * (a + 16) / 255))  # Красный компонент
#     pal[a][1] = round(50 + 50 * math.cos(2 * math.pi * (a + 16) / 255))  # Зеленый компонент
#     pal[a][2] = round(150 + 100 * math.sin(2 * math.pi * (a + 16) / 255))  # Синий компонент
# pal[255] = [255, 255, 255]  # Белый цвет для последней палитры

# Создание изображения множества Мандельброта
@numba.jit(nopython=True)
def generate_mandelbrot(horiz, vert, absc, ordi, size):
    image = np.zeros((vert, horiz), dtype=np.float32)
    step = size / horiz
    absc2 = absc - step * (horiz - 1) / 2
    ordi2 = ordi - step * (vert - 1) / 2

    max_iter = 2500  # Увеличенное количество итераций для улучшения детализации

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

# Функция для отображения прогресс-бара
def print_progress_bar(iteration, total, length=50, fill='█'):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r|{bar}| {percent}% Complete')
    sys.stdout.flush()

# Создание анимации
frames = []
num_frames = 1000  # Количество кадров в анимации

# # Генерируем случайные значения для параметров
# absc = -1.96680095  # -1.96680095
# ordi = 0.00000478  # 0.00000478
# start_size = 0.10000000 # 0.00000014
# end_size = 0.0000000001   # 0.00000001
# # Центрирование на интересной части множества Мандельброта
# # Пример координат для красивых фигур
# absc = -0.745428  # Центр множества
# ordi = 0.113009  # Центр множества
# start_size = 0.005
# end_size = 0.0000001  # Не уменьшайте слишком сильно

# # Центрирование на интересной части множества Мандельброта
# # Начало с большой известной фигуры и углубление в более мелкие детали
# absc = -0.743643887037158704752191506114774 # Центр множества
# ordi = 0.131825904205311970493132056385139 # Центр множества
# start_size = 2.0 # Начальное большое масштабирование
# end_size = 0.0001 # Конечное маленькое масштабирование

# # Генерируем случайные значения для параметров
# absc = -1.9668009503795  # -1.96680095 X
# ordi = 0.0000047800105  # 0.00000478 Y
# start_size =0.0005 # 0.00000014
# end_size = 0.0000000000001   # 0.00000001

absc = -0.743643887037158704752191506114774
ordi = 0.131825904205311970493132056385139
start_size = 15.5
end_size = 0.000000001



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
    # Обновление прогресс-бара
    print_progress_bar(i + 1, num_frames)

# Сохранение изображений в папку
save_images(frames, "Mandelbrot_Frames")

# Сохранение анимации в виде GIF
frames[0].save('Mandelbrot_animation07(без белого).gif', save_all=True, append_images=frames[1:], loop=0, duration=33)
print("Анимация сохранена как Mandelbrot_animation05.gif")

