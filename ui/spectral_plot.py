from PIL import ImageDraw, Image, ImageFont

def show_channel(fb, channel_number: int = 1):
    pass

def show_band(fb, rf_data):
    # Initialise image in framebuffer
    image = Image.new("RGBA", fb.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Draw grid
    # 15 lines, 20px =
    # RSSI from -96 to -26 = 70dBm
    # Every 10dBm -> 7 lines -> 240/7 = 30

    small_fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 10)
    hdg_fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 16)

    # Boundaries: (come out 20px each side)
    # Top left corner: (30, 20)
    # Top right corner: (310, 20)
    # Bottom left corner: (30, 220)
    # Bottom right corner: (310, 220)
    # Frequency: 2400 - 2540MHz
    # RF power: -20 to -120dBm

    minX = 30
    maxX = 310
    minY = 20
    maxY = 220

    shape = [(0, 0), (320, 240)]
    draw.rectangle(shape, fill="#000000", outline="black")

    shape = [(minX, minY), (maxX, maxY)]
    draw.rectangle(shape, fill="#101010", outline="white")

    for x in range(minX, maxX, 20):
        draw.line((x, minY, x, maxY), fill="green")
        if (x % 40 == 0):
            label = f"{int(2380 + (x/2))}"
            draw.text((x-25, maxY), label.rjust(6), font=small_fnt, fill="green")

    for y in range(minY, maxY, 20):
        draw.line((minX, y, maxX, y), fill="white")
        label = f"{int(-30 - (y-20)/2)}"
        draw.text((0, y+15), label.rjust(4), font=small_fnt, fill="green")

    draw.text((50, 0), "SPECTRAL ANALYSIS", font=hdg_fnt, fill="red")

    # Convert frequency to x pixel
    old_data = None
    for data_point in rf_data:
        frequency = data_point[0] / 1000
        rf_power = data_point[1]

        x = int(((frequency - 2400) * 2) + minX)
        y = int((-((rf_power + 20) * 2)) + minY)

        if old_data is None:
            old_data = (x, y)
        new_data = (x, y)

        draw.ellipse([(x-1, y-1), (x+1, y+1)], fill="yellow")
        draw.line([old_data, new_data], fill="yellow")

        old_data = new_data

    fb.show(image)