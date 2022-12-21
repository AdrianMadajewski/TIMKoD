import os
import math
from bitarray import bitarray

# Read file contents
def read_file(file_name):
    file = open(file_name, 'r')
    return file.read()

# Analyze content - calculate probability
def analyze_content(content):
    letters = {}
    counter = 0

    for _, letter in enumerate(content):
        cardinality = letters.get(letter, 0)
        letters.update({letter: cardinality + 1})
        counter += 1

    return letters, counter


# Create code
def create(dictionary: dict):
    code_dictionary = {}
    unique_characters = len(dictionary.keys())
    length = math.ceil(math.log(unique_characters + 1, 2))

    for index, key in enumerate(dictionary.keys()):
        base = int_to_bits(length, index)
        code_dictionary.update({key: base})
    return code_dictionary, length


# Convert integer value to bit array
def int_to_bits(length, value):
    bits_array = [1 if digit == '1' else 0 for digit in bin(value)[2:]]
    bits = bitarray(length - len(bits_array))
    bits.setall(0)
    for bit in bits_array:
        bits.append(bit)
    return bits


# Encode text
def encode(code_dict: dict, text: str):
    encoded = bitarray()

    for letter in text:
        for bit in code_dict.get(letter):
            encoded.append(bit)

    return encoded


# Decode text
def decode(encoded_bits: bitarray, code_dict: dict, length):
    decoded = ''
    total_length = len(encoded_bits)

    for index in range(int(total_length / length)):
        code = encoded_bits[index * length: (index + 1) * length].to01()
        decoded += code_dict.get(code, '')

    return decoded


# Save encoded details to file
def save(code_dict: dict, encoded_content: bitarray, directory: str, bytesize = 8):
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Normalize to bytesize byte
    content = encoded_content.copy()
    for _ in range(len(content) % bytesize):
        content.append(1)

    # Save encoded result to file
    with open(directory + 'result', 'wb') as content_file:
        content.tofile(content_file)

    # Save encoding to file
    with open(directory + 'key', 'w') as key_file:
        for key in code_dict.keys():
            key_file.write(key)


# Load
def load(directory):
    encoded_content = bitarray()
    code_dictionary = {}

    # Load encoded file
    with open(directory + 'result', 'rb') as content_file:
        encoded_content.fromfile(content_file)

    # Load encoded key-file and set values
    with open(directory + 'key', 'r') as key_file:
        content = key_file.read()
        code_length = math.ceil(math.log(len(content) + 1, 2))

        for index, key in enumerate(content):
            base = int_to_bits(code_length, index)
            code_dictionary.update({base.to01(): key})

    return encoded_content, code_length, code_dictionary


# Calculate size
def calculate_sizes(directory, original):
    encoded_size = os.stat(directory + 'result').st_size
    key_size = os.stat(directory + 'key').st_size
    original_size = os.stat(original).st_size
    return encoded_size, key_size, original_size

def main():
    directory_name = 'encoded/'
    file_name = 'norm_wiki_sample.txt'

    # Read
    content = read_file(file_name)
    letters_dictionary, _ = analyze_content(content)
    code_dict, _ = create(letters_dictionary)
    encoded = encode(code_dict, content)

    # Save
    save(code_dict, encoded, directory_name)

    # Load
    encoded_content, loaded_code_length, loaded_code_dictionary = load(directory_name)
    decoded = decode(encoded_content, loaded_code_dictionary, loaded_code_length)

    # Stats
    encode_size, key_size, file_size = calculate_sizes(directory_name, file_name)

    sum_size = key_size + encode_size
    print(f'Original file: "{file_name}"')
    print(f'File size: {file_size} [bytes]')

    print(f'Encoded size: {encode_size} [bytes]')
    print(f'Key size: {key_size} [bytes]')
    print(f'All size: {sum_size} [bytes]')

    print('Compare files check')

    compression_ratio = round(file_size / sum_size, 2)
    space_saving = round(1 - sum_size / file_size, 2)

    if decoded == content:
        print('Equal == true (✓)')
        print(f'Compression ratio: {compression_ratio}')
        print(f'Space saving: {space_saving}')
    else:
        print('Content != Decoded(Encoded(Content))')

        print(content)
        print('\n\n--------\n\n')
        print(decoded)


if __name__ == '__main__':
    main()