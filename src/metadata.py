import random

def generate_metadata():

    titles = [
        "99% Fail This Math Trick 😳",
        "Solve This in 3 Seconds! 🔥",
        "This Trick Will Shock You 🤯",
    ]

    hashtags = [
        "#shorts #mathtrick #brainhack #viral",
        "#learnmath #fastmath #shortsviral",
        "#education #maths #trickshot",
    ]

    return {
        "title": random.choice(titles),
        "hashtags": random.choice(hashtags)
    }
