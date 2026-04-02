import sys
emulated = sys.implementation.name = "cpython"

if emulated:
    from software_display import SoftwareDisplay
else:
    from hardware_display import HardwareDisplay
    from keypad import Keypad
from cas import Polynomial, ExprSyntaxError, MissingVariableValueError
from utils import *

def graph(polynomial: cas.Polynomial, graph_range: float, display: Display) -> None:
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

    for i in range(display_size):
        y = graph_range * (1 - 2 * i / display_size)
        current_row_vals = [polynomial.substitute(x=x, y=y) for x in x_coords]

        for j in range(display_size):
            current_sign = sign(current_row_vals[j])
            sign_change = False

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
        
    display.write(1, 2, str(polynomial) + "=0")

class Calculator:
    def __init__(self, display: "Display") -> None:
        self.expr = ""
        self.display = display

        self.zoom = 1.2
        self.mode = "typing" # or "graphing"

        self.pretty_print_expr()
        self.display.refresh()

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

    def typing_keypress(self, key: str) -> None:
        if key == "*":
            self.expr = self.expr[:-1]
        elif key.isdigit():
            self.expr += key
        elif key == "A":
            self.expr += "x"
        elif key == "B":
            self.expr += "y"
        elif key == "C" and self.expr[-1] == "+":
            self.expr = self.expr[:-1] + "."
        elif key == "C":
            self.expr += "+"
        elif key == "D":
            self.expr += "-"

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

    def keypress(self, key: str) -> None:
        if self.mode == "typing": self.typing_keypress(key)
        else: self.graphing_keypress(key)

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
