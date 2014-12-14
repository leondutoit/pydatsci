
### Handling errors

#### Exception handling

Suppose we have a function, like before, that tests whether a number is even or not.

```python
def is_even(num):
    if num % 2 == 0:
        return True
    else:
        return False

is_even(8)
is_even(1.1)
is_even('not a number...')
```

If the function is passed a string as a parameter it cannot perform the logic we intend it to - the function throws an exception: `TypeError: not all arguments converted during string formatting`. Functions often receive inputs from sources that are beyond our control and we need to decide what to do when errors arise from bad input data. Is it alright to simply notify the runner of the program that something failed and then continue? Should the program halt? In python such decisions are made by handling exceptions. How we handle them depends on the case.

Let's consider a simple use case: the program gets a list of data, that can contain integers and strings, and we are interested in whether the integers are even or odd. We need to decide how to respond when getting a string.

```python
input_data = [1, 2, 3, 4, 5, 'hello', 10, '...', 8]

def is_even2(num):
    try:
        if num % 2 == 0:
            return True
        else:
            return False
    except TypeError:
        print "Found non-numerical input, returning None"
        return None

map(is_even2, input_data)
```

In this case we get a list containing `True`, `False` or `None` and a notification that a non-numeric input was found. Instead of the program exiting with an error we specify how we want to handle the specific error and continue accordingly. We will see more of this throughout.

#### Unit testing

In the example python program covered on day 1 we read command line arguments into a list, inserted spaces between words, added an exclamation mark before printing a string to the console. Part of making robust software is writing tests to make sure functions and larger unit of code operate as expected. We can write simple unit tests for the functions in the example program and run them with `nosetests`.

```python
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

```

We can run this as follows: `cd pydatsci/examples && nosetests`. These are overly simplistic tests and not complete enough, but they illustrate the point well enough.

### Data manipulation with pandas

Series
DataFrame
file reading/writing
sql interaction
datatypes
new cols
Groupby
aggregation 
merge
pivot

### A Flask web app

serve a html file
