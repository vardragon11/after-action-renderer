import re
from collections import defaultdict
from pprint import pprint

class Tokenizer:

    # Define the keyword labels we want to tokenize by
    KEYWORDS = ['Title', 'Description', 'Unit', 'Feature', 'Objective', 'Event']

    def tokenize_by_keyword(text: str):
        text = text.replace("minus", "-")  # Normalize voice-to-text quirks
        pattern = r'\b(' + '|'.join(KEYWORDS) + r')\b(?:\s+is)?'
        tokens = re.split(pattern, text)

        # re.split gives us a list like: ['', 'Title', ' Operation X.', 'Unit', ' ID equals ...', ...]
        # We need to stitch it back together as {keyword: [chunks]}
        data = defaultdict(list)

        current_key = None
        for token in tokens:
            token = token.strip()
            if not token:
                continue
            if token in KEYWORDS:
                current_key = token
            elif current_key:
                data[current_key].append(token)

        return data

    # Run the tokenizer
    #tokenized_data = tokenize_by_keyword(voice_text)

    # Pretty print the result
    #pprint(dict(tokenized_data))
    # for item in tokenized_data['Unit']:
    #   print(item)