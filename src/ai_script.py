import random

def generate_script():

    hooks = [
        "Can you solve this in 3 seconds?",
        "Only smart people can solve this fast!",
        "Try this brain trick!",
    ]

    problems = [
        (47, 25),
        
    ]

    a, b = random.choice(problems)

    # smart trick logic
    rounded = ((a // 10) + 1) * 10
    add = rounded + b
    diff = rounded - a
    answer = add - diff

    script = f"""
{random.choice(hooks)}

Try this:
{a} + {b}

Instead of adding normally…
Add {rounded} + {b} = {add}

Then subtract {diff} → {answer}

Boom! Faster than your teacher!

Follow for more brain tricks!
"""

    return script
