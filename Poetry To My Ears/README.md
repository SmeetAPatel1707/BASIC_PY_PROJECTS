# 📝 K-Gram Poetry Generator

A Python implementation of a **K-Gram Language Model** that learns writing patterns from a collection of poems and generates new poetry-like text.

This project is divided into two stages:

1. **Build a K-Gram language model** from raw text.
2. **Extend the model using Object-Oriented Programming (OOP)** to generate poems with different strategies.

---

# 📌 Features

## Question 1 – K-Gram Language Model

### Text Processing

- Read poems from a text file
- Handle missing or empty files with proper exceptions
- Convert text to lowercase
- Remove punctuation except:
  - `,`
  - `.`
- Split poems using numeric identifiers
- Tokenize text into words and punctuation
- Append a special `<END>` token after each poem

### K-Gram Model

Builds a dictionary-based language model where:

```python
(k-gram) -> {next_token: frequency}
```

Example:

```python
{
    ("the", "moon"): {
        "shines": 2,
        "is": 1
    }
}
```

### Model Query

Retrieve all possible next tokens for any valid k-gram.

### Error Handling

The implementation validates:

- Invalid file paths
- Empty files
- Invalid text input
- Invalid k values
- Invalid model construction

### Unit Tests

Includes tests for:

- Text cleaning
- Model construction
- Invalid inputs
- File handling

---

# 🚀 Question 2 – Object-Oriented Poetry Generator

Transforms the K-Gram model into a reusable text generation framework.

## Base Class

### `TextGenerator`

Responsibilities:

- Store raw text
- Build the K-Gram model
- Generate text recursively
- Manage model updates

Features:

- Recursive text generation
- Automatic formatting
- Capitalization handling
- Punctuation cleanup
- Dynamic model rebuilding

---

# 🏗 Generator Classes

## DeterministicGenerator

Always selects the **most frequent** next token.

Tie-breaking:

- Alphabetical order

---

## RandomGenerator

Randomly selects the next token using weighted probabilities based on token frequency.

Uses:

```python
random.choices()
```

---

## HaikuGenerator

Generates three-line poems using an approximate:

```
5 Tokens
7 Tokens
5 Tokens
```

Each line begins from a randomly selected starting k-gram.

---

## AcrosticPoemGenerator

Generates poems where the first letter of every line spells a chosen keyword.

Example:

```
PYTHON
```

Produces:

```
P...
Y...
T...
H...
O...
N...
```

---

# 🔄 Dynamic Model Updates

Supports rebuilding without creating a new object.

Methods include:

- `rebuild_model()`
- `update_k()`
- `add_poem()`

---

# 📂 Project Structure

```text
.
├── sample_text.txt
├── question1.py
├── question2.py
├── tests.py
├── README.md
└── requirements.txt
```

---

# ⚙️ Requirements

- Python 3.10+
- Standard Library only

Modules used:

- `re`
- `random`
- `collections`
- `abc`
- `unittest`

---

# ▶️ Example

Input:

```
The bird sings.
The moon shines.
```

Generated Output:

```
The bird sings.
The moon shines softly.
```

(Output varies depending on the generator.)

---

# 🧪 Testing

Run all unit tests:

```bash
python -m unittest
```

or

```bash
python -m unittest discover
```

---

# 📚 Concepts Demonstrated

- Natural Language Processing (NLP)
- K-Gram Language Models
- Tokenization
- Recursive Algorithms
- Object-Oriented Programming
- Abstract Base Classes (ABC)
- Probability-Based Text Generation
- Unit Testing
- Exception Handling
- Python Data Structures

---

# 🎯 Learning Outcomes

This project demonstrates how a simple statistical language model can:

- Learn token sequences from text
- Predict likely next tokens
- Generate poetry-like sentences
- Apply OOP design principles for extensibility
- Support multiple text-generation strategies while sharing a common language model

---

## 📄 License

This project was developed for educational purposes as part of a university programming assignment.
