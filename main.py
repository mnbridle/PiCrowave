from framebuffer.framebuffer import Framebuffer
from framebuffer import constants

import ui.spectral_plot


def main():
    fb = Framebuffer(constants.framebuffer_number)
    ui.spectral_plot.show_band(fb)

    TestFrameBuffer()

main()