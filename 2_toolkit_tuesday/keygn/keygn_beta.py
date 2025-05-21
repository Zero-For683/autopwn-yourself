import argparse
from itertools import product, permutations

# Leet mapping
leet_map = {
    'a': ['@', '4'],
    'b': ['8'],
    'e': ['3'],
    'g': ['9', '6'],
    'i': ['1', '!'],
    'l': ['1'],
    'o': ['0'],
    's': ['$', '5'],
    't': ['7', '+'],
    'z': ['2']
}

def capitalize_words(words):
    result = []
    for word in words:
        result.append(word)
        if not word[0].isdigit():
            result.append(word.capitalize())
    return result

def generate_combinations(words, min_len=2, max_len=4):
    combos = []
    for r in range(min_len, max_len + 1):
        for p in permutations(words, r):
            combos.append(''.join(p))
    return combos

def leet_mutate(wordlist):
    leet_words = []
    for word in wordlist:
        char_options = []
        for letter in word:
            if letter.lower() in leet_map:
                char_options.append([letter] + leet_map[letter.lower()])
            else:
                char_options.append([letter])
        for combo in product(*char_options):
            leet_words.append(''.join(combo))
    return leet_words

def suffix_mutator(wordlist):
    common_suffixes = ['', '1', '12', '123', '1234', '12345', '321', '007',
                       '!', '!!', '1!', '!1', '@', '#', '$', '%', '?', '*',
                       '123!', '1234!', '1@3', '/1']
    mutated = []
    for word in wordlist:
        for suffix in common_suffixes:
            mutated.append(word + suffix)
    return mutated

def prefix_mutator(wordlist):
    common_prefixes = ['', '!', '@', '#', '$', '%', '*', '1', '0']
    mutated = []
    for word in wordlist:
        for prefix in common_prefixes:
            mutated.append(prefix + word)
    return mutated

def parse_args():
    parser = argparse.ArgumentParser(description="keygn: Personal wordlist generator")
    parser.add_argument('--words', nargs='+', required=True, help='List of base keywords')
    parser.add_argument('--leet', action='store_true', help='Apply leetspeak mutations')
    parser.add_argument('--suffix', action='store_true', help='Apply common suffixes')
    parser.add_argument('--prefix', action='store_true', help='Apply common prefixes')
    parser.add_argument('--output', default='keygn_output.txt', help='Output file name')
    return parser.parse_args()

def main():
    args = parse_args()

    # Step 1: Normalize and capitalize
    keywords = capitalize_words(args.words)

    # Step 2: Combine words
    combos = generate_combinations(keywords)
    pre_mutation = keywords + combos

    # Step 3: Leetspeak if enabled
    mutated = leet_mutate(pre_mutation) if args.leet else pre_mutation

    # Step 4: Prefix/suffix if enabled
    if args.prefix:
        mutated = prefix_mutator(mutated)
    if args.suffix:
        mutated = suffix_mutator(mutated)

    # Step 5: Write results
    with open(args.output, 'w') as f:
        for word in sorted(set(mutated)):  # deduplicate
            f.write(word + '\n')

    print(f"[+] Generated {len(set(mutated))} passwords in '{args.output}'")

if __name__ == "__main__":
    main()