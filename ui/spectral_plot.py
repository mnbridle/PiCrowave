from PIL import ImageDraw, Image, ImageFont

def show_channel(fb, channel_number: int = 1):
    pass

def show_band(fb, rf_data, location=(30, 20), size=(280, 200), gridlines=(1, 10)):
    # Initialise image in framebuffer
    image = Image.new("RGBA", fb.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Initialise fonts
    small_fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 10)
    hdg_fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 16)

    # Display window
    shape = [(0, 0), (320, 240)]
    draw.rectangle(shape, fill="#000000", outline="black")
    shape = [location, tuple([sum(tup) for tup in zip(location, size)])]
    draw.rectangle(shape, fill="#101010", outline="white")

    # Find min and max of each axes in the dataset
    freq_min, pwr_min = rf_data.min(axis=0)
    freq_max, pwr_max = rf_data.max(axis=0)

    freq_min /= 1000
    freq_max /= 1000

    # Freq will be on x, pwr on y
    # Work out scalings
    freq_span = (freq_max - freq_min)
    pwr_span = pwr_max - pwr_min

    # Next, work out MHz and dBm per pixel
    freq_per_px = freq_span / size[0]
    pwr_per_px = pwr_span / size[1]

    # Work out interval for gridlines
    grid_intervals = [
        (gridlines[0] / freq_span) * size[0],
        (gridlines[1] / pwr_span) * size[1]
    ]

    x = location[0]
    y = location[1]
    while x < location[0] + size[0]:
        draw.line((x, location[1], x, location[1] + size[1]), fill="green")
        x += int(grid_intervals[0])

    while y < location[1] + size[1]:
        draw.line((location[0], y, location[0] + size[0], y), fill="green")
        y += int(grid_intervals[1])

    old_data = None
    for data_point in rf_data:
        frequency = (data_point[0] / 1000)
        rf_power = data_point[1]

        x = int(((frequency - freq_min) / freq_per_px) + location[0])
        y = int((-(rf_power - pwr_min) / pwr_per_px) + location[1])

        if old_data is None:
            old_data = (x, y)
            
        new_data = (x, y)

        draw.ellipse([(x-1, y-1), (x+1, y+1)], fill="yellow")
        draw.line([old_data, new_data], fill="yellow")

        old_data = new_data
    
    fb.show(image)
