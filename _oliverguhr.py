from transformers import pipeline

# https://huggingface.co/oliverguhr/spelling-correction-english-base
# pip install tf-keras

corrector = pipeline("text2text-generation", model="oliverguhr/spelling-correction-english-base")


def normalize(str):
    return str.lower().strip('.!? ')


def spell_check(input_text, id):
    output = corrector(input_text, max_length=2048)
    corrected_text = output[0]["generated_text"]
    if normalize(corrected_text) != normalize(input_text):
        return corrected_text
    return None


if __name__ == '__main__':
    spell_check("lets do a comparsion", 0)
    spell_check("I love to code in Pyhton.", 0)
    spell_check("Ths sentence has some misspeld words.", 0)
    spell_check("Screw you kuys, I am going home.", 1)
    spell_check("on one side of the island was a hugh rock, almost detached", 11595)
    spell_check("The glass was opacified more greater privacy", 11682)
    spell_check("in collee she minored in mathematics", 12111)
    spell_check("The scientists had to accommodate the new results with the existing theories", 10184)