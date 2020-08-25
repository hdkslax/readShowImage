import tkinter
from tkinter import *
from tkinter import filedialog
import os
import array


# read a bmp file
def read_bmp():
    root = tkinter.Tk()
    root.withdraw()  # not show the tk dialog box
    bmp_path = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title="Please select a bmp file: ")
    if bmp_path == '':
        exit()

    print("文件名为：", bmp_path)
    return bmp_path


def bmp_to_binary(bmp_path):
    bmp_file = open(bmp_path, 'rb')
    bmp = bmp_file.read()
    print(len(bmp))
    print(bmp)
    bmp_header = array.array('i', (0 for _ in range(14)))
    dib_header = array.array('i', (0 for _ in range(40)))

    data = array.array('i', (0 for _ in range(len(bmp) - 54)))

    for i in range(14):
        bmp_header[i] = bmp[i]
    for i in range(40):
        dib_header[i] = bmp[i + 14]
    for i in range(len(bmp) - 54):
        data[i] = bmp[i + 54]
    print("bmp_header = ", bmp_header)
    print("dib_header = ", dib_header)


    biwidth = dib_header[7] * 16 * 16 * 16 * 16 * 16 * 16 + dib_header[6] * 16 * 16 * 16 * 16 + dib_header[
        5] * 16 * 16 + dib_header[4]
    print("biwidth = ", biwidth)
    pixel_per_row = 4 * int(((dib_header[14] * biwidth) + 31) / 32)
    print(pixel_per_row)
    biheight = dib_header[11] * 16 * 16 * 16 * 16 * 16 * 16 + dib_header[10] * 16 * 16 * 16 * 16 + dib_header[
        9] * 16 * 16 + dib_header[8]
    print("biheight = ", biheight)

    num_dummy_bytes = pixel_per_row % 3
    print("dummy = ", num_dummy_bytes)

    # if num_dummy_byte = 0 and biwidth is odd, the image will cut the last byte of each line to the next line,
    # to aviod this, biwidth should plus 1
    if num_dummy_bytes == 0 and biwidth % 2 == 1:
        biwidth += 1

    pixel_array_size = biwidth * biheight
    pixel = [[0 for i in range(3)] for j in range(pixel_array_size)]
    cum_dummy_bytes = 0
    for i in range(pixel_array_size):
        red_code = data[3 * i + 2 + cum_dummy_bytes]

        green_code = data[3 * i + 1 + cum_dummy_bytes]

        blue_code = data[3 * i + 0 + cum_dummy_bytes]

        pixel[i][0] = red_code
        pixel[i][1] = green_code
        pixel[i][2] = blue_code

        if i != 0 and i % biwidth == 0:
            for j in range(num_dummy_bytes):
                cum_dummy_bytes += 1

    temp = [[0 for i in range(3)] for j in range(pixel_array_size)]
    for i in range(biheight):
        for j in range(biwidth):
            temp[j + i * biwidth][0] = pixel[j + (biheight - 1 - i) * biwidth][0]
            temp[j + i * biwidth][1] = pixel[j + (biheight - 1 - i) * biwidth][1]
            temp[j + i * biwidth][2] = pixel[j + (biheight - 1 - i) * biwidth][2]


    return temp, biwidth, biheight


def RGB_to_YUV(RGB=[]):
    R = RGB[0]
    G = RGB[1]
    B = RGB[2]

    # print(R, G, B)
    # calculate corresponding YUV
    Y1 = round(0.299 * R + 0.587 * G + 0.114 * B)
    # U = round((-0.299) * R + (-0.587) * G + (0.886) * B)
    # V = round((0.701) * R + (-0.587) * G + (-0.114) * B)
    U = Y1
    V = Y1
    YUV = [Y1, U, V]

    return YUV


def color_to_grayscale(pixel):
    pixel_grayscale = [[0 for i in range(3)] for j in range(len(pixel))]
    for i in range(len(pixel)):
        pixel_grayscale[i] = RGB_to_YUV(pixel[i])

    return pixel_grayscale


def darken_bmp(pixel):
    darker_pixel = [[0 for i in range(3)] for j in range(len(pixel))]
    for i in range(len(pixel)):
        darker_pixel[i][0] = int(0.5 * pixel[i][0])
        darker_pixel[i][1] = int(0.5 * pixel[i][1])
        darker_pixel[i][2] = int(0.5 * pixel[i][2])
    return darker_pixel

def lighten_bmp(pixel):
    lighter_bmp = [[0 for i in range(3)] for j in range(len(pixel))]
    for i in range(len(pixel)):
        for j in range(3):
            lighter_bmp[i][j] = int(1.2 * pixel[i][j])
            if lighter_bmp[i][j] > 255:
                lighter_bmp[i][j] = 255
    return lighter_bmp


def higher_color_saturation(pixel):
    higher_saturation_pixel = [[0 for i in range(3)] for j in range(len(pixel))]
    for i in range(len(pixel)):
        if pixel[i][0] == max(pixel[i]):
            higher_saturation_pixel[i][0] = pixel[i][0] + 20
            if higher_saturation_pixel[i][0] > 255:
                higher_saturation_pixel[i][0] = 255
            higher_saturation_pixel[i][1] = pixel[i][1]
            higher_saturation_pixel[i][2] = pixel[i][2]
        elif pixel[i][1] == max(pixel[i]):
            higher_saturation_pixel[i][1] = pixel[i][1] + 20
            if higher_saturation_pixel[i][1] > 255:
                higher_saturation_pixel[i][1] = 255
            higher_saturation_pixel[i][0] = pixel[i][0]
            higher_saturation_pixel[i][2] = pixel[i][2]
        else:
            higher_saturation_pixel[i][2] = pixel[i][2] + 20
            if higher_saturation_pixel[i][2] > 255:
                higher_saturation_pixel[i][2] = 255
            higher_saturation_pixel[i][0] = pixel[i][0]
            higher_saturation_pixel[i][1] = pixel[i][1]

        if pixel[i][0] == min(pixel[i]):
            higher_saturation_pixel[i][0] = pixel[i][0] - 20
            if higher_saturation_pixel[i][0] < 0:
                higher_saturation_pixel[i][0] = 0
            higher_saturation_pixel[i][1] = pixel[i][1]
            higher_saturation_pixel[i][2] = pixel[i][2]
        elif pixel[i][1] == min(pixel[i]):
            higher_saturation_pixel[i][1] = pixel[i][1] - 20
            if higher_saturation_pixel[i][1] < 0:
                higher_saturation_pixel[i][1] = 0
            higher_saturation_pixel[i][0] = pixel[i][0]
            higher_saturation_pixel[i][2] = pixel[i][2]
        else:
            higher_saturation_pixel[i][2] = pixel[i][2] - 20
            if higher_saturation_pixel[i][2] < 0:
                higher_saturation_pixel[i][2] = 0
            higher_saturation_pixel[i][0] = pixel[i][0]
            higher_saturation_pixel[i][1] = pixel[i][1]

    return higher_saturation_pixel





def draw_bmp(pixel, bmp_path, biwidth, biheight):
    tk = Tk()
    tk.geometry('1000x900')
    title = bmp_path.split('/')
    title = title[-1]
    tk.title(title)
    tk.config(bg='lightgray')

    # a canvas to show the bmp image
    canvas = Canvas(tk, width=900, height=500)
    canvas.place(x=50, y=20)

    img = PhotoImage(master=canvas, width=biwidth, height=biheight)
    canvas.create_image((450, 250), image=img, state="normal")

    def rgb_to_hex(rgb):
        return '#%02x%02x%02x' % rgb

    def show_original_image():
        canvas.delete()
        canvas.create_image((450, 250), image=img, state="normal")
        for i in range(biheight):
            for j in range(biwidth):
                pixel_color = tuple(pixel[j + i * biwidth])
                pixel_color = rgb_to_hex(pixel_color)
                img.put(pixel_color, (j, i))

    show_original_image()

    # a frame to contain buttons
    btn_frame = Frame(tk)
    btn_frame.config(bg='lightgray', height=200, width=900)
    btn_frame.place(x=50, y=650)

    show_original_btn = Button(btn_frame,
                               borderwidth=3,
                               background='lightblue',
                               overrelief='sunken',
                               text='show original image',
                               command=show_original_image)
    show_original_btn.place(x=0, y=0)

    # a button refreshing the original image by the grayscale image
    def grayscale_refresh():
        canvas.delete()
        canvas.create_image((450, 250), image=img, state="normal")
        pixel_grey = color_to_grayscale(pixel)
        for i in range(biheight):
            for j in range(biwidth):
                gray_image_pixel = tuple(pixel_grey[j + i * biwidth])
                gray_image_pixel = rgb_to_hex(gray_image_pixel)
                img.put(gray_image_pixel, (j, i))

    grayscale_refresh_btn = Button(btn_frame,
                                   borderwidth=3,
                                   background='lightblue',
                                   overrelief='sunken',
                                   text='show grayscale image',
                                   command=grayscale_refresh)
    grayscale_refresh_btn.place(x=250, y=0)

    # a button refreshing the original image 50% darker
    def darker_refresh():
        canvas.delete()
        canvas.create_image((450, 250), image=img, state="normal")
        pixel_darker = darken_bmp(pixel)
        for i in range(biheight):
            for j in range(biwidth):
                darker_image_pixel = tuple(pixel_darker[j + i * biwidth])
                darker_image_pixel = rgb_to_hex(darker_image_pixel)
                img.put(darker_image_pixel, (j, i))

    darker_refresh_btn = Button(btn_frame,
                                borderwidth=3,
                                background='lightblue',
                                overrelief='sunken',
                                text='show 50% darker image',
                                command=darker_refresh)
    darker_refresh_btn.place(x=500, y=0)

    # a button refreshing the original image more vivid
    def vivid_refresh():
        canvas.delete()
        canvas.create_image((450, 250), image=img, state="normal")
        pixel_vivid = higher_color_saturation(pixel)
        pixel_vivid = lighten_bmp(pixel_vivid)
        for i in range(biheight):
            for j in range(biwidth):
                vivid_image_pixel = tuple(pixel_vivid[j + i * biwidth])
                vivid_image_pixel = rgb_to_hex(vivid_image_pixel)
                img.put(vivid_image_pixel, (j, i))

    vivid_refresh_btn = Button(btn_frame,
                               borderwidth=3,
                               background='lightblue',
                               overrelief='sunken',
                               text='show more vivid image',
                               command=vivid_refresh)
    vivid_refresh_btn.place(x=750, y=0)

    # an open button to open another bmp file
    def open_another_file():
        tk.destroy()
        main()

    open_btn = Button(btn_frame,
                      borderwidth=3,
                      background='lightpink',
                      overrelief='sunken',
                      text='open another file',
                      command=open_another_file)
    open_btn.place(x=200, y=90)

    # a close button to close the graph GUI
    close_btn = Button(btn_frame,
                       borderwidth=3,
                       width=16,
                       background='lightpink',
                       text='close',
                       overrelief='sunken',
                       command=tk.destroy)
    close_btn.place(x=400, y=90, anchor='nw')

    # a button to exit the program
    exit_btn = Button(btn_frame,
                      borderwidth=3,
                      width=16,
                      background='lightpink',
                      overrelief='sunken',
                      text='exit',
                      command=exit)
    exit_btn.place(x=600, y=90, anchor='nw')
    tk.mainloop()


def main():
    bmp_path = read_bmp()
    pixel, biwidth, biheight = bmp_to_binary(bmp_path)
    draw_bmp(pixel, bmp_path, biwidth, biheight)


if __name__ == '__main__':
    main()
