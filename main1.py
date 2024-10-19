import numpy as np
from PIL import Image
import math
import random
# Генирация изображений
# Константы
horiz = 1024
vert = 1024

absc = -1.96680095
ordi = 0.00000478
size = 0.00000014


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
    image = np.zeros((vert, horiz), dtype=np.uint8)
    step = size / horiz
    absc2 = absc - step * (horiz - 1) / 2
    ordi2 = ordi - step * (vert - 1) / 2

    for b in range(vert):
        n = ordi2 + b * step
        for a in range(horiz):
            m = absc2 + a * step
            c = complex(m, n)
            z = complex(0, 0)
            t = 4081
            while t > 0:
                z = z * z + c
                if (z.real * z.real + z.imag * z.imag) > 1000000.0:  # Выход за предел
                    break
                t -= 1
            if t == 0:
                image[b, a] = 255
            else:
                image[b, a] = t % 255
    return image

# Генерация изображения
mandelbrot_image = generate_mandelbrot(horiz, vert, absc, ordi, size)

# Применение палитры
colored_image = np.zeros((vert, horiz, 3), dtype=np.uint8)
for i in range(256):
    colored_image[mandelbrot_image == i] = pal[i]

# Создание и сохранение изображения
img = Image.fromarray(colored_image, 'RGB')
img.save('Mandelbrot7.bmp')
print("Изображение сохранено как Mandelbrot7.bmp")