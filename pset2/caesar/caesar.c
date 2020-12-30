#include <stdio.h>
#include <cs50.h>
#include <math.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>


// pseudo code
// check command line arguments
// prompt user for plain text
// iterate over each character checking if upper/lower and then changing it
// print out changed character
// print new line



int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else
    {
        string k = argv[1];

        for (int i = 0, n = strlen(k); i < n; i++)
        {
            if (!isdigit(k[i]))
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }
        // number of characters to shift by
        int key = atoi(k);

        string plaintext = get_string("plaintext: ");
        printf("ciphertext: ");

        // loop over plain text
        for (int j = 0, l = strlen(plaintext); j < l; j++)
        {
            char c = plaintext[j];

            if (isalpha(c))
            {
                // adapt the formula so it wraps around correctly
                char m = 'A';
                if (islower(c))
                {
                    m = 'a';
                }
                printf("%c", (c - m + key) % 26 + m);
            }
            else
            {
                printf("%c", c);
            }

        }

        printf("\n");

    }

}

