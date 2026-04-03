import sys
import json
from math import pi
emulated = sys.implementation.name == "cpython"

if emulated:
    from software_display import SoftwareDisplay
else:
    from hardware_display import HardwareDisplay
    from keypad import Keypad
    from machine import Pin
from cas import Polynomial, ExprSyntaxError, MissingVariableValueError
from utils import *

# some of these are taylor expansions so i don't need to add individual support
# for these functions, just make sure not to zoom out too far :D
with open("catalogue.json", "r") as f:
    catalogue = json.load(f)

def graph(polynomial: cas.Polynomial, graph_range: float, display: "Display") -> None:
    display_size = 128
    x_offset = 16
    y_offset = 0
    refresh_interval = 15
    
    display.clear()
    
    mid = display_size // 2
    for i in range(display_size):
        display.set_pixel(mid + x_offset, i + y_offset, True)
        display.set_pixel(i + x_offset, mid + y_offset, True)
    display.refresh()

    x_coords = [graph_range * (2 * j / display_size - 1) for j in range(display_size)]
    prev_row_vals = [0] * display_size

    led = None if emulated else Pin("LED", Pin.OUT)

    for i in range(display_size):
        y = graph_range * (1 - 2 * i / display_size)
        current_row_vals = [polynomial.substitute(x=x, y=y) for x in x_coords]

        if not emulated: led.toggle()

        for j in range(display_size):
            current_sign = sign(current_row_vals[j])
            sign_change = False

            # since we have such a low resolution, it is a bad idea to check
            # if the point at the centre of a pixel is 0. instead, we check
            # if the sign has changed across pixels, which would mean that 0
            # is somewhere within one of the pixels. after all, pixels are
            # squares, not points.
            if j > 0 and current_sign != sign(current_row_vals[j - 1]):
                sign_change = True
            if j < display_size - 1 and current_sign != sign(current_row_vals[j + 1]):
                sign_change = True

            if i > 0 and current_sign != sign(prev_row_vals[j]):
                sign_change = True

            if sign_change:
                display.set_pixel(j + x_offset, i + y_offset, "red")
        if i % refresh_interval == 0: display.refresh()

        prev_row_vals = current_row_vals
        
    if not emulated: led.on()
    display.write(1, 2, str(polynomial) + "=0")

class Calculator:
    def __init__(self, display: "Display") -> None:
        self.expr = ""
        self.display = display

        self.zoom = 1.2
        self.mode = "typing" # or "graphing", "catalogue" or "calculate"
        self.catalogue_selection = 0

        self.pretty_print_expr()
        self.display.refresh()

        if not emulated:
            Pin("LED", Pin.OUT).on()

    def run(self) -> None:
        self.display.mainloop(lambda key, _: self.keypress(key))

    def graph(self) -> None:
        if self.expr == "": return
        polynomial = Polynomial(self.expr)
        graph(polynomial, self.zoom, self.display)

    def pretty_print_expr(self) -> None:
        if self.expr == "":
            self.display.write(1, 2, "_")
            return
        polynomial = Polynomial(self.expr)
        self.display.write(1, 2, str(polynomial) + "_")

    def type_key(self, key: str, a: str, b: str) -> None:
        expr_ends_in_dash = len(self.expr) > 0 and self.expr[-1] == "-"

        if key == "*":
            self.expr = self.expr[:-1]
        elif key.isdigit():
            self.expr += key
        elif key == "A":
            self.expr += a
        elif key == "B":
            self.expr += b
        elif key == "C" and len(self.expr) > 0 and self.expr[-1] == "+":
            self.expr = self.expr[:-1] + "."
        elif key == "C":
            self.expr += "+"
        elif key == "D" and not expr_ends_in_dash:
            self.expr += "-"

    def typing_keypress(self, key: str) -> None:
        expr_ends_in_dash = len(self.expr) > 0 and self.expr[-1] == "-"

        self.type_key(key, a="x", b="y")

        self.display.clear()
        self.pretty_print_expr()
    
        if key == "#":
            try:
                self.zoom = 1.2
                self.graph()
                self.mode = "graphing"
            except MissingVariableValueError:
                self.display.clear()
                self.display.write(1, 2, "only x and y are allowed!")
        elif key == "D" and expr_ends_in_dash:
            self.catalogue_selection = 0
            self.mode = "catalogue"
            self.keypress("C") # draw the catalogue

    def graphing_keypress(self, key: str) -> None:
        if key == "C":
            self.zoom /= 1.5
        elif key == "D":
            self.zoom *= 1.5
        elif key == "#":
            self.display.clear()
            self.pretty_print_expr()
            self.mode = "typing"
            return

        self.display.clear()
        self.graph()

    def catalogue_keypress(self, key: str) -> None:
        if key == "C":
            self.catalogue_selection -= 1
        elif key == "D":
            self.catalogue_selection += 1
        self.catalogue_selection = min(len(catalogue)-1, max(0, self.catalogue_selection))

        self.display.clear()
        self.display.write(1, 2, "catalogue")
        self.display.write(1, 9, "(of premade functions)")
        self.display.write(1, 128-7-1, "Press A for calculator mode")

        for i, (name, expr) in enumerate(catalogue.items()):
            self.display.write(1, 23+i*7, "  " + name)
            if i == self.catalogue_selection:
                self.display.write(1, 23+i*7, ">")

        if key == "#":
            choice = list(catalogue.values())[self.catalogue_selection]
            self.zoom = choice[0]
            self.expr = choice[1]
            self.mode = "graphing"
            self.graph()
        elif key == "*":
            self.mode = "typing"
            self.expr = self.expr[:-1] # remove trailling '-'
            self.display.clear()
            self.pretty_print_expr()
        elif key == "A":
            self.mode = "calculate"
            self.display.clear()
            self.expr = ""
            self.display.write(1, 2, "_")
    
    def calculate_keypress(self, key: str) -> None:
        expr_ends_in_dash = len(self.expr) > 0 and self.expr[-1] == "-"

        self.type_key(key, a="*", b="/")

        self.display.clear()
        self.display.write(1, 2, self.expr + "_")

        if key == "#":
            try:
                # this is safe because the string can only contains
                # chars that can be typed by the keypad. and besides,
                # your only gonna be able to hack yourself, there's
                # no trust boundary here.
                result = str(eval(self.expr))
            except BaseException as e:
                result = e.__name__
            self.display.clear()
            self.display.write(1, 2, self.expr)
            self.display.write(1, 128-7-1, "=" + result)
        elif key == "D" and expr_ends_in_dash:
            self.catalogue_selection = 0
            self.mode = "catalogue"
            self.keypress("C") # draw the catalogue

    def keypress(self, key: str) -> None:
        if   self.mode == "typing":    self.typing_keypress(key)
        elif self.mode == "graphing":  self.graphing_keypress(key)
        elif self.mode == "catalogue": self.catalogue_keypress(key)
        elif self.mode == "calculate": self.calculate_keypress(key)

if __name__ == "__main__":
    if emulated:
        Calculator(SoftwareDisplay(160, 128, 10)).run()
    else:
        keypad = Keypad(['1', '2', '3', 'A',
                    '4', '5', '6', 'B',
                    '7', '8', '9', 'C',
                    '*', '0', '#', 'D'],
                    [0, 1, 2, 3],
                    [4, 5, 6, 7],
                    4, 4)    
        keypad.set_debounce_time(400)
    
        Calculator(HardwareDisplay(keypad)).run()
