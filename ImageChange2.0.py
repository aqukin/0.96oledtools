import multiprocessing
import os
import tkinter
import tkinter.messagebox
from queue import PriorityQueue
from tkinter import *
from tkinter.filedialog import askopenfilename

from PIL import Image, ImageSequence

findex = 0
codeIndex = 0
eachFramesTime = []

result_queue = PriorityQueue()


def saveFps(PIL_Image_object):
    """
    保存gif每一帧
    """
    if not os.path.exists(os.getcwd() + '\\gifOutput'):
        os.mkdir(os.getcwd() + '\\gifOutput')
        os.chdir(os.getcwd())
        print("切换到%s" % (os.getcwd()))
    PIL_Image_object.seek(0)
    frames = duration = 0

    imgiter = ImageSequence.Iterator(PIL_Image_object)  # GIF图片流的迭代器
    for frame in imgiter:  # 遍历图片流的每一帧
        try:
            frames += 1
            duration = PIL_Image_object.info['duration']  # 获取当前帧的持续时间
            eachFramesTime.append(duration)  # 将当前帧时间保存到列表
            # print("第%d帧时间%d ms"%(frames,duration))
            PIL_Image_object.seek(PIL_Image_object.tell() + 1)
            newframe = frame.convert("RGBA")
            newframe.save(os.getcwd() + '\\gifOutput' + "\\" + str(frames) + '.png')  # 保存当前帧
            duration = 0
        except EOFError:  # 当没有下一帧时会引发此错误
            pass
            # tkinter.messagebox.showwarning(title='OK',message='转换完成')


def remove_transparency(im, bg_colour=(255, 255, 255)):
    '''
    @function:删除PNG图片的透明度
    @parameter: im - Image object
                bg_colour -  BackgroundColor
    '''
    # 仅当图像具有透明度时进行处理
    # if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
    if True:
        # 需要转换为RGBA如果LA格式由于PIL的一个bug
        alpha = im.convert('RGBA').split()[-1]

        # 创建一个新的背景图像的马特色.
        # 必须是RGBA，因为粘贴要求两个图像有相同的格式
        bg = Image.new("RGBA", im.size, bg_colour + (255,))
        bg.paste(im, mask=alpha)
        return bg
    else:
        return im


def ma():
    '''
    转为BMP格式
    '''
    pass
    # print('转为bmp格式')
    # print(os.listdir(os.getcwd()))
    # for i in (os.listdir(os.getcwd())):
    #     if i.lower().split('.')[-1] == 'png' or i.lower().split('.')[-1] == 'jpg':  # 判断图片格式是否为 png 或 jpg
    #         imgName = i.lower().split('.')[0]  # 获取文件名
    #         # i = oldpath  + '\\'+i
    #         if i.lower().split('.')[-1] == 'jpg':
    #             img = Image.open(i)  # 打开图片
    #             img = remove_transparency(img)  # 透明度处理
    #             img.save(imgName + '.bmp', 'bmp')
    #
    #         if i.lower().split('.')[-1] == 'png':
    #             img = Image.open(i).convert("1")  # 打开图片
    #             img.save(imgName + '.bmp', 'bmp')
    #
    # for i in (os.listdir(os.getcwd())):
    #     if i.lower().split('.')[-1] == 'png' or i.lower().split('.')[-1] == 'jpg':  # 判断图片格式是否为 png 或 jpg
    #         os.remove(i)  # 删除 后缀为 jpg 或 png 的图片
    #
    # # tkinter.messagebox.showwarning(title='OK',message='转换完成')
    # print(" 转为BMP格式转换完成!")


def convert_to_rgb565(img):
    # 获取图像大小
    width, height = img.size
    img.convert()
    # 创建一个新图像，模式为RGB565
    rgb565_img = Image.new('RGB', (width, height))
    for x in range(width):
        for y in range(height):
            # 获取像素的RGB值
            r, g, b = img.getpixel((x, y))

            # 将RGB值转换为RGB565格式
            r565 = (r >> 3) & 0x1F
            g565 = (g >> 2) & 0x3F
            b565 = (b >> 3) & 0x1F

            # 计算新的RGB565值
            rgb565_value = (r565 << 11) | (g565 << 5) | b565
            # 在新图像中设置像素的RGB565值
            rgb565_img.putpixel((x, y), rgb565_value)
    return rgb565_img


def resizeImg():
    '''
    重置大小
    '''
    print("重置图片大小")
    os.chdir(os.getcwd() + "\\gifOutput")

    new_x = int(sizex_entry.get())
    new_y = int(sizey_entry.get())
    global new_size
    new_size = (new_x, new_y)
    # print(os.listdir(newpath))
    file = os.listdir(os.getcwd())  # 获取路径下的所有文件
    print(file)
    file.sort(key=lambda x: int(x[:-4]))  # 按照文件名 排序
    index1 = 0
    if variable.get() == 'oled':
        for each in file:
            index1 = index1 + 1
            image = Image.open(each).convert('1')
            new_image = image.resize(new_size)
            new_image.save(str(index1) + '.bmp', 'bmp')
            # os.remove(each)
    else:
        for each in file:
            index1 = index1 + 1
            image = Image.open(each).convert('RGB')
            # image = image.convert('RGB')
            # image = convert_to_rgb565(image)
            if new_x == 0:
                new_image = image.transpose(Image.ROTATE_90)
            else:
                new_image = image.transpose(Image.ROTATE_90).resize(new_size)

            new_image.save(str(index1) + '.bmp', 'bmp')
            # os.remove(each)
    for i in (os.listdir(os.getcwd())):
        if i.lower().split('.')[-1] == 'png' or i.lower().split('.')[-1] == 'jpg':  # 判断图片格式是否为 png 或 jpg
            os.remove(i)  # 删除 后缀为 jpg 或 png 的图片
    print("重置大小完成")


def bmp2hex(imgFile):
    '''
     图片取模
    '''
    outputList = []
    print(f"正在处理>>>>{imgFile}")
    img = Image.open(imgFile)
    (width, height) = img.size  # 获取图片的宽 高信息
    list1 = []
    list2 = []
    bin_list = []
    if variable.get() == 'oled':
        for w in range(height):
            for h in range(width):
                pixel = img.getpixel((h, w))  # 获取图片的像素点
                if True:  # 01反转
                    if pixel == 255:
                        pixel = 0
                    else:
                        pixel = 1
                    list1.append(pixel)  # 当前像素值添加到列表里
            list2.append(list1.copy())
            list1.clear()
        while len(list2[0]) % 8 != 0:  # 判断是否为8的倍数,不足补0
            for i in range(len(list2)):  # 循环每一行
                list2[i].append(0)  # 末尾补0
        lenth = len(list2[0]) // 8
    else:
        for w in range(height):
            for h in range(width):
                r, g, b = img.getpixel((h, w))
                r565 = (r >> 3) & 0x1F
                g565 = (g >> 2) & 0x3F
                b565 = (b >> 3) & 0x1F
                rgb565_value = (r565 << 11) | (g565 << 5) | b565
                bitsH = (rgb565_value >> 8) & 0xFF
                resH = '0x' + str(hex(bitsH))[2:].zfill(2).upper()
                bitsL = rgb565_value & 0xFF
                resL = '0x' + str(hex(bitsL))[2:].zfill(2).upper()
                bin_list.append(bitsH)
                bin_list.append(bitsL)
                list2.append(resH)
                list2.append(resL)

    if variable.get() == 'oled':
        j = 0
        k = 0
        num = 0
        for m in range(len(list2)):  # 行循环
            for i in range(lenth):  # 列循环
                j = j + 7
                l1 = list2[m][k:j + 1]  # 提取8位
                for q in range(len(l1)):
                    num = num | l1[q] << 7 - q  # 合并8位单独数字
                res = '0x' + str(hex(num))[2:].zfill(2).upper()  # 格式化为0x00样式
                outputList.append(res)
                num = 0
                k = j + 1
                j = j + 1
            j = 0
            k = 0
        print(f'{imgFile}处理完成')
        return outputList, bin_list
    else:
        return list2, bin_list
    # tkinter.messagebox.showwarning(title='ok',message='保存完成')


def bmp2hex_oled(imgFile):
    '''
     图片取模
    '''
    outputList = []
    print(f"正在处理>>>>{imgFile}")
    img = Image.open(imgFile)
    (width, height) = img.size  # 获取图片的宽 高信息
    list1 = []
    list2 = []
    bin_list = []
    for w in range(height):
        for h in range(width):
            pixel = img.getpixel((h, w))  # 获取图片的像素点
            if True:  # 01反转
                if pixel == 255:
                    pixel = 0
                else:
                    pixel = 1
                list1.append(pixel)  # 当前像素值添加到列表里
        list2.append(list1.copy())
        list1.clear()
    while len(list2[0]) % 8 != 0:  # 判断是否为8的倍数,不足补0
        for i in range(len(list2)):  # 循环每一行
            list2[i].append(0)  # 末尾补0
    lenth = len(list2[0]) // 8

    j = 0
    k = 0
    num = 0
    for m in range(len(list2)):  # 行循环
        for i in range(lenth):  # 列循环
            j = j + 7
            l1 = list2[m][k:j + 1]  # 提取8位
            for q in range(len(l1)):
                num = num | l1[q] << 7 - q  # 合并8位单独数字
            res = '0x' + str(hex(num))[2:].zfill(2).upper()  # 格式化为0x00样式
            outputList.append(res)
            num = 0
            k = j + 1
            j = j + 1
        j = 0
        k = 0
    print(f'{imgFile}处理完成')
    return outputList

    # tkinter.messagebox.showwarning(title='ok',message='保存完成')


def selectGifFile():
    global gif_file
    try:
        gif_file = askopenfilename(title="选择GIF图片", filetypes=[("GIF Image", '*.gif'), ('PNG Image', '*.png')])
        os.chdir(os.path.dirname(gif_file))
        print(gif_file)
    except OSError:
        tkinter.messagebox.showwarning(title='ok', message='请选择正确的gif或png文件')


def process_files_in_directory(result_dick, bin_dick, file):
    result, bin_list = bmp2hex(file)
    key = file
    result_dick.update({key: result})
    bin_dick.update({key: bin_list})
    print("dickID = ", id(result_dick))


def process_files_in_directory_oled(result_dick, file):
    result = bmp2hex_oled(file)
    key = file
    result_dick.update({key: result})
    print("dickID = ", id(result_dick))


def write_results_to_file(result_dick, bin_dick):
    filename = entry.get()
    outPutFile = filename + ".h"
    with open(outPutFile, 'a+') as f:
        if result_dick:
            # 获取排序后的结果
            file = os.listdir(os.getcwd())
            size = len(result_dick['1.bmp'])
            f.write(f"unsigned char {filename}[][{size}] = {{")
            filtered_files = [i for i in file if i != outPutFile]
            filtered_files.sort(key=lambda x: int(x[:-4]))  # 按照文件名 排序
            for i in filtered_files:
                # f.write(f"File: {i}\n")
                f.write("{")
                result = result_dick[i]
                counter = int(0)
                for j in result:
                    f.write(j)
                    counter = counter + 1
                    if counter != len(result):
                        f.write(', ')
                    if not counter % 16:
                        f.write('\n')

                f.write("},\n")
            f.write("};\n")
    if variable.get() == 'lcd':
        with open('boot.bin', 'wb') as boot:
            file = os.listdir(os.getcwd())
            filtered_files = [i for i in file if i != outPutFile and i != 'boot.bin']
            filtered_files.sort(key=lambda x: int(x[:-4]))  # 按照文件名 排序
            for i in filtered_files:
                bin_list = bin_dick[i]
                for j in bin_list:
                    binary_data = j.to_bytes(1, byteorder='big')
                    boot.write(binary_data)

    tkinter.messagebox.showwarning(title='ok', message='转换完成')


def beginSpilt():
    """
    开始转换
    """
    img = Image.open(gif_file)  # 打开选择的GIF
    saveFps(img)  # 提取并保存GIF的每一帧
    resizeImg()  # 重置图片大小并转换为bmp模式（改为48X48）
    # ma()  # 转为BMP格式

    file = os.listdir(os.getcwd())  # 获取路径下的所有文件
    file.sort(key=lambda x: int(x[:-4]))  # 按照文件名 排序
    print(os.listdir(os.getcwd()))
    print(file)

    # 创建一个公共字典
    manager = multiprocessing.Manager()
    result_dick = manager.dict()
    bin_dick = manager.dict()
    arg_list = []
    if variable.get() == 'oled':
        for i in file:
            l1 = (result_dick, i)
            arg_list.append(l1)
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
        pool.starmap(process_files_in_directory_oled, arg_list)  # 多线程处理每个bmp图像
        pool.close()
        pool.join()
    else:
        for i in file:
            l1 = (result_dick, bin_dick, i)
            arg_list.append(l1)
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
        pool.starmap(process_files_in_directory, arg_list)  # 多线程处理每个bmp图像
        pool.close()
        pool.join()

    write_results_to_file(result_dick, bin_dick)  # 将处理结束的字典输出到.h文件

    # bmp2hex()  # 图片取模，保存数组文件

    # generateArduinoCode(); #  生成 Arduino 代码


def splitGif():
    '''
    开始转换
    '''
    tkinter.messagebox.showwarning(title='开始', message='需要一小会儿时间...请稍后,点击确定开始')
    beginSpilt()
    # splitThread = threading.Thread(target=beginSpilt)
    # splitThread.setDaemon(True)
    # splitThread.start()


windows = Tk()
windows.title("OLED动图生成")
windows.geometry('300x300')
windows.resizable(0, 0)

text = "分割GIF,转BMP格式"
# text2 = "选择你使用的库文件"
L1 = Label(windows, text=text)
L1.pack()

L2 = Label(windows, text='选择生成方式', fg="red")
L2.pack()

variable = StringVar()
w = OptionMenu(windows, variable, "oled", "lcd")  # 创建以及下拉框，用于选择头文件
w.pack()

bb1 = Button(windows, text="选择GIF图片", command=selectGifFile)
bb1.pack()

sizex_text = '在下方输入生成图片x'
L4 = Label(windows, text=sizex_text, fg="red")
L4.pack()
sizex_entry = Entry(windows)
sizex_entry.pack()
sizex_entry.insert(1, "请输入x的大小")
sizey_text = '在下方输入生成图片y'
L5 = Label(windows, text=sizey_text, fg="red")
L5.pack()
sizey_entry = Entry(windows)
sizey_entry.pack()
sizey_entry.insert(1, "请输入y的大小")

text3 = "在下方输入框写入数组名，\n生成的数组文件也会为此名，\n注意命方式和C语言一致"
L3 = Label(windows, text=text3, fg="red")
L3.pack()

entry = Entry(windows)
entry.pack()
entry.insert(0, "数组名(必填)")

bb2 = Button(windows, text='生成二位数组', command=splitGif)
bb2.pack()

if __name__ == "__main__":
    multiprocessing.freeze_support()
    mainloop()
