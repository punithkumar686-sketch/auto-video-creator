import random

def generate_script():
    hooks = [
        "Only 1% can solve this!",
        "Try this in 3 seconds!",
        "Are you smarter than most?"
    ]

    questions = [
        ("47 + 38 = ?", "85"),
        ("15 × 6 = ?", "90"),
        ("100 - 29 = ?", "71")
    ]

    hook = random.choice(hooks)
    q, a = random.choice(questions)

    return f"{hook}\n\n{q}\n\nAnswer: {a}"
