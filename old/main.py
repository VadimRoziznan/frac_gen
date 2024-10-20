from PIL import Image
import numpy as np
import random


# Функция для создания изображения с фракталом Мандельброта
def create_random_fractal_image(width, height, filename):
    # Генерация случайных параметров для множества Мандельброта
    re_center = random.uniform(-0.7, 0.7)
    im_center = random.uniform(-0.7, 0.7)
    zoom_factor = random.uniform(1, 10)

    re_range = 3.5 / zoom_factor
    im_range = 3.0 / zoom_factor

    re_min = re_center - re_range / 2
    re_max = re_center + re_range / 2
    im_min = im_center - im_range / 2
    im_max = im_center + im_range / 2

    max_iter = random.randint(100, 1000)

    # Создание массива для хранения значений фрактала
    mandelbrot_set = np.zeros((height, width), dtype=np.uint8)

    # Генерация множества Мандельброта
    for x in range(width):
        for y in range(height):
            # Преобразование координат пикселей в комплексную плоскость
            c = complex(re_min + (x / width) * (re_max - re_min),
                        im_min + (y / height) * (im_max - im_min))
            z = 0
            iteration = 0
            while abs(z) <= 2 and iteration < max_iter:
                z = z * z + c
                iteration += 1
            # Сохранение количества итераций
            mandelbrot_set[y, x] = int(255 * iteration / max_iter)

    # Создание изображения
    image = Image.fromarray(mandelbrot_set, mode='L')
    image.save(filename)
    print(f"Изображение сохранено как {filename}")


# Создаем случайное изображение 800x600 и сохраняем его
create_random_fractal_image(800, 600, 'random_mandelbrot_set.png')