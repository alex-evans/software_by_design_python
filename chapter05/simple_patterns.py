
class Match:
    def __init__(self, rest):
        self.rest = rest if rest is not None else Null()

    def __eq__(self, other):
        return (other is not None and
                self.__class__ == other.__class__ and
                self.rest == other.rest)

    def match(self, text):
        result = self._match(text, 0)
        return result == len(text)


class Null(Match):
    def __init__(self):
        self.rest = None

    def _match(self, text, start):
        return start


class Lit(Match):
    def __init__(self, chars, rest=None):
        super().__init__(rest)
        self.chars = chars

    def __eq__(self, other):
        return super().__eq__(other) and (
            self.chars == other.chars
        )

    # def _match(self, text, start):
    #     end = start + len(self.chars)
    #     if text[start:end] != self.chars:
    #         return None
    #     return self.rest._match(text, end)
    

class Any(Match):
    def __init__(self, rest=None):
        super().__init__(rest)

    def _match(self, text, start):
        for i in range(start, len(text) + 1):
            end = self.rest._match(text, i)
            if end == len(text):
                return end
        return None
    

class Either(Match):
    def __init__(self, children, rest=None):
        super().__init__(rest)
        self.children = children

    def __eq__(self, other):
        return super().__eq__(other) and self.children.__eq__(
            other.children
        )

