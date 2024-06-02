from transformers import pipeline

# https://huggingface.co/oliverguhr/spelling-correction-english-base
# pip install tf-keras

corrector = pipeline("text2text-generation", model="oliverguhr/spelling-correction-english-base")


def normalize(text):
    return text.lower().strip('.!?" ')


def check(sentence, correction):
    return normalize(sentence) == normalize(correction)


def spell_check(input_text, rowid):
    output = corrector(input_text, max_length=2048)
    corrected_text = output[0]["generated_text"]
    if not check(corrected_text, input_text):
        return corrected_text
    return None


def spell_check_print(input_text, rowid):
    corrections = spell_check(input_text, rowid)
    if corrections:
        print(f"{rowid}\t{input_text}\t{corrections}")


if __name__ == '__main__':
    spell_check_print("lets do a comparsion", 0)
    spell_check_print("I love to code in Pyhton.", 0)
    spell_check_print("Ths sentence has some misspeld words.", 0)
    spell_check_print("Screw you kuys, I am going home.", 1)
    spell_check_print("on one side of the island was a hugh rock, almost detached", 11595)
    spell_check_print("The glass was opacified more greater privacy", 11682)
    spell_check_print("in collee she minored in mathematics", 12111)
    spell_check_print("The scientists had to accommodate the new results with the existing theories", 10184)