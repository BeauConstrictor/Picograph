superscripts = "⁰¹²³⁴⁵⁶⁷⁸⁹"
normal_digits = "0123456789"
SUPERSCRIPT = {n: s for n, s in zip(normal_digits, superscripts)}

superscripts = "⁰¹²³⁴⁵⁶⁷⁸⁹"
normal_digits = "0123456789"
NORMALSCRIPT = {s: n for s, n in zip(superscripts, normal_digits)}

def isnumeric(s: str) -> bool:
    if not s:
        return False
    for c in s:
        if c not in "0123456789":
            return False
    return True

def split_terms(expr: str) -> list[str]:
    terms = []
    term = ""
    for i, c in enumerate(expr):
        if c in "+-" and term:
            terms.append(term)
            term = c
        else:
            term += c
    if term:
        terms.append(term)
    return terms

def translate(s: str, table: dict[str, str]) -> str:
    result = ""
    for c in s:
        result += table.get(c, c)
    return result

def sign(val: float) -> int:
        return 1 if val > 0 else -1 if val < 0 else 0
