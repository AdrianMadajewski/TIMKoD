#!/usr/bin/python3

import typing
import random
import sys

def hasNumber(string : str):
    return any(char.isdigit() for char in string)

def loadWordsFromFile(filename : str):
    file = open(filename, 'r')
    words = {}
    for line in file:
        for word in line.split():
            if hasNumber(word):
                continue

            if word in words:
                 words[word] += 1
            else:
                 words[word] = 1
   
    file.close()
    return words

words = loadWordsFromFile('norm_wiki_sample.txt')
# # # print(words)
sorted_words = sorted(words.items(), key = lambda value: value[1], reverse=True)
# print(sorted_words)

# Top words (exercise 1)
# print(sorted_words[:30000])
# print(len(sorted_words))

def wordPercent(words: list, bound : int):
    sum_all = sum(value[1] for value in words)
    sum_bound = sum(value[1] for value in words[:bound])
    return sum_bound / sum_all

# most frequent 10
# for key, value in sorted_words[:10]:
    # print(f'{key} = {value} ({value / sum_all:.2f}%)')

# print(f'30 tysiecy najpopularniejszych slow stanowi {wordPercent(sorted_words, 30000):.2f}% wszystkich slow')
# print(f'6 tysiecy najpopularniejszych slow stanowi {wordPercent(sorted_words, 6000):.2f}% wszystkich slow')

def firstRowApprox(words, length):
    result = []
    letters = [*words.keys()]
    weights = [*words.values()]
    for _ in range(length):
        result.append(random.choices(letters, weights)[0])
    return ' '.join(result)

# print('PRZYBLIZENIE PIERWSZEGO RZEDU')
message = firstRowApprox(words, 100)
# print(message)
# print('PRZYBLIZENIE PIERWSZEGO RZEDU')

def readWordsFromFile(filename):
    file = open(filename, 'r')
    words = []

    for line in file:
        for word in line.split():
            if not hasNumber(word):
                words.append(word)
    
    file.close()
    return words

def markov(step, filename, sample_size):
    # Setup
    words = readWordsFromFile(filename)[:sample_size]
    dictionary = {}
    
    # Load dictionary
    for index in range(len(words) - step):
        temp_chunk = ' '.join(words[index:index + step])
        chunk = words[index + step]
        
        # Check if chunk exists in dictionary
        if temp_chunk in list(dictionary.keys()):
            if chunk in list(dictionary[temp_chunk].keys()):
                dictionary[temp_chunk][chunk] += 1
            else:
                dictionary[temp_chunk][chunk] = 1
        else:
            dictionary[temp_chunk] = {}
            dictionary[temp_chunk][chunk] = 1
    
    return dictionary


def solve(in_filename, step, probe_size, start_word, sentence_size, out_filename):
    print(f'{out_filename}: Creating chunks')
    chunks = markov(step, in_filename, probe_size) 
    words = readWordsFromFile(in_filename)[:probe_size]
    output = random.sample(words, step)
    
    print(f'{out_filename}: Creating starting points')
    if start_word != '':
        output[0] = start_word

    # Check if output is valid
    while ' '.join(output) not in chunks.keys():
        if start_word != '':
            output = [start_word] + random.sample(words, step - 1)
        else:
            output = random.sample(words, step)
    
    print(f'{out_filename}: Generating sentence')
    # Generate sentence
    for _ in range(sentence_size):
        output += random.choices(
                list(chunks[' '.join(output[-step:])].keys()),
                list(chunks[' '.join(output[-step:])].values()),
                k = 1)

    print(f'{out_filename}: Writing to file')
    output_file = open(out_filename, 'w')
    output_file.write(' '.join(output))
    output_file.write('\n')
    output_file.close()
    print(f'{out_filename}: Finished')


input_filename = sys.argv[1]
step = int(sys.argv[2])
probe_size = int(sys.argv[3])
sentence_size = int(sys.argv[4])
output_filename = sys.argv[5]
starting_word = '' if len(sys.argv) != 7 else sys.argv[6]

# Main
solve(input_filename, step, probe_size, starting_word, sentence_size, output_filename)
