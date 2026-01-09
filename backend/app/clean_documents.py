import re

def clean_text(text: str) -> str:
    text = text.replace("\u00a0", " ")
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = text.strip()
    return text


def clean_documents(texts):
    cleaned = []
    for t in texts:
        cleaned.append(clean_text(t))
    return cleaned
