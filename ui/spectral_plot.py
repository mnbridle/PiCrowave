from PIL import ImageDraw, Image, ImageFont

def show_channel(fb, channel_number: int = 1):
    pass

def show_band(fb):
    # Initialise image in framebuffer
    image = Image.new("RGBA", fb.size, (128, 128, 128, 0))
    draw = ImageDraw.Draw(image)

    # Draw grid - every 5MHz
    # 17 lines, 320/17=18px
    # RSSI from -96 to -26 = 70dBm
    # Every 10dBm -> 7 lines -> 240/7 = 30

    small_fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 6)

    for x in range(20, 300, 16):
        draw.line((x, 15, x, 225), fill=(255, 255, 255, 0))
        draw.text((x, 0), f"{2400 + x}", font=small_fnt, fill=(0, 255, 0, 0))

    for y in range(15, 225, 30):
        draw.line((0, y, 300, y), fill=(255, 255, 255, 0))
        draw.text((0, y), f"{-30 - y}", font=small_fnt, fill=(0, 255, 0, 0))

    # get a font
    fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 12)

    # draw multiline text
    draw.multiline_text((10, 10), "Hello\nWorld", font=fnt, fill=(0, 255, 0, 0))
    fb.show(image)