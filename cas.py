import re

from utils import *

class ExprSyntaxError(Exception):
    def __init__(self, message: str, expr: str, position: int) -> None:
        self.message = message
        self.expr = expr
        self.position = position

        if position is not None and expr:
            pointer = " " * position + "^"
            full_message = f"{message} at position {position}\n{expr}\n{pointer}"
        elif position is not None:
            full_message = f"{message} at position {position}"
        else:
            full_message = message

        super().__init__(full_message)

class MissingVariableValueError(Exception):
    pass

class Monomial:
    def __init__(self, expr: str) -> None:
        self.coefficient = 1
        self.indeterminates = {}

        if not expr:
            raise ExprSyntaxError("empty monomial", expr, 0)
        if expr[0] == "-":
            self.coefficient *= -1
            expr = expr[1:]

        acc = ""
        for i, ch in enumerate(expr):
            if ch in "+ ": continue

            if ch in "0123456789.":
                acc += ch
                continue
            elif acc:
                self.coefficient *= float(acc)
                acc = ""

            if ch.isalpha():
                self.indeterminates[ch] = self.indeterminates.get(ch, 0) + 1
            else:
                raise ExprSyntaxError("invalid character", expr, i)

        if isnumeric(acc.replace(".", "")):
            self.coefficient *= float(acc)

    def substitute(self, **variables: dict[str, float]) -> float:
        result = self.coefficient
        for var, power in self.indeterminates.items():
            if var not in variables:
                raise MissingVariableValueError(f"missing value for '{var}' in substitution")
            result *= variables[var] ** power
        return result

    def __str__(self) -> str:
        string = ""
        if abs(self.coefficient) != 1: string += f"{self.coefficient:g}"
        elif self.coefficient == -1: string += "-"

        for var, power in sorted(self.indeterminates.items()):
            string += var
            if power != 1: string += translate(str(power), SUPERSCRIPT)

        if abs(self.coefficient) == 1 and not self.indeterminates: string += "1"
        return string

class Polynomial:
    def __init__(self, expr: str) -> None:
        self.terms: list[Monomial] = [Monomial(t) for t in split_terms(expr)]

    def substitute(self, **variables: dict[str, float]) -> float:
        result = 0
        for term in self.terms:
            result += term.substitute(**variables)
        return result

    def __str__(self) -> str:
        string = ""
        for i, term in enumerate(self.terms):
            if term.coefficient > 0 and i != 0:
                string += "+"
            string += str(term)
        
        return string

