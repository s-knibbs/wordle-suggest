from __future__ import annotations

from argparse import ArgumentParser
import readline  # noqa
from collections import defaultdict, Counter
from dataclasses import dataclass
from typing import Iterator, TypeVar, Sequence


ALPHABET = set("abcdefghijklmnopqrstuvwxyz")
DEFAULT_WORD_LIST = '/usr/share/dict/british-english-large'

T = TypeVar("T")


def chunked(items: Sequence[T], size: int) -> Iterator[Sequence[T]]:
    for idx in range(0, len(items), size):
        yield items[idx:idx + size]


@dataclass
class WordleClue:
    guess: str
    present: Counter[str]
    missing: set[str]
    matching: dict[int, str]

    @classmethod
    def from_str(cls, clue: str) -> WordleClue:
        try:
            guess, present, matching = clue.lower().split(':')
            matching = {int(match[0]): match[1] for match in chunked(matching, 2)}
        except ValueError:
            try:
                guess, present = clue.lower().split(":")
            except ValueError:
                guess = clue.lower()
                present = ''
            matching = {}
        missing = set(guess) - set(present) - set(matching.values())
        return WordleClue(guess, Counter(present) + Counter(matching.values()), missing, matching)

    def validate(self, words: set[str]) -> str | None:
        if self.guess not in words:
            return f"'{self.guess}' is not a 5-letter word"
        if len(self.present) != len(ALPHABET & set(self.present.keys())):
            p = ''.join(self.present.keys())
            return f"Invalid characters in letters present '{p}'"
        for idx, match in self.matching.items():
            if len(match) != 1 or match not in ALPHABET:
                return f"Invalid match '{idx}{match}'"
        return None


@dataclass
class WordsIndexes:
    words: set[str]
    letter_lookup: dict[str, set[str]]
    match_lookup: tuple[dict[str, set[str]], ...]

    @classmethod
    def from_words(cls, words: set[str]) -> WordsIndexes:
        match_lookup = (defaultdict(set), defaultdict(set), defaultdict(set), defaultdict(set), defaultdict(set))
        letter_lookup = defaultdict(set)
        for word in words:
            for idx, letter in enumerate(word):
                letter_lookup[letter].add(word)
                match_lookup[idx][letter].add(word)
        return WordsIndexes(words, letter_lookup, match_lookup)

    def matching_words(self, clue: WordleClue) -> set[str]:
        matching_words = None
        for idx, letter in clue.matching.items():
            if matching_words is None:
                matching_words = set(self.match_lookup[idx][letter])
            else:
                matching_words &= self.match_lookup[idx][letter]

        for present, count in clue.present.items():
            matches = {word for word in self.letter_lookup[present] if Counter(word)[present] >= count}
            if matching_words is None:
                matching_words = matches
            else:
                matching_words &= matches

        if matching_words is None:
            matching_words = set(self.words)

        non_matching_words = set()
        for word in matching_words:
            if set(word) & clue.missing:
                non_matching_words.add(word)
        for idx, letter in enumerate(clue.guess):
            if idx in clue.matching:
                continue
            non_matching_words |= self.match_lookup[idx][letter]
        return matching_words - non_matching_words


def get_word_list(word_list_file: str) -> set[str]:
    words = set()
    with open(word_list_file) as words_file:
        for line in words_file:
            word = line.strip()
            if len(word) == 5 and "'" not in word:
                words.add(word.lower())
    return words


REPL_USAGE = """
The program operates as a REPL. Enter clues in the format 'GUESS:PRESENT:MATCHES', example 'slate:a:0s3t'.
The number of possible answers will decrease as each clue is entered. Use CTRL+D to reset the answers.
CTRL+C to exit.
"""


def main():
    parser = ArgumentParser(epilog=REPL_USAGE)
    parser.add_argument("-w", "--word-list", default=DEFAULT_WORD_LIST, type=str, help="Path to word list")
    args = parser.parse_args()
    words = get_word_list(args.word_list)
    index = WordsIndexes.from_words(words)
    matches = set(words)
    while True:
        try:
            try:
                clue = WordleClue.from_str(input(f"{len(matches)} answers> "))
            except (ValueError, IndexError):
                print("Invalid clue - format: GUESS:PRESENT:MATCHES 'valid:li:4d'")
                continue
            except EOFError:
                matches = set(words)
                print()
                continue
            error = clue.validate(words)
            if error:
                print(error)
                continue
            matches &= index.matching_words(clue)
            for chunk in chunked(sorted(matches), 6):
                print("  ".join(chunk))
        except KeyboardInterrupt:
            print()
            return


if __name__ == "__main__":
    main()
