
from simple_patterns import Either
from simple_patterns import Lit

from parsing_text import Tokenizer
from parsing_text import Parser


def test_tok_empty_string():
    assert Tokenizer().tok("") == []


def test_tok_any_either():
    assert Tokenizer().tok("*{abc,def}") == [
        ["Any"],
        ["EitherStart"],
        ["Lit", "abc"],
        ["Lit", "def"],
        ["EitherEnd"]
    ]


def test_parse_either_two():
    assert Parser().parse("{abc,def}") == Either(
        [Lit("abc"), Lit("def")]
    )