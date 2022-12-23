import numpy as np

num = np.arange(26)
alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
num_to_alphabet = dict(zip(num, alphabet))
alphabet_to_num = dict(zip(alphabet, num))

def make_arr(seed):
    np.random.seed(seed)
    arr = np.arange(26)
    np.random.shuffle(arr)
    return arr

def match_arr(A, a, b):
    return num_to_alphabet[np.where(b==a[alphabet_to_num[A]])[0][0]]

def make_pairs(ar, seed):
    np.random.seed(seed)
    np.random.shuffle(ar)
    pairs = []
    for i in range(0, len(ar) - 1, 2):
        pairs.append([ar[i], ar[i + 1]])
    return pairs

class Rotor:
    def __init__(self, seed):
        self.seed = seed
        self.arr_0 = make_arr(seed)
        self.arr_1 = make_arr(seed + 1)
    
    def encode(self, A):
        return match_arr(A, self.arr_0, self.arr_1)
    
    def decode(self, A):
        return match_arr(A, self.arr_1, self.arr_0)
    
    def rotate(self):
        self.arr_0 = np.roll(self.arr_0, 1)
        self.arr_1 = np.roll(self.arr_1, 1)

class Turnover:
    def __init__(self, seed):
        self.seed = seed
        self.pairs = make_pairs(np.arange(26), seed)
        # print(self.pairs)
    
    def encode(self, A):
        for pair in self.pairs:
            if A == num_to_alphabet[pair[0]]:
                return num_to_alphabet[pair[1]]
            elif A == num_to_alphabet[pair[1]]:
                return num_to_alphabet[pair[0]]
        return A

# 関数の呼び出し回数を記録するカウンタ
class Counter:
    def __init__(self):
        self.count = 0
    
    def count_up(self):
        self.count += 1
    
    def reset(self):
        self.count = 0

class EnigmaMachine:
    def __init__(self, seed):
        self.rotor1 = Rotor(seed)
        self.rotor2 = Rotor(seed + 1)
        self.rotor3 = Rotor(seed + 2)
        self.turnover = Turnover(seed + 3)
        self.counter = Counter()
        
    def encode_a_character(self, A):
        self.counter.count_up()
        # print(A, end="")
        A = self.rotor1.encode(A)
        # print(A, end="")
        A = self.rotor2.encode(A)
        # print(A, end="")
        A = self.rotor3.encode(A)
        # print(A, end="")
        A = self.turnover.encode(A)
        # print(A, end="")
        A = self.rotor3.decode(A)
        # print(A, end="")
        A = self.rotor2.decode(A)
        # print(A, end="")
        A = self.rotor1.decode(A)
        # print(A)
        self.rotor1.rotate()
        if self.counter.count % (26) == 0:
            self.rotor2.rotate()
        if self.counter.count % 26**2 == 0:
            self.rotor3.rotate()
        return A
    
    def encode_a_word(self, word):
        return "".join([self.encode_a_character(A) for A in word])
    
    def encode(self, text):
        text = text.upper()
        return " ".join([self.encode_a_word(word) for word in text.split(" ")])
    
    def reset(self):
        self.rotor1 = Rotor(self.rotor1.seed)
        self.rotor2 = Rotor(self.rotor2.seed)
        self.rotor3 = Rotor(self.rotor3.seed)
        self.turnover = Turnover(self.turnover.seed)
        self.counter.reset()


if __name__ == "__main__":
    print("=== Welcome to Enigma Machine! ===")
    print("Please input a seed number.")
    seed = int(input())
    enigma = EnigmaMachine(seed)
    while True:
        print("\nPlease select an operation.")
        print("1: Encode/Decode a text")
        print("2: Reset the machine")
        print("3: Exit")
        try:
            operation = int(input())
        except:
            print("### Invalid operation! ###")
            continue
        if operation == 1:
            print("Please input a text.")
            text = input()
            print(enigma.encode(text))
        elif operation == 2:
            enigma.reset()
        elif operation == 3:
            print("=== Thank you for using Enigma Machine! ===")
            break
        else:
            print("### Invalid operation! ###")