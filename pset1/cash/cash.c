#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void) 
{
    // initialize values of coins
    int quarter = 25;
    int dime = 10;
    int nickel = 5;
    int penny = 1;
    
    float dollars;
    do
    {
        dollars = get_float("Change to give: ");
    }
    // check amount given is > 0
    while (dollars <= 0);
    
    int cents = round(dollars * 100);
    int coins = 0;
    
    while (cents > 0) 
    {
        // check if possible to give quarter
        if (cents - quarter >= 0) 
        {
            cents = cents - 25;
            coins++;
            
        }  // check if possible to give dime
        else if (cents - dime >= 0)
        {
            cents = cents - 10;
            coins++;
            
        }  // check if possible to give nickel
        else if (cents - nickel >= 0)
        {
            cents = cents - 5;
            coins++;
            
        } // use a penny 
        else
        {
            cents = cents - 1;
            coins++;
        }
    }
    printf("%i\n", coins);
}