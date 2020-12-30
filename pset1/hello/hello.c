#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // gets name from user input assigns to to variable name
    string name = get_string("What is your name?\n");
    // prints hello and name variable 
    printf("hello, %s\n", name);
}