import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL = "oliverguhr/spelling-correction-english-base"

tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL)
model.eval()


def correct(texts: list[str], max_new_tokens: int = 128) -> list[str]:
    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
    with torch.inference_mode():
        outputs = model.generate(**inputs, max_new_tokens=max_new_tokens)
    return tokenizer.batch_decode(outputs, skip_special_tokens=True)


def normalize(text):
    return text.lower().strip('.!?" ')


def check(sentence, correction):
    return normalize(sentence) == normalize(correction)


def spell_check(input_text, rowid):
    output = correct(input_text)
    corrected_text = output[0]
    if not check(corrected_text, input_text):
        return corrected_text
    return None


def spell_check_print(input_text, rowid):
    corrections = spell_check(input_text, rowid)
    if corrections:
        print(f"{rowid}\t{input_text} -> {corrections}")
    else:
        print(f"{rowid}\t{input_text} -> <no correction>")
