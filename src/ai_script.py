import random

def generate_script():
    hooks = [
        "You won’t believe this...",
        "This will change how you think forever...",
        "Most people don’t know this trick...",
        "Watch this before it goes viral..."
    ]

    facts = [
        "Your brain processes visuals 60,000x faster than text.",
        "90% of people fail because they ignore consistency.",
        "Small habits can change your entire life in 30 days.",
        "Focus beats talent when talent doesn’t focus."
    ]

    endings = [
        "Follow for more viral insights.",
        "This is why consistency wins.",
        "Try this today and see the difference."
    ]

    script = f"""
{random.choice(hooks)}

{random.choice(facts)}

{random.choice(endings)}
"""
    return script
