# By Michael Grazebrook
#
# Re-write of the 6 March London Python dojo using ctypes
#
# ctypes is a library used to map C data types, so it can represent
# a value as a "union", which means you can interpret the same data
# in different ways.
import sys
import pygame
import struct
import ctypes
import dis


####################################################
#           Managing 32 bits of data
####################################################


class Char(ctypes.Structure):
    """
    Interpret 8 bits of memory as an ASCII character

    Equivalent to C language:
    struct Char {
        char c;
    };
    """
    _fields_ = [("c", ctypes.c_char)]
    def __str__(self):
        return self.c


class Int16(ctypes.Structure):
    """
    Interpret 2 bytes as a 16 bit integer

    Equivalent to C (though it depends on processor architecture):
    struct Int16 {
        short i;
    };
    """
    _fields_ = [
        ("i", ctypes.c_int16)
    ]


class Data32(ctypes.Union):
    """
    Various views on the same 32 bits of memory
    """
    _fields_ = [
        ("i", ctypes.c_int32), # Integer
        ("u", ctypes.c_uint32), # Unsigned integer
        ("f", ctypes.c_float), # 32 bit floating point number
        ("s", Int16 * 2), # A pair of 16 bit numbers fit in the same space
        ("c", Char * 4), # Or 4 characters
    ]

    def rgb(self):
        """
        Convert 32 bits into a pixel.

        In practice, images are often stored compressed but usually converted
        to pixels when a program reads them.

        Pygame uses 24 bits for pixels, so we ignore the top 8 bits as padding.
        """
        red   = (0x0000ff & self.i) # Mask only the bottom bits
        green = (0x00ff00 & self.i) >> 8 # Shift right 8 bits, like dividing by 256
        blue  = (0xff0000 & self.i) >> 16
        # Ignore the highest bits

        return (red, green, blue)




####################################################
#        Pygame stuff
####################################################


WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)


class CheckBox(object):
    def __init__(self, screen, rect):
        self.screen = screen
        self.rect = rect
        self.checked = False


    def __contains__(self, point):
        return self.rect.collidepoint(point)

    def draw(self):
        width = 0 if self.checked else 1
        pygame.draw.rect(self.screen, YELLOW, self.rect, width)


def get_string(boxes):
     return ''.join(str(int(b.checked)) for b in boxes)


class BitViews:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 600))
        self.FONT = pygame.font.SysFont('Consolas', 24)

        self.boxes = []
        w = 20
        for i in range(32):
            r = pygame.Rect(10 + 1.5 * w * i, 10, w, w)
            self.boxes.append(CheckBox(self.screen, r))


    def draw_string(self, text, pos, colour = WHITE):
        try:
            self.screen.blit(self.FONT.render(text, True, colour), pos)
        except pygame.error:
            pass


    def draw(self):
        self.screen.fill((0, 0, 0))
        for b in self.boxes:
            b.draw()

        string = get_string(self.boxes)

        data = Data32()
        data.i = int(string, 2)
        self.draw_views(data)

    def draw_views(self, data):
        # Student question: Why do the first 3 but not unsigned use data.i?
        self.draw_string("Binary           : " + "{0:b}".format(data.i), (10, 50))
        self.draw_string("Hexadecimal      : " + "{0:X}".format(data.i), (10, 80))
        self.draw_string("32 bit Integer   : " + "{0:d}".format(data.i), (10, 110))
        self.draw_string("Unsigned integer : " + str(data.u), (10, 170))

        # Less accuracy, but more of them.
        self.draw_string("16 bit integers  : " + repr([data.s[1].i, data.s[0].i]), (10, 140))

        # Follows the "IEEE 754" standard - tricky! Can you work out how to display -10.0?
        self.draw_string("Floating point   : " + str(data.f), (10, 200))

        chars = [item.c for item in reversed(data.c)]
        self.draw_string("Character array  : " + repr(chars), (10, 230))

        # If a character has value zero i.e. '\x00', the rest of the text is lost.
        # In many programming languages, you keep printing text until you find a zero.
        self.draw_string("Text             : " + ''.join(chars), (10, 260))

        self.draw_string("red/green/blue   : " + repr(data.rgb()), (10, 290))
        self.draw_string("Colour           : ", (10, 320))
        try:
            pygame.draw.rect(self.screen, data.rgb(), (250,320,20,20))
        except:
            pass

        code = [ dis.opname[ord(c.c)] for c in reversed(data.c)]
        self.draw_string("Python byte code : " + repr(code), (10, 350))

        pygame.display.flip()


    def run(self):
        while True:

            self.draw()
            event = pygame.event.wait()
            if event.type == pygame.QUIT: 
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for b in self.boxes:
                    if event.pos in b:
                        b.checked = not b.checked


if __name__ == "__main__":
    app = BitViews()
    app.run()
    
