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
    # Top left corner: (20, 20)
    # Top right corner: (300, 20)
    # Bottom left corner: (20, 220)
    # Bottom right corner: (300, 220)
    # Frequency: 2400 - 2540MHz
    # RF power: -20 to -120dBm

    shape = [(0, 0), (320, 240)]
    draw.rectangle(shape, fill="#000000", outline="black")

    shape = [(40, 20), (319, 220)]
    draw.rectangle(shape, fill="#101010", outline="white")

    for x in range(40, 320, 20):
        draw.line((x, 20, x, 220), fill="green")
        if (x % 40 == 0):
            label = f"{int(2380 + (x/2))}"
            draw.text((x-25, 220), label.rjust(6), font=small_fnt, fill="green")

    for y in range(20, 220, 20):
        draw.line((40, y, 320, y), fill="white")
        label = f"{-30 - (y-20)/2}"
        draw.text((0, y+15), label.rjust(6), font=small_fnt, fill="green")

    draw.text((50, 0), "SPECTRAL ANALYSIS", font=hdg_fnt, fill="red")

    # Convert frequency to x pixel
    rf_power = -60
    for frequency in range(2400, 2540, 5):
        x = int(((frequency - 2400) * 2) + 40)
        y = int((-((rf_power + 20) * 2)) + 20)
        draw.text((x, y), "X", font=small_fnt, fill="yellow")

    fb.show(image)