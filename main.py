import time
from framebuffer import framebuffer

def main():
    lcd_screen = framebuffer.FB_GFXInterface(320, 240)
    
    lcd_screen.init()
    lcd_screen.write_screen()
    
    for idx, circle_radius in enumerate(range(8, 128, 8)):
        lcd_screen.circle(160, 120, circle_radius, fg_shade=idx*2)

    for y in range(16, 240, 16):
        lcd_screen.horizontal_line(y=y, fg_shade=15)

    for x in range(16, 320, 16):
        lcd_screen.vertical_line(x=x, fg_shade=15)

    lcd_screen.write_screen()

main()
