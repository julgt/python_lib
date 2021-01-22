# https://habr.com/ru/post/163663/
# Играем с изображениями python
import hashlib
import random
import os
import time
import shutil
from io import BytesIO
from operator import itemgetter
from PIL import Image, ImageDraw #Подключим необходимые библиотеки.

in_path= 'D:/temp/in'
inProgress_path= 'D:/temp/inProgress'
base_path = 'D:/temp/images'
out_path = 'D:/temp/out'

# блок try здесь для того, чтобы не копировать каждый раз файлы в папку in
# потом убрать
# try:
#     if (len(os.listdir(in_path))!=0):
#         print(os.listdir(in_path))
#         print(len(os.listdir(in_path)))
# except: print()
# else:
#     for item in os.listdir(base_path):
#         shutil.copy(base_path+'/'+item, in_path)


# поучаем список изображений в папке и сортируем их по дате Date Last Accesed
def file_info(directory, sortLastModifiedOrNaw=False):
    file_list = []
    currentMin = 0
    for i in os.listdir(directory):
        a = os.stat(os.path.join(directory, i))
        if sortLastModifiedOrNaw == True:
            if a.st_atime > currentMin:
                currentMin = a.st_atime
                file_list.append([i, time.ctime(a.st_atime), time.ctime(a.st_ctime)])
            else:
                file_list.insert(0, [i, time.ctime(a.st_atime), time.ctime(a.st_ctime)])
        else:
            file_list.append([i, time.ctime(a.st_atime), time.ctime(a.st_ctime)])
    return file_list


# масштабирование изображения
def scale_image(input_image_path,
                output_image_path,
                width=None,
                height=None
                ):
    # input_image_path = Image.open(input_image_path)
    w, h = input_image_path.size
    print('The original image size is {wide} wide x {height} '
          'high'.format(wide=w, height=h))

    if width and height:
        max_size = (width, height)
    elif width:
        max_size = (width, h)
    elif height:
        max_size = (w, height)
    else:
        # No width or height specified
        raise RuntimeError('Width or height required!')

    input_image_path.thumbnail(max_size, Image.ANTIALIAS)
    input_image_path.save(output_image_path)

    scaled_image = Image.open(output_image_path)
    width, height = scaled_image.size
    print('The scaled image size is {wide} wide x {height} '
          'high'.format(wide=width, height=height))

if (os.path.exists(in_path)):
    file_list = file_info(in_path,sortLastModifiedOrNaw=True)

    for item in file_list:
        line = "Name: {:<20} | Date Last Accesed: {:>20} | Date Created: {:>20}".format(item[0],item[1],item[2])
        print(line)

    for item in file_list:
        img = in_path + '/' + item[0]
        file_name = item[0].replace(".png","").replace(".jpg","").replace(".gif","")
        print(file_name)

        # mode = int(input('mode:')) #Считываем номер преобразования.
        image = Image.open(img)  # Открываем изображение.
        draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования.
        width = image.size[0]  # Определяем ширину.
        height = image.size[1]  # Определяем высоту.
        pix = image.load()  # Выгружаем значения пикселей.

        # переводим в черно-белое
        # factor = int(input('factor:'))
        factor = 70
        for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                S = a + b + c
                if (S > (((255 + factor) // 2) * 3)):
                    a, b, c = 255, 255, 255
                else:
                    a, b, c = 0, 0, 0
                draw.point((i, j), (a, b, c))
        image.save(inProgress_path + '/' + file_name + "______.jpg")
        del draw

        img_new_resize=(inProgress_path + '/' + file_name + "_scaled.gif")
        scale_image(image,img_new_resize,width=280)
        shutil.move(img, inProgress_path)

        inletter = False
        foundletter = False
        start = 0
        end = 0

        letters = []


        # Получение строки для BytesIO
        img_data = None
        with open(img_new_resize, 'rb') as fh:
            img_data = fh.read()
        # Создание PIL.Image на основе строки
        with BytesIO(img_data) as img_buf:
            with Image.open(img_buf) as img:
                # img = img.convert("P")  ## убрать потом??
                for y in range(img.size[0]):  # slice across
                    for x in range(img.size[1]):  # slice down
                        pix = img.getpixel((y, x))
                        if pix != 255:
                            inletter = True
                    if foundletter == False and inletter == True:
                        foundletter = True
                        start = y

                    if foundletter == True and inletter == False:
                        foundletter = False
                        end = y
                        letters.append((start, end))

                    inletter = False
                print(letters)

                # здесь разбиваем капчу на символы отдельные
                # и сохраняем изображения в текущей папке
                count = 0
                for letter in letters:
                    m = hashlib.md5()
                    im3 = img.crop((letter[0], 0, letter[1], img.size[1]))
                    m.update(repr("%s%s" % (time.time(), count)).encode('utf-8'))
                    im3.save(inProgress_path + '/' + "./%s.gif" % (m.hexdigest()))
                    count += 1


else:
    print("error! что-то пошло не так !!!!!!!!!!!!!!")
