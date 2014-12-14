from make_a_sentence import make_annoying_sentence, exclaim

def test_make_annoying_sentence():
    """Test that words are converted to upper case and that spaces are inserted"""
    sample_words = ['hello', 'there']
    sentence = make_annoying_sentence(sample_words)
    correct_sentence = ['HELLO', ' ', 'THERE', ' ']
    assert(sentence == correct_sentence)

def test_exclaim():
    """Test that an exclamation mark is added to a sentence"""
    with_exclamation = exclaim(['BLA'])
    assert('!' in with_exclamation)
