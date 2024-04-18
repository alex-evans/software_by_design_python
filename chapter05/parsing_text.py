
import string

from simple_patterns import Any
from simple_patterns import Either
from simple_patterns import Lit
from simple_patterns import Null


CHARS = set(string.ascii_letters + string.digits)


class Tokenizer:
    def __init__(self):
        self._setup()

    def _setup(self):
        self.result = []
        self.current = ""

    def tok(self, text):
        self._setup()
        for ch in text:
            if ch == "*":
                self._add("Any")
            elif ch == "{":
                self._add("EitherStart")
            elif ch == ",":
                self._add(None)
            elif ch == "}":
                self._add("EitherEnd")
            elif ch in CHARS:
                self.current += ch
            else:
                raise NotImplementedError(f"what is '{ch}'?")
        self._add(None)
        return self.result

    def _add(self, thing):
        if len(self.current) > 0:
            self.result.append(["Lit", self.current])
            self.current = ""
        if thing is not None:
            self.result.append([thing])


class Parser:
    def __init__(self):
        self._setup()
        self.tokenizer = Tokenizer()
        self.tokens = []

    def _setup(self):
        self.result = []
        self.current = ""

    def parse(self, text):
        self._setup()
        tokens = self.tokenizer.tok(text)
        self._parse(tokens)

    def _parse(self, tokens):
        if not tokens:
            return Null()
        
        front, back = tokens[0], tokens[1:]
        if front[0] == "Any":
            handler = self._parse_Any
        elif front[0] == "EitherStart":
            handler = self._parse_EitherStart
        elif front[0] == "Lit":
            handler = self._parse_Lit
        else:
            assert False, f"Unknown token type {front}"

        return handler(front[1:], back)
    
    def _parse_Any(self, rest, back):
        return Any(self._parse(back))
    
    def _parse_Lit(self, rest, back):
        return Lit(rest[0], self._parse(back))
    
    # def _parse_EitherStart(self, rest, back):
    #     if (
    #         len(back) < 3
    #         or (back[0][0] != "Lit")
    #         or (back[1][0] != "Lit")
    #         or (back[2][0] != "EitherEnd")
    #     ):
    #         raise ValueError("badly-formatted Either")
    #     left = Lit(back[0][1])
    #     right = Lit(back[1][1])
    #     return Either([left, right], self._parse(back[3:]))

    def _parse_EitherStart(self, rest, back):
        children = []
        while back and (back[0][0] == "Lit"):
            children.append(Lit(back[0][1]))
            back = back[1:]

        if not children:
            raise ValueError("empty Either")

        if back[0][0] != "EitherEnd":
            raise ValueError("badly-formatted Either")

        return Either(children, self._parse(back[1:]))
