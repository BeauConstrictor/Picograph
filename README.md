# Picograph – Graphing Calculator

A graphing calculator that runs on a Pi Pico. If run locally, the Python code automatically emulates the device using pygame.

<img src="/assets/picograph.png" alt="Screenshot of a rotated ellipse" width="400" />

You input expressions via a hex keypad, which are interpreted as bivariate implicit polynomial equations. Expressions must be entered in fully expanded form.

## Syntax

- `A` & `B`: Enter *x* and *y* into expressions.
- `C` & `D`: Enter *+* and *-*.
- `*`: Backspace
- `#`: *= 0*; toggles between editing and viewing mode.

For exponentiation, repeatedly hit the same variable key (e.g., `AAA` → *x³*). For a decimal point, double press `C`.

In viewing mode, use `C` & `D` to zoom in and out.

## Catalogue

The catalogue features some pre-written functions that you can graph right away. Some of the functions are approximations, as they cannot be expressed fully in polynomial form. To enter the catalogue, double press the `D` key.

These approximations are implemented as [Taylor series](https://en.wikipedia.org/wiki/Taylor_series). These expressions are quite slow to evaluate on real hardware, so the zoom is automatically set to get you the best view of the function - zooming out too far will reveal the 'limitations' of the approximation.

## Calculator Mode

You can also enter a simple calculation mode by pressing A when on the catalogue screen. Here, the buttons `A` & `B` serve as multiplcation and division, respectively. Every other button has the same function as in the normal.

To multiplication signs in a row actually performs exponentiation.

To exit this mode, double press `D`. 

## Implementation

### 1. Construction

Use a Pico Omnibus or similar device to duplicate the Pico’s pins.

On one pin set, connect a [Waveshare Pico LCD 1.8"](https://www.waveshare.com/wiki/Pico-LCD-1.8).

On the other pin set, connect a 4×4 matrix keypad as follows (rows -> pins 0-3, columns -> pins 4-7):

```
1 2 3 A
4 5 6 B
7 8 9 C
* 0 # D
```

I call this device the 'Picophone' and use it in a few of my other projects. You can also easily connect a switch and battery to make it fully portable.

### 2. Installation

Once you have built the Picophone, use `make flash` (micropython must be installed on the Pico and `mpremote` must be installed on your machine through `pip`) to install the software.

## License

This project is licensed under GNU GPLv3.
