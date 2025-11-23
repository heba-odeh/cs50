from logic import *

# Symbols
AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")
# I have to add these, otherwise model_check can't see the full information
# We need to explicitly represent what A might have said so the logic can reason about both possibilities
A_said_knight = Symbol("A said 'I am a Knight'")
A_said_knave = Symbol("A said 'I am a Knave'")



# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    Implication(AKnight, And(AKnight, AKnave)),
    Implication(AKnave, Not(And(AKnight, AKnave)))
)


# Puzzle 1
# A says "We are both knaves."
knowledge1 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave)))
)


# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # A says same kind
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),

    # B says different kind
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    Implication(BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight))))
)


# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
 # A is either knight or knave
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # B
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # C
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),

    # A said either "I am a knight" or "I am a knave"
    Or(A_said_knight, A_said_knave),
    Not(And(A_said_knight, A_said_knave)),

    # If A said "I am a knight", then:
    Implication(A_said_knight,
        And(
            Implication(AKnight, AKnight),
            Implication(AKnave, Not(AKnight))
        )
    ),

    # If A said "I am a knave", then:
    Implication(A_said_knave,
        And(
            Implication(AKnight, AKnave),
            Implication(AKnave, Not(AKnave))
        )
    ),

    # B says: A said "I am a knave"
    Implication(BKnight, A_said_knave),
    Implication(BKnave, Not(A_said_knave)),

    # B says: "C is a knave"
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),

    # C says: "A is a knight"
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight))
)


# List of all puzzles
puzzles = [
    ("Puzzle 0", knowledge0),
    ("Puzzle 1", knowledge1),
    ("Puzzle 2", knowledge2),
    ("Puzzle 3", knowledge3)
]


def main():
    for name, knowledge in puzzles:
        print(name)
        for symbol in [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]:
            if model_check(knowledge, symbol):
                print(f"    {symbol}")
        print()


if __name__ == "__main__":
    main()

