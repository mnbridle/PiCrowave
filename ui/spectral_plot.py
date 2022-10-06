from PIL import ImageDraw, Image, ImageFont

def show_channel(fb, channel_number: int = 1):
    pass

def show_band(fb):
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