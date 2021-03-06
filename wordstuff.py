import operator
import pandas as pd
from scipy import stats as sstats

csvSave = 'csv/'


def main():
    words = get_words()
    # len_statistics(words)
    distribution(words)
    # use_of_letters(words)
    # entropy_of_words_based_on_lengths(words)
    # compound_Words(words)
    # vokals_consonant_relationship(words)
    # vokal_consonant_by_length_rel(words)


def vokal_consonant_by_length_rel(words):
    longestWordLen = len(max(words, key=len))
    len_dict = {}
    for x in range(1, longestWordLen):
        len_dict[x] = [[get_relationship(word)[0], get_relationship(word)[3]]
                       for word in words if len(word) == x]
    stats = {}
    for k, v in len_dict.items():
        stats[k] = sum([word[1] for word in v])/len(v)

    with open(f'{csvSave}vkrel.csv', 'w') as file:
        file.write('length;averagerel\n')
        for key, value in stats.items():
            value = str(value).replace('.', ',')
            file.write(f'{key};{value}\n')


def get_relationship(word):
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'x', 'y',
                'z', 'æ', 'ø', 'å']
    vokals = ['a', 'e', 'i', 'o', 'u', 'y', 'æ', 'ø', 'å']
    consonants = [letter for letter in alphabet if letter not in vokals]
    chars = [letter for letter in word]
    c = len([consonant for consonant in chars if consonant in consonants])
    v = len([vokal for vokal in chars if vokal in vokals])
    if c == 0 or v == 0:
        rel = 0
    elif c > v:
        rel = round(c/v, 2)
    else:
        rel = round(v/c, 2)
    return [word, c, v, rel]


def vokals_consonant_relationship(words):
    rich_words = []

    for word in words:
        rich_words.append(get_relationship(word))

    sorted_list = sorted(rich_words, key=operator.itemgetter(3))
    top10 = sorted_list[-10:]
    for w in top10:
        print(f'Word: {w[0]}, Consonants: {w[1]}, \
                Vocals: {w[2]}, Ratio: {w[3]}')


def compound_Words(words):
    # roots = []
    # compounds = []
    # regex = '([\w-]*{word}[\w-]*)'
    # for xword in words:
    #     r = re.compile(regex.format(word=xword))
    #     compounds = list(filter(r.match, words))
    compounds = []
    for xword in words:
        for yword in words:
            if xword in yword:
                compounds.append([xword, yword])
    compounds = list(set(compounds))
    print(compounds)


def entropy_of_words_based_on_lengths(words):
    word_len = {}
    entropy_words = {}
    longestWordLen = len(max(words, key=len))

    for x in range(1, longestWordLen):
        word_len[x] = [
            [word, entropy(word)] for word in words
            if len(word) == x]
    for key, value in word_len.items():
        average = sum([entropy[1] for entropy in value])/len(value)
        entropy_words[key] = average
    with open(f'{csvSave}entropyFile.csv', 'w') as entropyFile:
        entropyFile.write('Length;entropy\n')
        for key, value in entropy_words.items():
            entropyFile.write('{length};{entropy}\n'
                              .format(length=key, entropy=str(value)
                                      .replace('.', ',')))


def use_of_letters(words):
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'x', 'y',
                'z', 'æ', 'ø', 'å']
    use_of_letters = {}
    for letter in alphabet:
        letterUsed = [word.count(letter) for word in words if letter in word]
        use_of_letters[letter] = sum(letterUsed)
    with open(f'{csvSave}letterDist.csv', 'w') as letterDistFile:
        letterDistFile.write('letter,count\n')
        for key, value in use_of_letters.items():
            letterDistFile.write(f'{key},{value}\n')


def distribution(words):  # Distributionen af æøå ord i ordlisten
    dist = {}
    letters = ['æ', 'ø', 'å']
    combos = [['æ', 'ø', 'å'], ['æ', 'å', 'ø'], ['å', 'ø', 'æ']]
    # TODO: Make it less switch like and maybe more scalable.
    for x in range(0, len(letters)):
        dist[letters[x]] = len([word for word in words
                                if letters[x] in word
                                and letters[x-1] not in word
                                and letters[x-2] not in word])
    for x in range(0, len(combos)):
        dictName = ''.join(combos[x][:2])
        dist[dictName] = len([word for word in words
                              if combos[x][0] in word
                              and combos[x][1] in word
                              and combos[x][2] not in word])
    dist['æøå'] = len([word for word in words
                       if 'æ' in word
                       and 'ø' in word
                       and 'å' in word])

    dist['other'] = len([word for word in words
                         if 'æ' not in word
                         and 'ø' not in word
                         and 'å' not in word])

    dist['all'] = sum([value for key, value in dist.items()])

    with open(f'{csvSave}charDist.csv', 'w') as charDistFile:
        charDistFile.write('letter,count\n')
        for key, value in dist.items():
            charDistFile.write(f'{key},{value}\n')


def len_statistics(words):  # Distributionen af ordlængder
    longestWordLen = len(max(words, key=len))
    lenStats = {}
    for x in range(1, longestWordLen):
        y = len([word for word in words if len(word) == x])
        lenStats[x] = y
    with open(f'{csvSave}length.csv', 'w') as lengthFile:
        lengthFile.write('length,amount\n')
        for key, value in lenStats.items():
            lengthFile.write(f'{key},{value}\n')


def get_words():
    with open('words.txt', 'r') as wordfile:
        tempWords = wordfile.readlines()
        words = [word.strip() for word in tempWords]
    return words


def entropy(s):
    # Shannon algortithm
    series = pd.Series([letter for letter in s])
    counts = series.value_counts()
    entropy = sstats.entropy(counts)
    return entropy


if __name__ == "__main__":
    main()
