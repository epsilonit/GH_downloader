import re


def remove_headers_footers(text, header_patterns=None, footer_patterns=None):
    if header_patterns is None:
        header_patterns = [r'^.*Header.*$']
    if footer_patterns is None:
        footer_patterns = [r'^.*Footer.*$']
    for pattern in header_patterns + footer_patterns:
        text = re.sub(pattern, '', text, flags=re.MULTILINE)
    return text.strip()


def remove_special_characters(text, special_chars=None):
    if special_chars is None:
        special_chars = r'[^A-Za-z0-9\s\.,;:\'\"\?\!\-]'
    text = re.sub(special_chars, '', text)
    return text.strip()


def remove_repeated_substrings(text, pattern=r'\.{2,}'):
    text = re.sub(pattern, '.', text)
    return text.strip()


def remove_extra_spaces(text):
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def remove_emojis(text):
    emoji = re.compile("["
                       u"\U0001F600-\U0001F64F"  # emoticons
                       u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                       u"\U0001F680-\U0001F6FF"  # transport & map symbols
                       u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                       u"\U00002500-\U00002BEF"  # chinese char
                       u"\U00002702-\U000027B0"
                       u"\U000024C2-\U0001F251"
                       u"\U0001f926-\U0001f937"
                       u"\U00010000-\U0010ffff"
                       u"\u2640-\u2642"
                       u"\u2600-\u2B55"
                       u"\u200d"
                       u"\u23cf"
                       u"\u23e9"
                       u"\u231a"
                       u"\ufe0f"  # dingbats
                       u"\u3030"
                       "]+", re.UNICODE)
    return re.sub(emoji, '', text)


def remove_username(text):
    text = re.sub(' @[^\s]+', '', text)
    text = re.sub('[\r\n]+@[^\s]+','', text)
    text = re.sub('^@[^\s]+', '', text)
    return text.strip()


def preprocess_text(text):
    # Remove headers and footers
    # text = remove_headers_footers(text)
    # Remove special characters
    # text = remove_special_characters(text)
    # Remove repeated substrings like dots
    # text = remove_repeated_substrings(text)
    # Remove extra spaces between lines and within lines
    # text = remove_extra_spaces(text)
    # Additional cleaning steps can be added here
    text = remove_emojis(text)
    text = remove_username(text)
    return text.strip()
