# https://habr.com/ru/post/149091/ Декодирование капчи на python
from PIL import Image
import hashlib
import time
import math
import os

from io import BytesIO
import cv2
import difflib

# разбиваем цветное зашумленное изображение,
# переведеннное в черно-белое первым способом
# где нужно знать гистограммму цветов текущего изображения -
# не подходит для массового использования

out_path = 'D:/temp/out'

im = Image.open("UM-UGM-1.png")
# im = Image.open("captcha-internet-infozet_scaled.jpg")
im = im.convert("P")
im2 = Image.new("P", im.size, 255)
#
im = im.convert("P")

temp = {}

for x in range(im.size[1]):
    for y in range(im.size[0]):
        pix = im.getpixel((y, x))
        temp[pix] = pix
        if pix == 218 or pix == 1:  # 220 227 these are the numbers to get
            im2.putpixel((y, x), 0)
im2.save("output.gif")
# new code starts here

inletter = False
foundletter = False
start = 0
end = 0

letters = []

for y in range(im2.size[0]):  # slice across
    for x in range(im2.size[1]):  # slice down
        pix = im2.getpixel((y, x))
        if pix != 255:  #255
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

iconset = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
imageset = []
# Функция вычисления хэша
def CalcImageHash(FileName):
    image = cv2.imread(FileName)  # Прочитаем картинку
    # print("image.shape "+image.shape)
    resized = cv2.resize(image, (8, 8), interpolation=cv2.INTER_AREA)  # Уменьшим картинку
    gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)  # Переведем в черно-белый формат
    avg = gray_image.mean()  # Среднее значение пикселя
    ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0)  # Бинаризация по порогу

    # Рассчитаем хэш
    _hash = ""
    for x in range(8):
        for y in range(8):
            val = threshold_image[x, y]
            if val == 255:
                _hash = _hash + "1"
            else:
                _hash = _hash + "0"

    return _hash


def CompareHash(hash1, hash2):
    l = len(hash1)
    i = 0
    count2 = 0
    while i < l:
        if hash1[i] != hash2[i]:
            count2 = count2 + 1
        i = i + 1
    return count2
str=''


for letter in letters:
    m = hashlib.md5()
    im3 = im2.crop((letter[0], 0, letter[1], im2.size[1]))
    m.update(repr("%s%s" % (time.time(), count)).encode('utf-8'))
    im = out_path + '/' + "%s.gif" % (m.hexdigest())
    im3.save(im)
    count += 1

    # # Получение строки для BytesIO
    # img_data = None
    # with open(im, 'rb') as fh:
    #     img_data = fh.read()
    # # Создание PIL.Image на основе строки
    # with BytesIO(img_data) as img_buf:
    #     with Image.open(img_buf) as img:

    hash1 = CalcImageHash(im)
    print("hash1: "+hash1)
# отсюда мое

    for letter2 in iconset:
        for img in os.listdir('C:/1/%s/' % (letter2)):
            hash2 = CalcImageHash(img)
            print("hash1: " + hash1)
            index = CompareHash(hash1, hash2)
            if (index <= 5):
                print(index)
                str=str+letter2

print("капча: "+str)


# # Код ниже не работает.проблемы в классе с векторным пространством
# # #
# # # векторное пространство
# class VectorCompare:
#     def magnitude(self, concordance):
#         total = 0
#         for word, count in concordance.items():  # iteritems
#             total += count ** 2
#         return math.sqrt(total)
#
#     def relation(self, concordance1, concordance2): #(v.relation(y[0], buildvector(im3))
#         relevance = 0
#         topvalue = 0
#         for word, count in concordance1.items():  # iteritems
#             if concordance2.__contains__(word):  # if concordance2.has_key(word):
#                 topvalue += count * concordance2.__contains__(word)
#         return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))
#
#
# # загружаем обучающее множество, чтобы иметь возможность сравнивать с ним:
# def buildvector(im):
#     d1 = {}
#     count = 0
#     for i in im.getdata():
#         d1[count] = i
#         count += 1
#     return d1
#
#
# v = VectorCompare()
#
# # iconset = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
# # 'n', 'o', 'p', 'q', 'r', 's', 't', 'u','v','w','x','y','z']
#
# iconset = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
#
# imageset = []
#
# for letter in iconset:
#     for img in os.listdir('C:/1/%s/' % (letter)):
#         temp = []
#         if img != "Thumbs.db":
#             temp.append(buildvector(Image.open("C:/1/%s/%s" % (letter, img))))
#         imageset.append({letter: temp})
#
# # определяем, где находится каждый символ и проверяем его с помощью нашего векторного пространства.
# # Затем сортируем результаты и печатаем их.
# count = 0
# for letter in letters:
#     m = hashlib.md5()
#     im3 = im2.crop((letter[0], 0, letter[1], im2.size[1]))
#     im3.save("output1111.gif")
#
#     guess = []
#
#     for image in imageset:
#         for x, y in image.items():
#             if len(y) != 0:
#                 guess.append((v.relation(y[0], buildvector(im3)), x))
#
#     guess.sort(reverse=True)
#     print("", guess[0])
#     count += 1
