from framebuffer.framebuffer import Framebuffer
from framebuffer import constants

import time
from PIL import ImageDraw, Image, ImageFont
import matplotlib.pyplot as plt
import random
import io


def TestFrameBuffer():
    fb = Framebuffer(constants.framebuffer_number)

    # Initialise image in framebuffer
    image = Image.new("RGBA", fb.size)
    draw = ImageDraw.Draw(image)
    draw.rectangle(((0, 0), fb.size), fill="red")
    draw.ellipse(((0, 0), fb.size), fill="blue", outline="red")

    # get a font
    fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 12)

    # draw multiline text
    draw.multiline_text((10, 10), "Hello\nWorld", font=fnt, fill=(0, 0, 0))

    fb.show(image)

    # Plot something using matplotlib

    # # channel RSSI
    # randomlist = []
    # for i in range(0,13):
    #     n = random.randint(-90,-20)
    #     randomlist.append(n)

    # print(randomlist)

    # plt.rcParams["figure.figsize"] = [7.50, 3.50]
    # plt.rcParams["figure.autolayout"] = True

    # fig = plt.figure(figsize=(320/72, 240/72), dpi=72)
    # ax = fig.add_axes([0, 0, 1, 1])
    # channels = [chan for chan in range(1, 14)]

    # ax.plot(channels, randomlist)

    # img_buf = io.BytesIO()
    # plt.savefig(img_buf, format='png')

    # im = Image.open(img_buf)
    # fb.show(im)

    # img_buf.close()


def main():
    TestFrameBuffer()

main()