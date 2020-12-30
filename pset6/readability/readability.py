import cs50
import math

# make helper functions
# plug values into formula


def count_letters(text):
    letters = 0
    for i in range(len(text)):
        if (text[i].isalpha()):
            letters += 1 
    return float(letters)     


def count_words(text):
    words = 0
    for i in range(len(text)):
        if (text[i].isspace()):
            words += 1
    return float(words) + 1
  
    
def count_sentences(text):
    sentences = 0
    for i in range(len(text)):
        if (text[i] == '!' or text[i] == '?' or text[i] == '.'):
            sentences += 1
    return float(sentences)
    

# main part of application

text = cs50.get_string("Text: ")
letters = count_letters(text)
words = count_words(text)
sentences = count_sentences(text)

l = (letters / words) * 100
s = (sentences / words) * 100  
pre_index = round(0.0588 * l - 0.296 * s - 15.8)
index = math.trunc(pre_index)

if (index < 1):
    print("Before Grade 1")
elif (index >= 16):
    print("Grade 16+")
else:
    print(f"Grade {index}")