# Graphing Calculator

A graphing calculator the runs on a Pi Pico. If you try to run the python code locally, it will automatically emulate using pygame.

You type expressions on a hex keypad and they are interpreted as *bivariate implicit polynomial equations*, which must be entered in fully expanded form.

## Syntax

To enter expressions, use the `A` & `B` keys to enter *x* and *y* into an expression, respectively. `*` servers as backspace and `#` serves as enter/equals, toggling between viewing and editing mode. The `C` & `D` keys enter `+` and `-` respectively. To use powers, repeatedly type the appropriate key - for instance, Typing `AAA` cause *x³* to appear on the screen. When in viewing mode, you can use `C` & `D` to zoom in and out, respectively.

## Implementation

To run this software on real hardware, use a Pico Omnibus or similar device to split the duplicate the Pico's pins. On one of these pin sets, connect a (Waveshare Pico LCD 1.8")[https://www.waveshare.com/wiki/Pico-LCD-1.8). On the other set of pins, connect a 4x4 matrix keypad's rows to pins `0-3` and columns to pins `4-7` (inclusive). This layout is assumed:

```
1 2 3 A
4 5 6 B
7 8 9 C
* 0 # D
```

## License

This project uses the GNU GPLv3.# Picograph
