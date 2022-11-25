from PIL import ImageDraw, Image, ImageFont

import copy


def initialise_image(image, channel, location=(30, 20), size=(280, 200), freq_scale=(2400, 2483), pwr_scale=(-150, -30), gridlines=(10, 10)):
    # Initialise image in framebuffer
    draw = ImageDraw.Draw(image)

    # Initialise fonts
    small_fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 10)
    hdg_fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 16)

    # Display window
    shape = [(0, 0), (320, 240)]
    draw.rectangle(shape, fill="#000000", outline="black")
    shape = [location, tuple([sum(tup) for tup in zip(location, size)])]
    draw.rectangle(shape, fill="#101010", outline="white")

    # Draw gridlines
    pwr_min, pwr_max = pwr_scale
    freq_min, freq_max = freq_scale

    # Freq will be on x, pwr on y
    # Work out scalings
    freq_span = (freq_max - freq_min)
    pwr_span = abs(pwr_max - pwr_min)

    # Work out interval for gridlines
    grid_intervals = [
        (gridlines[0] / freq_span) * size[0],
        (gridlines[1] / pwr_span) * size[1]
    ]

    x = location[0]
    y = location[1]
    
    freq = freq_min
    while x < location[0] + size[0]:
        draw.line((x, location[1], x, location[1] + size[1]), fill="green")
        if (freq - freq_min) % 5 == 0:
            draw.text((x, 220), f"{freq}", font=small_fnt, fill="yellow")
        freq += gridlines[0]
        x += int(grid_intervals[0])

    dbm = pwr_max        
    while y < location[1] + size[1]:
        draw.line((location[0], y, location[0] + size[0], y), fill="green")
        if dbm % 20 == 0:
            draw.text((0, y-4), f"{dbm}", font=small_fnt, fill="yellow")
        dbm -= gridlines[1]
        y += int(grid_intervals[1])

    draw.text((0, 0), f"Spectrum analysis - channel {channel}", font=hdg_fnt, fill="yellow")

    return image

def show_band(image, rf_data, location=(30, 20), size=(280, 200), freq_scale=(2400, 2483), pwr_scale=(-150, -30), gridlines=(10, 10)):
    draw = ImageDraw.Draw(image)

    # Draw gridlines
    pwr_min, pwr_max = pwr_scale
    freq_min, freq_max = freq_scale

    # Freq will be on x, pwr on y
    # Work out scalings
    freq_span = (freq_max - freq_min)
    pwr_span = abs(pwr_max - pwr_min)

    # Next, work out MHz and dBm per pixel
    freq_per_px = freq_span / size[0]
    pwr_per_px = pwr_span / size[1]

    # Reorder RF data
    rf_data = rf_data[rf_data[:, 0].argsort()]

    old_data = None
    for data_point in rf_data:
        frequency, rf_power = data_point

        x = int(((frequency - freq_min) / freq_per_px) + location[0])
        y = int((abs(pwr_min - rf_power) / pwr_per_px) + location[1])

        if old_data is None:
            old_data = (x, y)

        new_data = (x, y)
        draw.line([old_data, new_data], fill="yellow")
        old_data = new_data
    
    return image
