from itertools import product, permutations

# Basic input of words to accept -> Capitalize and lowercase start of each word

keywords = ["cookie", "cat", "geyer", "liesel", "14", "7", "2003"]
keywords_capitalized_lowercase = []
for word in keywords:
    keywords_capitalized_lowercase.append(word)
    if not word[0].isdigit():
        keywords_capitalized_lowercase.append(word.capitalize())




# Combine those words together in every variation possible (2 word combos, 3 word combos, and 4 word combos, capitalization and all)

combinations = [
    ''.join(p)
    for r in range(2, 5)  # r = 2, 3, 4 word combos
    for p in permutations(keywords_capitalized_lowercase, r)
]

pre_mutation = combinations + keywords_capitalized_lowercase


# Mutate regular, and combined words with leetspeek

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

leet_mutations = []

for word in pre_mutation:
    char_options = []

    for letter in word:
        if letter.lower() in leet_map: 
            char_options.append([letter] + leet_map[letter.lower()]) 
        else:
            char_options.append([letter]) 

    for combo in product(*char_options): 
        leet_mutations.append(''.join(combo))  



# TODO: Mutate regular, and combined words with common mutations (123, !1, 2020, etc...)


def suffix_mutator(wordlist):
    common_suffixes = ['', '1', '12', '123', '1234', '12345', '321', '007','!', '!!', '1!', '!1', '@', '#', '$', '%', '?', '*','123!', '1234!', '1@3', '/1']
    suffix_words = []
    for word in wordlist:
        for suffix in common_suffixes:
            suffix_words.append(word + suffix)
    return suffix_words

def prefix_mutator(wordlist):
    common_prefixes = ['', '!', '@', '#', '$', '%', '*', '1', '0']
    prefix_words = []
    for word in wordlist:
        for prefix in common_prefixes:
            prefix_words.append(prefix + word)
    return prefix_words
