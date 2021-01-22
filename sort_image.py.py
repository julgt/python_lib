# в папке получаем данные по изображени€м и сортируем их по дате редактировани€,
# открываем изображени€ по очереди
# Ќќ не закрываем
#

import os
import time
import webbrowser
# from PilLite import Image


path_to_watch='D:/temp/images'

def file_info(directory, sortLastModifiedOrNaw=False):
    file_list = []
    currentMin = 0
    for i in os.listdir(directory):
        a = os.stat(os.path.join(directory,i))
        if sortLastModifiedOrNaw == True:
            if a.st_atime > currentMin:
                currentMin = a.st_atime
                file_list.append([i,time.ctime(a.st_atime),time.ctime(a.st_ctime)])
            else:
                file_list.insert(0,[i,time.ctime(a.st_atime),time.ctime(a.st_ctime)])
        else:
            file_list.append([i,time.ctime(a.st_atime),time.ctime(a.st_ctime)])
    return file_list

file_list2 = file_info(path_to_watch,sortLastModifiedOrNaw=True)

for item in file_list2:
    line = "Name: {:<20} | Date Last Accesed: {:>20} | Date Created: {:>20}".format(item[0],item[1],item[2])
    print(line)

print()
for item in file_list2:
    g=path_to_watch+'/'+item[0]
    # f = Image.open(g).show()
    os.system('start '+path_to_watch+'/'+item[0])
    # webbrowser.open(path_to_watch+'/'+item[0])
    time.sleep(3)
    # ImageTk.PhotoImage(Image.open(path_to_watch+'/'+item[0]))
    print(item[0])


# os.system('taskkill /F '+path_to_watch+'/'+item[0])
