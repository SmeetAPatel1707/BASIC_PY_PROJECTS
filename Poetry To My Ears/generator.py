from abc import ABC, abstractmethod
import random
import unittest
from kgram import build_kgram_model

# ----------------[Step - 1 implementation (Implement Base Class)]----------------------|
class TextGenerator(ABC):
    '''
    Thi sclass is abstract base class for all poetry generators.

    It manages : raw input text
                 k-gram size
                 k-gram model
    '''

    def __init__(self, text:str, k:int):
        '''
        Initialises the text generator.

        Parameters:
            text(str): The raw input text.
            k(int): The k-gram size.
        '''
        self.text = text
        self.k = k

        # Build and store the k-gram model
        self.model = build_kgram_model(self.text, self.k)

# ----------------[Step - 2 implementation (Access Next Word Options)]-------------------|
    def get_next_options(self, kgram: tuple) -> dict:
        '''
        It returns the possible next tokens for a given k-gram.

        Parameters:
            kgram(tuple): The k-gram to search for.
        
        Returns:
            dict: A dictionary containing next tokens and their frequency counts.
            it returns an empty dictionary while kgram doesn't exist in the model.
        '''

        # Check whether the k-gram exists
        if kgram in self.model:
            return self.model[kgram]

        # return empty if missing
        return {}

# ----------------[Step - 3 implementation (Define the Token Selection Interface)]-------------------|
    @abstractmethod
    def choose_next_token(self, options: dict) -> str:
        '''
        It selects the next token from the available options.

        Parameters:
            options (dict): Dictionary contains possible next 
            tokens and their corrosponding frequency units.

        Returns:
            str : The selected next token.
        '''
        pass

# ----------------[Step - 4 implementation (Generate Text Using Recursion)]-------------------|
    # Helper Function - 1
    def _generate_recursive(self, current_kgram: tuple, current_tokens: list, max_tokens: int) -> list:
        '''
        Recursively generates tokens for the poem.

        Parameters:
            current_kgram(tuple):Current k-gram context.
            current_kgram(list):Tokens generated so far.
            max_tokens(int):Maximum allowed token count.

        Returns:
            list: List of generated tokens.
        '''
        # Stop if maximum token count is reached.
        if len(current_tokens) >= max_tokens:
            return current_tokens

        
        # Get the possible next token options
        options = self.get_next_options(current_kgram)

        if options == {}:
            return current_tokens

        # Select the next_token
        next_token = self.choose_next_token(options)

        # Stop if END token is reached
        if next_token == "<END>":
            return current_tokens

        current_tokens.append(next_token)

        # Build next k-gram 
        next_kgram = tuple(current_tokens[-self.k:])

        return self._generate_recursive(next_kgram, current_tokens, max_tokens)

    def generate(self, start_kgram: tuple, max_tokens: int) -> str:
        '''
        Generates text Recursively using the k-gram model.

        Parameters:
            start_kgram(tuple): Starting k-gram for generation.
            max_tokens(int):Maximum number of tokens to generate.

        Returns:
            str: The generated formatted text.

        Raises:
            ValueError: Raised for invalid inputs.
        '''

        # Validating a type of start_kgram
        if not isinstance(start_kgram, tuple):

            raise ValueError(f"start_kgram must be a tuple.")

        # Validate k-gram length it must be same as k
        if len(start_kgram) != self.k:

            raise ValueError(f"start_kgram length must be match k.")

        # max_tokens validation
        if max_tokens < self.k:

            raise ValueError(f"max_tokens must be grater than or equal to k.")

        # Validate starting k-gram existance
        if start_kgram not in self.model:

            raise ValueError(f"start_kgram does not exist in the model.")

        generated_tokens = list(start_kgram)

        # Generate reamining tokens
        generated_tokens = self._generate_recursive(start_kgram, generated_tokens, max_tokens)

        # If present "END", remove it.
        tokens_cleaned = []
        for token in generated_tokens:

            if token != "<END>":
                tokens_cleaned.append(token)

        generated_text = " ".join(tokens_cleaned)

        # Remove spaces that having before punctuation
        generated_text = generated_text.replace(" ,", ",")
        generated_text = generated_text.replace(" .", ".")

        # First character must be capital
        if generated_text != "":
            generated_text = (generated_text[0].upper() + generated_text[1:])

        # Capitalise after periods
        sentence_parts = generated_text.split(". ")
        capitalised_sentences = []
        for part in sentence_parts:

            if part != "":
                formatted_sentence = (part[0].upper() + part[1:])
                capitalised_sentences.append(formatted_sentence)

        generated_text = ". ".join(capitalised_sentences)

        return generated_text

# ----------------[Step - 5 implementation (Dynamic Model Updates)]-------------------|

    def rebuild_model(self) -> None:
        '''
        Rebuilds the internal k-gram model using the current 
        text and k-value.
        '''
        self.model = build_kgram_model(self.text, self.k)
    
    def update_k(self, new_k: int) -> None:
        '''
        Updates the value of k and rebuilds the model based on it.
        
        Parameters:
            new_k(int): The size of new k-gram.
        '''

        # Validate type of new k
        if not isinstance(new_k, int):
            raise TypeError("new_k must be an integer.")

        # Validate value of k
        if new_k <= 0:
            raise ValueError("new_k must be grater then zero.")

        self.k = new_k
        self.rebuild_model()

    def add_poem(self, new_poem: str) -> None:
        '''
        Adds a new poem to the existing text and rebuilds the model.
        
        Parameters:
            new_poem(str): The poem to append.
        '''
        if not isinstance(new_poem, str):
            raise TypeError("new_poem must be a string.")
        
        if new_poem.strip()=="":
            raise ValueError("new_poem can not be empty.")

        # add seperator before append
        self.text += "\n" + new_poem
        self.rebuild_model()


# ----------------[Step - 6 implementation (Implement Subclasses)]-------------------|

class DeterministicGenerator(TextGenerator):
    '''
    This class helps to generate text deterministically using the 
    highest-frequescy token.
    '''

    def choose_next_token(self, options: dict) -> str:
        '''
        Selects the next token with the highest frequency.
        If frequencies as same as highest on,then token are sorted by alphabatic order.

        Parameters:
            options(dict): Dictionary containing tokens and their frequency counts.
        
        Returns: 
            str: Selected token.
        '''
        # Store the founded highest frequency
        highest_freq = max(options.values())

        candidate_tokens = []

        for token, frequency in options.items():
            if frequency == highest_freq:
                candidate_tokens.append(token)

        # Sort tokens alphabatically
        candidate_tokens.sort()

        # Return first alphabetical token
        return candidate_tokens[0]

class RandomGenerator(TextGenerator):
    '''
    Generates text by using a weighted random token selection.
    '''
    def choose_next_token(self, options:dict) -> str:
        '''
        It selects the next token randomly by using frequescy counts as weights.

        Parameters:
            options (dict): All pair of tokens and frequencies in the form of key-value pair.

        Returns:
            str: selected token.
        '''
        token_choices = []
        token_weights = []

        # Seperate tokens and frequencies
        for token, frequency in options.items():
            token_choices.append(token)
            token_weights.append(frequency)

        # Selecting one token using weights
        selected_token = random.choices(token_choices, weights = token_weights, k = 1)[0]

        return selected_token

class HaikuGenerator(RandomGenerator):
    '''
    It generates a simple haiku-style poem through 5-7-5 token structure.
    '''

    def generate_poem(self)-> str:
        '''
        Generates a 3-line haiku.

        Returns: 
            str : Three-line poem
        '''

        line_lengths = [5,7,5]
        poem_lines = []

        # Generate each line seperatly
        for line_length in line_lengths:

            # Select a random starting by kgram model
            start_kgram = random.choice(list(self.model.keys()))

            line = self.generate(start_kgram, line_length)

            # Remove stray punctuation
            line = line.strip(" .,")

            # Remove <END> Token if present.
            line = line.replace("<END>", "")

            # Remove extra spaces
            line = line.strip()

            poem_lines.append(line)

        # combine poem lines
        complete_poem = "\n".join(poem_lines)

        return complete_poem

class AcrosticPoemGenerator(RandomGenerator):
    '''
    This class helps to generating an acrostic poem, 
    where the first letter of each line follows the 
    provided keyword.  
    '''

    def __init__(self, text: str, k: int, keyword: str) -> None:
        '''
        Initializes the acrostic generator.
        Parameters: 
            text(str): Raw input text.
            k (int): K-gram size.
            keyword (str): Word used for acrostic.
        '''

        # Inintalize parent class
        super().__init__(text, k)

        # Store keyword in lower case 
        self.keyword = keyword.lower()

    def generate_poem(self) -> str:
        '''
        Generates an acrostic poem.

        Returns: 
            str: Generated acrostic poem or fallback message.
        '''

        poem_lines = []

        for letter in self.keyword:

            matching_kgrams = []

            for kgram in self.model.keys():

                # Check first token of kgram
                first_word = kgram[0]

                if first_word.startswith(letter):
                    matching_kgrams.append(kgram)

            # Return fallback if no match exists
            if len(matching_kgrams) == 0:

                return ("Unable to generate acrostic poem for the given keyword.")
            
            # Select one matching poem randomly
            selected_kgram = random.choice(matching_kgrams)

            # Generate approximately 6 tokens
            line = self.generate(selected_kgram, 6)

            # Remove stray punctuation
            line = line.strip(" .,")

            # Remove <END> Token if present.
            line = line.replace("<END>", "")

            # Remove extra spaces
            line = line.strip()

            # Store completed line
            poem_lines.append(line)
        
        # Join lines into complete poem
        complete_poem = "\n".join(poem_lines)

        return complete_poem

# ----------------[Step - 7 implementation (Unit Testing)]-------------------|

class TestQuestion2(unittest.TestCase):

    def test_generation_logic(self):

        sample_text = '''
        1
        the bird sings.

        2
        the bird files.
        '''
        generator = DeterministicGenerator(sample_text, 2)

        generated_text = generator.generate(("the", "bird"), 5)

        self.assertTrue(len(generated_text.split()) <= 5)

        self.assertNotIn("<END>", generated_text)

    def test_subclass_behaviour(self):

        sample_text = '''
        1
        moon stars.
        '''

        options = {
            "moon": 2,
            "stars": 2,
            "sun": 1
        }

        deterministic = DeterministicGenerator(sample_text, 1)

        selected_token = deterministic.choose_next_token(options)

        self.assertEqual(selected_token, "moon")

        random_generator = RandomGenerator(sample_text, 1)

        random_result = random_generator.choose_next_token(options)

        self.assertIn(random_result, options)

    def test_specialised_poems(self):
        sample_text = '''
        1
        the bird sings softly.

        2
        stars shine brightly.
        '''

        haiku = HaikuGenerator(sample_text, 1)
        haiku_poem = haiku.generate_poem()

        self.assertEqual(len(haiku_poem.split("\n")), 3)

        acrostic = AcrosticPoemGenerator(sample_text, 1, "ts")

        acrostic_poem = acrostic.generate_poem()

        self.assertEqual(len(acrostic_poem.split("\n")), 2)

    def test_formatting_and_cleanup(self):
        sample_text ='''
        1
        the bird sings.
        '''

        generator = DeterministicGenerator(sample_text, 2)
        generated_text = generator.generate(("the", "bird"), 5)

        self.assertNotIn(" ,", generated_text)
        self.assertNotIn(" .", generated_text)
        self.assertNotIn("<END>", generated_text)
        self.assertTrue(generated_text[0].isupper())

    def test_dynamic_updates(self):

        sample_text = '''
        1
        the bird sings.
        '''

        generator = DeterministicGenerator(sample_text, 1)
        original_k = generator.k

        generator.update_k(2)

        self.assertNotEqual(original_k, generator.k)

        generator.add_poem("new poem added")

        self.assertIn("new poem added", generator.text)

    def test_invalid_inputs(self):

        sample_text = '''
        1
        the bird sings.
        '''

        generator = DeterministicGenerator(sample_text, 2)

        # Errors occured due to generation...
        with self.assertRaises(ValueError):
            generator.generate("not_tuple", 5)

        with self.assertRaises(ValueError):
            generator.generate("the", 5)

        with self.assertRaises(ValueError):
            generator.generate(("the", "bird"), 1)
        
        # Errors occured by update_k
        with self.assertRaises(TypeError):
            generator.update_k("two")
        
        with self.assertRaises(ValueError):
            generator.update_k(0)

        with self.assertRaises(ValueError):
            generator.update_k(-1)

        # Errors occured by add_poem
        with self.assertRaises(TypeError):
            generator.add_poem(123)
        
        with self.assertRaises(ValueError):
            generator.add_poem("")

        with self.assertRaises(ValueError):
            generator.add_poem("   ")


if __name__=="__main__":
    unittest.main()


