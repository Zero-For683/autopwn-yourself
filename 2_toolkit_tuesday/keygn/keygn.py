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

def suffix_mutator(wordlist, extra_suffixes=None):
    common_suffixes = ['', '1', '12', '123', '1234', '12345',
                       '!', '!!', '1!', '!1', '@', '#', '$', '%', '?', '*',
                       '123!', '1234!', '/1', '_', '__']

    if extra_suffixes:
        common_suffixes += extra_suffixes

    mutated = []
    for word in wordlist:
        for suffix in common_suffixes:
            mutated.append(word + suffix)
    return mutated

def prefix_mutator(wordlist, extra_prefixes=None):
    common_prefixes = ['', '!', '@', '#', '$', '%', '*', '1', '0', '_', '__']

    if extra_prefixes:
        common_prefixes += extra_prefixes

    mutated = []
    for word in wordlist:
        for prefix in common_prefixes:
            mutated.append(prefix + word)
    return mutated

def get_date_variants(dates):
    last_two = [d[-2:] for d in dates if len(d) == 4 and d.isdigit()]
    reversed_dates = [d[::-1] for d in dates]
    combined = dates + last_two + reversed_dates

    separators = ['', '_', '-', '.', '!', '/']
    all_formatted = []

    for date in combined:
        for sep in separators:
            all_formatted.append(f"{sep}{date}")  # for suffix
            all_formatted.append(f"{date}{sep}")  # for prefix

    return list(set(all_formatted))

def combine_with_dates(wordlist, date_variants):
    combined = []
    for word in wordlist:
        for date in date_variants:
            combined.append(word + date)
    return combined


def read_wordlist(filename):
    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] Wordlist '{filename}' not found.")
        return []


def parse_args():
    parser = argparse.ArgumentParser(description="keygn: Personal wordlist generator")
    parser.add_argument('--words', nargs='+', required=True, help='List of base keywords')
    parser.add_argument('--leet', action='store_true', help='Apply leetspeak mutations')
    parser.add_argument('--suffix', action='store_true', help='Apply common suffixes')
    parser.add_argument('--prefix', action='store_true', help='Apply common prefixes')
    parser.add_argument('--output', default='keygn_output.txt', help='Output file name')
    parser.add_argument('--dates', nargs='+', help='List of important dates (e.g. 1995 07 2020)')
    parser.add_argument('--rockyou', action='store_true', help='Include top5000 passwords from rockyou.txt')
    parser.add_argument('--waterfall', action='store_true', help='Include waterfall/keyboard-walk passwords (roughly 7k passwords)')
    return parser.parse_args()

def main():
    args = parse_args()

    # Step 1: Normalize
    args.words = [word.lower() for word in args.words]
    keywords_uppercase = capitalize_words(args.words)

    # Step 2: Base combos
    combos_upper = generate_combinations(keywords_uppercase)
    combos_lower = generate_combinations(args.words)
    pre_mutation = keywords_uppercase + combos_lower + combos_upper

    # Step 3: Optional date-aware combos
    if args.dates:
        date_variants = get_date_variants(args.dates)
        pre_mutation += combine_with_dates(pre_mutation, date_variants)


    # Step 4: Begin mutations
    mutated = pre_mutation.copy()

    if args.leet:
        mutated += leet_mutate(pre_mutation)

    if args.prefix:
        mutated = prefix_mutator(mutated)
    if args.suffix:
        mutated = suffix_mutator(mutated)



    if args.rockyou:
        mutated += read_wordlist("top5000.txt")
    if args.waterfall:
        mutated += read_wordlist("combo_walks.txt")

    with open(args.output, 'w') as f:
        for word in sorted(set(mutated)):  # deduplicate
            f.write(word + '\n')

    print(f"[+] Generated {len(set(mutated))} passwords in '{args.output}'")

if __name__ == "__main__":
    main()