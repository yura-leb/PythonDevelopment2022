import textdistance
import random

# Hamming, Bag
def bullcows(guess: str, secret: str) -> (int, int):
    bag = textdistance.Bag()
    ham = textdistance.Hamming()
    bulls = len(guess) - ham(guess, secret)
    cows = bag(guess, secret)
    return bulls, cows

def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    word = random.choice(words)
    guessed, count = False, 0
    while not guessed:
        ask("Введите слово: ", words)
        inform("Быки: {}, Коровы: {}", bulls, cows)
        count += 1
    return count

def ask(prompt: str, valid: list[str] = None) -> str:
    word = input(prompt)
    if valid:
        if not prompt in valid:
            return ask(prompt, words) 
    else:
        return word

def inform(format_string: str, bulls: int, cows: int) -> None:
    pass

if __name__ == "__main__":
    pass
