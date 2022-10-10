from PIL import ImageDraw, Image, ImageFont

def show_channel(fb, channel_number: int = 1):
    pass

def show_band(fb):
    # Initialise image in framebuffer
    image = Image.new("RGBA", fb.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Draw grid
    # 15 lines, 20px = 
    # RSSI from -96 to -26 = 70dBm
    # Every 10dBm -> 7 lines -> 240/7 = 30

    small_fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 10)

    # Boundaries: (come out 20px each side)
    # Top left corner: (20, 20)
    # Top right corner: (300, 20)
    # Bottom left corner: (20, 220)
    # Bottom right corner: (300, 220)

    shape = [(0, 0), (320, 240)]
    draw.rectangle(shape, fill="#000000", outline="black")

    shape = [(20, 20), (300, 220)]
    draw.rectangle(shape, fill="#101010", outline="white")

    for x in range(40, 320, 20):
        draw.line((x, 20, x, 220), fill="green")
        draw.text((x, 220), f"{2380 + (x/2)}", font=small_fnt, fill="green")

    for y in range(20, 220, 20):
        draw.line((40, y, 320, y), fill="white")
        draw.text((0, y), f"{-30 - (y-20)/2}", font=small_fnt, fill="green")

    fb.show(image)