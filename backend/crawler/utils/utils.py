import re
def pre_process_text(text, max_len=100):
    if not text: return ""
    split_text = re.split(r"\s+", text)
    filtered_text = [word for word in split_text if word.isalnum()]
    new_text = " ".join(filtered_text)
    if len(new_text) > max_len:
        new_text = new_text[:max_len]
    return new_text