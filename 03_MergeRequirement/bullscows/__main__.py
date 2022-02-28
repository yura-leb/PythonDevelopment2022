import textdistance
# Hamming, Bag
def bullcows(guess: str, secret: str) -> (int, int):
    bag = textdistance.Bag()
    ham = textdistance.Hamming()
    bulls = len(guess) - ham(guess, secret)
    cows = bag(guess, secret)
   return bulls, cows

