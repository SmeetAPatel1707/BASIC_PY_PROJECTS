import re

# For unit testing and text processing...
import unittest
import tempfile
import os

def read_text(file_path: str) -> str:
    '''
    This function reads a text file and returns its contents as a string.
    Parameters: 
        file_path (str): The actual path to the text file.
    Returns:
        str: The contents of the file.
    Raises: 
        FileNotFoundError: 
            Raised when the file does not exist.
        ValueError:
            Raised when the file is empty removing whitespace.
    '''
    try:
        # Open the file safely using UTF-8 encoding
        with open(file_path, 'r', encoding="utf-8") as file:

            # Read the entire file content
            file_contents = file.read()

    except FileNotFoundError:
        # Raise the custom error message if the file is missing
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    # Remove leading and trailing whitespace
    cleaned_contents = file_contents.strip()

    # Check whether the file contains valid text.
    if cleaned_contents == "":
        raise ValueError(f"The file is empty and contains no valid text.")
        
    return file_contents

def clean_text(text: str) -> str:
    '''
    This function help us to converting input text into lowercase and remove punctuations,
    except commas and fullstops.
    Parameters: 
        text(str): The raw input text.
    Returns: 
        str: The cleaned text.
    Raises: 
        TypeError:
            Raised when the input text is not a string.
    '''

    # Validate that the input is a string.
    if not isinstance(text, str):
        raise TypeError(f"Input text must be a string.")

    # Converting all text into lowercase
    lowercase_text = text.lower()

    # Remove punctuations except "," and "."
    cleaned_text = re.sub(r"[^a-z0-9\s,.\n]", "", lowercase_text)

    # Replace multiple spaces wuth a single space
    cleaned_text = re.sub(r"[ ]+", " ", cleaned_text)

    return cleaned_text

# Helper Function - 1
def split_poems(text: str) -> list:
    '''
    This method help to split the text into individual poems by using 
    numaric index lines as seperators. Note that it is a helper function.
    Parameters: 
        text(str) : The cleaned text.
    Returns:
        list : A list contains individual poems as strings.
    '''

    # Split the text into seperate lines
    lines = text.splitlines()

    # Store all filtered poems
    poems = []

    # Tamporarily store lines belonging to one poem.
    current_poem_lines = []

    for line in lines:
        line_stripped = line.strip()

        # Check if the line contains only digits
        if line_stripped.isdigit():
            if current_poem_lines:

                # combine lines into one string with removing spaces
                completed_poem = " ".join(current_poem_lines)
                completed_poem = completed_poem.strip()

                # Store them into the poems
                poems.append(completed_poem)

                # reset the list of current_poem_lines for next poem
                current_poem_lines = []

        else:
            # Completely ignore empty lines
            if line_stripped != "":
                current_poem_lines.append(line_stripped)

    # To add the final poem if exists
    if current_poem_lines:

        # Follow same as done before.
        completed_poem = " ".join(current_poem_lines)
        completed_poem = completed_poem.strip()
        poems.append(completed_poem)

    return poems


# Helper function -2 
def tokenize_poem(poem:str) -> list:
    '''
        This function converts each poem's word, commas, fullstops into the individual tokens.
        It is also the helper function.

        Rules:
        > Words become tokens
        > Commas become seperate tokens
        > Full stops become seperate tokens

        Parameters:
            poem(str): A single poem as a string.
        Returns:
            list: A list of tokens for the poem.

    '''
    tokens = []

    # find all possible matched items of poem(./,/word)
    tokens_matched = re.findall(r'\w+|[,.]', poem)

    # Add each token individually
    for token in tokens_matched:
        tokens.append(token)
    
    # Put mark the end of the poem
    tokens.append("<END>")

    return tokens

# Main logic brain of entire program
def build_kgram_model(text: str, k: int) -> dict:
    '''
    This function builds a k-gram model from the given text.

    Parameters: 
        text(str): The raw input text.
        k(int): The size of the k-gram.
    Returns:
        dict: A dictionary representing the k-gram model.
    Raises:
        TypeError:
            Raised when text is not a string.
            or k is not an integer.
        ValueError:
            Raised when k is less then or equal to 0.
            or when no valid k-grams can be created.
    '''

    # validate text input
    if not isinstance(text, str):
        raise TypeError(f"Text must be a string.")

    # Validate key type
    if not isinstance(k, int):
        raise TypeError(f"The value of k must be integer.")

    # Validate k value
    if k <=0:
        raise ValueError(f"k must be grater then 0.")

    # Clean the row text
    cleaned_text = clean_text(text)

    # Split it into a poems
    poems = split_poems(cleaned_text)

    
    all_tokens = []

    for poem in poems:
        # tokenization
        poem_tokens = tokenize_poem(poem)

        # Add poem tokens into master token list
        all_tokens.extend(poem_tokens)

    # Check whether tokens are exist
    if len(all_tokens) <= k:
        raise ValueError(f"Not enough tokens to build k-grams.")

    # Store the final model of k-grams
    kgram_model = {}

    for index in range(len(all_tokens)-k):

        # extract current k-gram
        current_kgram = tuple(all_tokens[index: index + k])

        next_token = all_tokens[index + k]

        # Create dictionary for new k-gram
        if current_kgram not in kgram_model:
            kgram_model[current_kgram] = {}

        # create counter for next token
        if next_token not in kgram_model[current_kgram]:
            kgram_model[current_kgram][next_token] = 0

        # Increase token frequency counts
        kgram_model[current_kgram][next_token] += 1
    
    return kgram_model

def get_next_token_options(kgram: tuple, model: dict) -> dict:
    '''
    This function returns the possible next tokens for a given kgram.
    Parameters:
        kgram(tuple): The k-gram to search for.
        model(dict): The k-gram model dictionary.
    Returns: 
        dict: A dictionary containing possible next tokens and their frequencies.
    '''

    # Check whether the k-gram exists in th emodel.
    if kgram in model:
        return model[kgram]
    
    # Return empty dictionary if k-gram not found
    return {}
        
# -----------------[ TESTING (INFORMAL) ]------------------

if __name__=='__main__':

    # Sample file path
    file_path = 'sample_text.txt'

    try:
        # read the sample text
        raw_text = read_text(file_path)

        print("File successfully loaded.\n")

        # Building kgram model by using k=2 for testing purpose
        k = 2
        kgram_model = build_kgram_model(raw_text, k)

        print("K-Gram model successfully created.\n")

        # Example k-gram query
        sample_kgram = ("the", "world")

        next_token_options = get_next_token_options(sample_kgram, kgram_model)

        print(f"K-gram: {sample_kgram}")
        print("Next token options:")
        print(next_token_options)

    except Exception as error:

        print(f"Error: {error}")
    
# ------------[ Unit testing for text processing ]---------------

class TestGeneratorFunctions(unittest.TestCase):

    def test_clean_text_logic(self):
        '''
        Verify that clean_text correctly converts text to lowercase, 
        removes unwanted punctuation, and keeps commas and full stops.
        '''

        raw_text = 'Hello! "World": sings,'
        expected_output = 'hello world sings,'

        cleaned_result = clean_text(raw_text)
        self.assertEqual(cleaned_result, expected_output)

    def test_build_model_basic(self):
        '''
        Verify that repeated k-grams correctly update token frequency
        counts.
        '''

        sample_text = '''
        1 
        the bird sings.

        2
        the bird sings.
        '''
        k = 2
        model = build_kgram_model(sample_text, k)

        expected_result = {
            "sings": 2
        }

        actual_result = get_next_token_options(
            ("the", "bird"),
            model
        )

        self.assertEqual(actual_result, expected_result)

    def test_invalid_inputs(self):
        '''
        Verify that correct exceptions are raised for
        invalid inputs.
        '''
        k = 2
        # Invalid text type
        with self.assertRaises(TypeError):
            build_kgram_model(123, 2)

        # Invalid k type
        with self.assertRaises(TypeError):
            build_kgram_model("sample text", "2")

        # Invalid k value
        with self.assertRaises(ValueError):
            build_kgram_model("sample text", 0)

    def test_file_errors(self):
        '''
        Verify that read_text handles missing or empty files.
        '''

        # Test missing file
        with self.assertRaises(FileNotFoundError):
            read_text("missing_file.txt")

        # Create temporary empty file
        temporary_file = tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8")
        temporary_file.close()

        try:
            # Empty file testing
            with self.assertRaises(ValueError):
                read_text(temporary_file.name)
        
        finally:
            # Remove temporary file safely
            os.remove(temporary_file.name)

if __name__=="__main__":
    unittest.main()






