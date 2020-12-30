// Implements a dictionary's functionality

#include <stdbool.h>

#include "dictionary.h"
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <strings.h>



// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table - per letter
const unsigned int N = 500;

// Hash table
node *table[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // change word to be lowercase
    int n = strlen(word);
    char wordlow[LENGTH + 1];

    for (int i = 0; i < n; i++)
    {
        wordlow[i] = tolower(word[i]);
    }

    // add string null terminator
    wordlow[n] = '\0';

    // get index (hash code) for hashed word
    int code = hash(wordlow);

    // set curNode to point at head of bucket
    node *curNode = table[code];

    // move along the bucket checking if found word if yes return
    // if no move on to next item in linked list
    while (curNode != NULL)
    {
        if (strcasecmp(curNode->word, wordlow) == 0)
        {
            return true;
        }
        else
        {
            curNode = curNode->next;
        }
    }

    // if nothing found return false
    return false;


}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned int hash_value = 0;
    for (int i = 0, n = strlen(word); i < n; i++)
    {
        hash_value = (hash_value << 2) ^ word[i];
    }
    return hash_value % N; //N is size of hashtable
}

// total words counter
int totalWords = 0;



// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // TODO
    // open dictionary file
    FILE *inputr = fopen(dictionary, "r");
    // check dictionary exists
    if (inputr == NULL)
    {
        return false;
    }
    // read each word in dictionary file

    // store the word
    char word[LENGTH + 1];
    
    // create node
    while (fscanf(inputr, "%s", word) != EOF)
    {
        node *n = malloc(sizeof(node));

        if (n == NULL)
        {
            return false;
        }

        // copy word into node
        strcpy(n->word, word);

        // determine which hash code to use
        int code = hash(word);

        // sets head to point to first bucket
        node *head = table[code];

        /* if there is no head */
        if (head == NULL)
        {
            // still need to initalize next even if the list is empty 
            n->next = NULL; 
            table[code] = n;
            totalWords++;
        }
        else
            // if head already exists
        {
            // point new node at first element of linked list;
            n->next = table[code];
            // set first element as new node;
            table[code] = n;

            totalWords++;
        }


    }
   

    fclose(inputr);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    if (totalWords > 0)
    {
        return totalWords;
    }
    else
    {
        return 0;
    }
}



// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{

    for (int i = 0; i < N + 1; i++)
    {

        node *head = NULL;
        node *curNode = table[i];
        node *temp = curNode;


        while (curNode != NULL)
        {
            curNode = curNode->next;
            free(temp);
            temp = curNode;
        }

    }

    // TODO
    return true;
}

