def response(hey_bob: str):
    hey_bob = hey_bob.strip()
    if len(hey_bob) == 0:
        return "Fine. Be that way!"
    if hey_bob.isupper() and hey_bob[-1] == "?":
        return "Calm down, I know what I'm doing!"
    elif hey_bob[-1] == "?":
        return "Sure."
    elif hey_bob.isupper():
        return "Whoa, chill out!"
    return "Whatever."
