start_token = "*start*"
end_token = "*end*"


def not_empty(string):
    return bool(string)


def format_sentence(sentence):
    return start_token + " " + sentence.strip() + " " + end_token


def format_word(word):
    return word.strip().lower() \
        .replace(' ', '') \
        .replace('"', '') \
        .replace('[', '') \
        .replace(']', '')
