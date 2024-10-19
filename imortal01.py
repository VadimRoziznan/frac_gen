import numpy as np
from PIL import Image
import math
import os
import sys

# Константы
horiz = 220  # Увеличено разрешение
vert = 170   # Увеличено разрешение

# Генерация палитры
# Определяем палитру в формате #RRGGBB
hex_colors = ['#182044', '#395198', '#54327D', '#C86AC6', '#082F50', '#1D8A85', '#165C5C', '#071739', '#266A73', '#03223E', '#0B2651', '#179796']
pal = np.zeros((256, 3), dtype=np.uint8)

# Преобразуем hex-цвета в RGB
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

rgb_colors = [hex_to_rgb(color) for color in hex_colors]

# Заполним палитру циклами через указанные цвета
num_colors = len(rgb_colors)
for i in range(256):
    pal[i] = rgb_colors[i % num_colors]

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


# Функция для отображения прогресс-бара
def print_progress_bar(iteration, total, length=50, fill='█'):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r|{bar}| {percent}% Complete')
    sys.stdout.flush()

# Создание анимации
frames = []
num_frames = 100  # Количество кадров в анимации

# Центрирование на интересной части множества Мандельброта
absc = -0.743643887037158704752191506114774  # Центр множества
ordi = 0.131825904205311970493132056385139  # Центр множества
start_size = 0.01000000
end_size = 0.0000000001   # Не уменьшайте слишком сильно

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
frames[0].save('Mandelbrot_animation09.gif', save_all=True, append_images=frames[1:], loop=0, duration=30)
print("Анимация сохранена как Mandelbrot_animation05.gif")