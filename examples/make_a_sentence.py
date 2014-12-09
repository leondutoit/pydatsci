from sys import argv

def make_annoying_sentence(words):
    """Takes a list of words, turns them into
    annoying all caps and inserts spaces between words"""
    sentence = []
    for word in words:
        sentence.append(word.upper())
        sentence.append(' ')
    return sentence

def exclaim(sentence):
    """Adds an exclamation mark to the sentence list"""
    sentence.append('!')
    return ''.join(sentence)

def main():
    inputs = argv[1:]
    print exclaim(make_annoying_sentence(inputs))

if __name__ == '__main__':
    main()
