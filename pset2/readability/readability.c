#include <stdio.h>
#include <cs50.h>
#include <math.h>
#include <ctype.h>
#include <string.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

// pseudocode
// need # of letters, words, setences in text
// letters uppercase & lowercase ignore spaces/punctuation
// for loop for length of string (funcion in lecture)
// if upper or lowercase letter increment letter counter (functions to determine type of character)
// words - first nonspace character = word, hit space, look out for next alphabetic character increment word count and repeat
// sentences - any . ! ? indicates a sentence, any time you hit one of these characters increment sentence count
// plug values into formula, round score using round function


int main(void)
{

    string text = get_string("Text: ");
    //totals in text
    float letters = count_letters(text);
    float words = count_words(text);
    float sentences = count_sentences(text);
    // per 100 words
    float L = (letters / words) * 100;
    float S = (sentences / words) * 100;
    int index = trunc(round(0.0588 * L - 0.296 * S - 15.8));

    
    if (index < 1)
    {
        printf("Before Grade 1\n");
    } 
    else if (index >= 16) 
    {
        printf("Grade 16+\n");
    } 
    else 
    {
        printf("Grade %i\n", index);
    }
}



// helper functions
int count_letters(string text)
{
    int letters = 0;

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
    }
    return (float) letters;
}

int count_words(string text)
{
    int words = 0;

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isspace(text[i]))
        {
            words++;
        }
    }
    return (float) words + 1;
}

int count_sentences(string text)
{
    int sentences = 0;

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == '!' || text[i] == '?' || text[i] == '.')
        {
            sentences++;
        }
    }
    return (float) sentences;
}