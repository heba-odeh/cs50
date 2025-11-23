import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S

NP -> N | Det N | Det AP N | NP PP
AP -> Adj | Adj AP
VP -> V | V NP | V PP | V NP PP | VP Adv | Adv VP
PP -> P NP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():
    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()
        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.leaves()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Lowercase and remove any word without an alphabetic character.
    """
    nltk.download("punkt", quiet=True)
    nltk.download("punkt_tab", quiet=True)  # Fix for newer NLTK versions

    from nltk.tokenize import word_tokenize
    words = word_tokenize(sentence.lower())
    return [w for w in words if any(c.isalpha() for c in w)]


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is a NP subtree that does not contain other NP subtrees.
    """
    chunks = []
    for subtree in tree.subtrees(lambda t: t.label() == "NP"):
        if not any(child.label() == "NP" for child in subtree.subtrees(lambda t: t != subtree and t.label() == "NP")):
            chunks.append(subtree)
    return chunks


if __name__ == "__main__":
    main()

