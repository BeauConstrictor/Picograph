import pygame
import sys

from font import font

NORMALSCRIPT = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹",
                             "0123456789")

EASY_KEYS = str.maketrans("0123456789XY+-=*/\r\b",
                          "0123456789ABCD#AB#*")

COLS = {
    "red":   (255, 0, 0),
    "green": (0, 255, 0),
    "blue":  (0, 0, 255),
}

class SoftwareDisplay:
    def __init__(self, width: int, height: int, scale: int) -> None:
        self.width = width
        self.height = height
        self.scale = scale
        self.font = font

        pygame.init()
        self.screen = pygame.display.set_mode((width * scale, height * scale))
        self.surface = pygame.Surface((width, height))

        self.clock = pygame.time.Clock()
        self.pixel_changes = []

        self.surface.fill((0, 0, 0))

    def set_pixel(self, x: int, y: int, val: bool|str) -> None:
        self.pixel_changes.append((x, y, val))

    def clear(self) -> None:
        # this way, changes after the clear are not lost
        # as they would be if a flag was used
        self.pixel_changes.clear()
        self.pixel_changes.append((-1, -1, -1))

    def write(self, x: int, y: int, text: str,
              char_spacing: int=1, line_height: int=7,
              space_width: int=3) -> None:
        cur_x = 0
        cur_y = 0

        for i, ch in enumerate(text):
            if ch == " ":
                cur_x += space_width
                continue
            if ch == "\n":
                cur_x = 0
                cur_y += line_height
                continue

            y_offset = 0
            if ch in "⁰¹²³⁴⁵⁶⁷⁸⁹":
                ch = ch.translate(NORMALSCRIPT)
                y_offset = -1

            pixels = self.font.get(ch, self.font["?"])
            for yo, row in enumerate(pixels):
                for xo, on in enumerate(row):
                    self.set_pixel(cur_x+x+xo, cur_y+y+yo+y_offset, on)
            char_width = len(pixels[0])
            cur_x += char_width+char_spacing

    def refresh(self) -> None:
        for x, y, color in self.pixel_changes:

            if (x, y, color) == (-1, -1, -1):
                self.surface.fill((0, 0, 0))
                continue

            if isinstance(color, str):
                color = COLS.get(color, (255, 255, 255))
            else:
                color = (255, 255, 255) if color else (0, 0, 0)
                
            if 0 <= x < self.width and 0 <= y < self.height:
                self.surface.set_at((x, y), color)

        self.pixel_changes.clear()

    def mainloop(self, keypress: callable[[str, "Display"]|None, None]) -> None:
        held = set()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYUP:
                    key = event.unicode.upper()
                    key = key.translate(EASY_KEYS)
                    if event.key == pygame.K_UP:   key = "C"
                    if event.key == pygame.K_DOWN: key = "D"
                    
                    if key == ".":
                        keypress("C", self)
                        keypress("C", self)
                    if event.key == pygame.K_ESCAPE:
                        keypress("D", self)
                        keypress("D", self)

                    if key not in "1234567890ABCD#*": continue
                    keypress(key, self)

            for key in held:
                keypress(key, self)

            self.refresh()

            scaled = pygame.transform.scale(
                self.surface,
                (self.width * self.scale, self.height * self.scale)
            )
            self.screen.blit(scaled, (0, 0))

            pygame.display.flip()
            self.clock.tick(60)