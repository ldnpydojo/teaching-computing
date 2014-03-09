# By Dan, Michael Grazebrook and Andrea Grandi
# London Python dojo 6th March
import sys
import pygame
import struct


            
asm = ['CMPSB',
'AAA',
'CMPSW',
'AAD',
'CWD',
'AAM',
'DAA',
'AAS',
'DAS',
'ADC',
'DEC',
'ADD',
'DIV',
'AND',
'HLT',
'CALL',
'IDIV',
'CBW',
'IMUL',
'CLC',
'IN',
'CLD',
'INC',
'CLI',
'INT',
'CMC',
'INTO',
'CMP',
'IRET',
'JA',
'JAE',
'JB',
'JBE',
'JC',
'JCXZ',
'JE',
'JG',
'JGE',
'JL',
'JLE',
'JMP',
'JNA',
'JNAE',
'JNB',
'JNBE',
'JNC',
'JNE',
'JNG',
'JNGE',
'JNL',
'JNLE',
'JNO',
'JNP',
'JNS',
'JNZ',
'JO',
'JP',
'JPE',
'JPO',
'JS',
'JZ',
'LAHF',
'LDS',
'LEA',
'LES',
'LODSB',
'LODSW',
'LOOP',
'LOOPE',
'LOOPNE',
'LOOPNZ',
'LOOPZ',
'MOV',
'MOVSB',
'RCR',
'SCASB',
'MOVSW',
'REP',
'SCASW',
'MUL',
'REPE',
'SHL',
]


pygame.init()

screen = pygame.display.set_mode((800, 500))

FONT = pygame.font.SysFont('Consolas', 24)

WHITE = (255, 255, 255)

YELLOW = (255, 255, 0)


class CheckBox(object):
    def __init__(self, rect):
        self.rect = rect
        self.checked = False


    def __contains__(self, point):
        return self.rect.collidepoint(point)
        
    def draw(self):
        width = 0 if self.checked else 1
        pygame.draw.rect(screen, YELLOW, self.rect, width)


def get_string():
     return ''.join(str(int(b.checked)) for b in boxes)


def get_int():
    return int(get_string(), 2)


boxes = []

def create_boxes():
    w = 10
    for i in range(32):
        r = pygame.Rect(10 + 20 * i, 10, w, w)
        boxes.append(CheckBox(r))

def draw_string(text, pos, colour = WHITE):
    try:
        screen.blit(FONT.render(text, True, colour), pos)
    except pygame.error:
        pass
    

def draw():
    screen.fill((0, 0, 0))
    for b in boxes:
    	b.draw()

    string = get_string()
    integer = get_int()
    bytes = struct.pack('>I', integer)
    
    draw_string("Binary:         " + string, (10, 50))
    draw_string("Integer:        " + str(integer), (10, 80))
    draw_string("Bytes:          " + bytes, (10,110))
    draw_string("Byte string:    " + repr(struct.pack('>I', integer)), (10,140))
    draw_string("Floating point: " + str(struct.unpack('>f', bytes)[0]), (10, 170))
    draw_string("Hexadecimal:    " + bytes.encode('hex'), (10, 200))

    if integer < len(asm):
        draw_string("Assembler:      " + asm[integer], (10, 290))
    else:
        draw_string("Assembler:       ERR", (10, 290))

    draw_string("Colour:         ", (10, 230) )
    red   = (0x0000ff & integer)
    green = (0x00ff00 & integer) >> 8
    blue  = (0xff0000 & integer) >> 16
    
    r = pygame.Rect(220, 230, 20,20)
    try:
        pygame.draw.rect(screen, (red,green,blue), r, 30)
    except:
        pass

    pygame.display.flip()


create_boxes()
while True:
    draw()
    event = pygame.event.wait()
    if event.type == pygame.QUIT: 
        sys.exit()
    if event.type == pygame.MOUSEBUTTONDOWN:
        for b in boxes:
            if event.pos in b:
                b.checked = not b.checked
