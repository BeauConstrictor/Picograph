# Picograph – Graphing Calculator

A graphing calculator that runs on a Pi Pico. If run locally, the Python code automatically emulates the device using pygame.

You input expressions via a hex keypad, which are interpreted as bivariate implicit polynomial equations. Expressions must be entered in fully expanded form.

## Syntax

- `A` & `B`: Enter *x* and *y* into expressions.
- `C` & `D`: Enter *+* and *-*.
- `*`: Backspace
- `#`: *= 0*; toggles between editing and viewing mode.

For exponentiation, repeatedly hit the same variable key (e.g., `AAA` → *x³*). For a decimal point, double press `C`.

In viewing mode, use `C` & `D` to zoom in and out.

## Catalogue

The catalogue features approximations of some common functions that cannot be graphed fully. To enter the catalogue, double press the `D` key.

These approximations are implemented as [Taylor series](https://en.wikipedia.org/wiki/Taylor_series). These expressions are quite slow to evaluate on real hardware, so the zoom is automatically set to get you the best view of the function - zooming out too far will reveal the 'limitations' of the approximation.

## Implementation

To run on hardware:

Use a Pico Omnibus or similar device to duplicate the Pico’s pins.

On one pin set, connect a [Waveshare Pico LCD 1.8"](https://www.waveshare.com/wiki/Pico-LCD-1.8).

On the other pin set, connect a 4×4 matrix keypad as follows (rows → pins 0–3, columns → pins 4–7):

```
1 2 3 A
4 5 6 B
7 8 9 C
* 0 # D
```

## License

This project is licensed under GNU GPLv3.