#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    // if input not between 1 & 8 redo the above
    while (height < 1 || height > 8);
    
    // loop for new line
    for (int i = 0; i < height; i++)
    {
        // loop for spaces 
        for (int k = height - i; k > 1; k--)
        {
            printf(" ");
        }
        // loop for #'s
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}

