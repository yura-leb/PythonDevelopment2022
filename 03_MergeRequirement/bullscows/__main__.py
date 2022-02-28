import textdistance
import random
import argparse
import urllib.request

# Hamming, Bag
def bullscows(guess: str, secret: str) -> (int, int):
    bag = textdistance.Bag()
    ham = textdistance.Hamming()
    bulls = max(len(secret), len(guess)) - ham(guess, secret)
    cows = max(len(secret), len(guess)) - bag(guess, secret)
    return bulls, cows

def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    word = random.choice(words)
    count = 0
    guessed, count = False, 0
    while not guessed:
        count += 1
        guess = ask("Введите слово: ", words)
        bulls, cows = bullscows(guess, word)
        inform("Быки: {}, Коровы: {}", bulls, cows)
        guessed = (bulls == len(word))
    return count

def ask(prompt: str, valid: list[str] = None) -> str:
    word = input(prompt)
    if valid:
        if word in valid:
            return word
        else:
            return ask(prompt, words)
    else:
        return word

def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('words_path', type=str, help='Dictionary to get words from')
    parser.add_argument('length', type=int, nargs='?', help='Dictionary to get words from')
    args = parser.parse_args()
    words = []
    if not args.length:
        args.length = 5
    try:
        with open(args.words_path, 'rt') as f:
            words = f.read().split('\n')
    except FileNotFoundError:
        pass
    try:
        with urllib.request.urlopen(args.words_path) as f:
            words = f.read().decode('utf-8').split('\n')
    except ValueError:
        pass
    if words:
        words = [word for word in words if len(word) == args.length]
        print(gameplay(ask, inform, words))
