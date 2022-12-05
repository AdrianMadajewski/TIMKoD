import random
import sys
import copy
from string import ascii_lowercase

alphabet = ascii_lowercase + ' ';

filename = 'norm_hamlet.txt'
# filename = 'norm_romeo.txt'
# filename = 'norm_wiki_sample.txt'

def generateRandomMessage(charset, length):
    return ''.join(random.choice(charset) for _ in range(length))


def averageLength(message):
    words = message.split()
    return sum(map(len, words)) / len(words)


# Zadanie 1 - przybliżenie zerowego rzędu
def zeroRowApprox():
    message = generateRandomMessage(alphabet, 100000)
    print(averageLength(message))


# print('Zadanie 1:')
# zeroRowApprox()

# Zadanie 2 - częstość liter
def letterFrequency():
    file = open(filename, 'r')
    dictionary = dict.fromkeys(alphabet, 0)
    for line in file:
        for char in line:
            dictionary[char] += 1
    return dictionary


# print('Zadanie 2:')
# letterFreq = letterFrequency()
# print(sorted(letterFreq.items(), key=lambda item: item[1], reverse=True))


# Zadanie 3 - Przybliżenie pierwszego rzędu
def firstRowApprox(length):
    freq_dict = letterFrequency()
    result = ''
    letters = [*freq_dict.keys()]
    weights = [*freq_dict.values()]
    for _ in range(length):
        result += random.choices(letters, weights)[0]
    return result


# print('Zadanie 3')
# message = firstRowApprox(1000)
# print(message)
# print(averageWordLength(message))

# Zadanie 4 - Prawdopodobienstwo warunkowe liter
# Zaczynamy od e oraz spacji bo wypada najczesciej
def lettersConditionalProbability(current_filename, charset, first_letter=' ', second_letter='e'):
    file = open(current_filename, 'r')
    data = file.read()
    after_first = dict.fromkeys(alphabet, 0)  # Dict ' '
    after_second = dict.fromkeys(alphabet, 0)  # Dict 'e'
    count_first = 0  # Counter ' '
    count_second = 0  # Counter 'e'
    for cursor in range(len(data)):
        next_cursor = cursor + 1
        if next_cursor < len(data):
            # Check for first most prob letter
            if data[cursor] == first_letter:
                count_first += 1

                # Check next item
                if data[next_cursor] in charset:
                    after_first[data[next_cursor]] += 1

            # Check for second most prob letter
            if data[cursor] == second_letter:
                count_second += 1

                # Check next item
                if data[next_cursor] in charset:
                    after_second[data[next_cursor]] += 1

    # Normalize counts
    for letter in charset:
        after_first[letter] /= count_first
        after_second[letter] /= count_second

    # Sort
    s_first = sorted(after_first.items(), key=lambda item: item[1], reverse=True)
    s_second = sorted(after_second.items(), key=lambda item: item[1], reverse=True)

    # print('Po spacji', s_first)
    # print("Po 'e'", s_second)


# Zadanie 4
# lettersConditionalProbability(filename, ascii_lowercase, first_letter=' ', second_letter='e')

# Zadanie 5 Przyblizenia na podstawie zrodla Markova

def markov(step, filename, charset):
    file = open(filename)
    data = file.read()
    letters = {letter: 0 for letter in charset}
    parts = []
    for index in range(len(data) - step):
        current_window = data[index: index + step]
        # Check if window [index : index + step] has 0-9 digits
        for char in current_window:
            if char.isdigit():
                continue

        if current_window not in parts:
            parts.append(current_window)

    part_dict = {key: letters.copy() for key in parts}

    for index in range(len(data) - step):
        part = data[index:index + step]
        if part in parts:
            next_part = data[index + step]
            if next_part in alphabet:
                part_dict[part][next_part] += 1

    return part_dict

def solve(step, sentence, size, filename):
    parts = markov(step, filename, alphabet)

    # if starting sentence is empty get first one from partition dict
    if sentence == '':
        sentence = list(parts.keys())[0]

    for index in range(len(sentence) - step, size):
        part = sentence[index:index + step]
        sentence += random.choices(
            list(parts[part].keys()),
            list(parts[part].values())
        )[0]

    return sentence


# Q1
# sentence1 = solve(1, '', 50, 'norm_hamlet.txt')
# print(sentence1, averageLength(sentence1))

# Q2
# sentence2 = solve(3, '', 50, 'norm_hamlet.txt')
# print(sentence2, averageLength(sentence2))

# Q3
# sentence3 = solve(5, 'probability', 50, 'norm_hamlet.txt')
# print(sentence3, averageLength(sentence3))

in_file = str(sys.argv[1])
out_size = int(sys.argv[2])
out_file = str(sys.argv[3])

sentence1 = solve(1, '', out_size, in_file)
avg1 = round(averageLength(sentence1), 2)

file = open(out_file, 'w')
file.write('Question A:\n')
file.write(sentence1 + '\n')
file.write('Avg word size: ' + str(avg1) + '\n')

sentence2 = solve(3, '', out_size, in_file)
avg2 = round(averageLength(sentence2), 2)

file.write('Question B:\n')
file.write(sentence2 + '\n')
file.write('Avg word size: ' + str(avg2) + '\n')

sentence3 = solve(5, 'probability', out_size, in_file)
avg3 = round(averageLength(sentence3), 2)

file.write('Question C:\n')
file.write(sentence3 + '\n')
file.write('Avg word size: ' + str(avg3) + '\n')