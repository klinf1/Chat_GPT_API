import tiktoken


def find_string(text: str):
    if text:
        return text.find('<&>', text.find('<&>')+1)


def cut_string_beginning(text: str):
    if text:
        return text[find_string(text):]


def cut_string_end(text: str):
    if text:
        return text[:find_string(text)]


def get_token_count(string):
    encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')
    return len(encoding.encode(string))
