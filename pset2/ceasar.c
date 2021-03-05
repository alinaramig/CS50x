#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    //Verify command line argument
    int c = atoi(argv[argc - 1]);
    int C = isdigit(c);

    if ((argc != 2) || ( C = 0))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    
    //Get plaintext from User
    string plaintext = get_string("Plaintext: ");
    
    //Get length of string
    int length = strlen(plaintext);
    
    //Cycle through alphabetical chars & print
    printf("Ciphertext:");
    
    for (int n = 0; n < length; n += 1 )
    {
        int place = plaintext[n]; 
        char letter = plaintext[n];
        
        //Checks if charachter is a letter
        if (isalpha(letter) != 0)
        {
            //Checks if charachter is upper or lowercase and converts it to ciphertext
            if (isupper(letter) != 0)
            {
                place -= 65;
                place += c;
                int final_number = place % 26;
                 final_number += 65;
                char final_letter = (char)final_number;
                printf("%c", final_letter);
            }
            else
            {
                place -= 97;
                place += c;
                int final_number = place % 26;
                final_number += 97;
                char final_letter = (char)final_number;
                printf("%c", final_letter); 
            }
        }
        else
        {
            printf("%c", letter);
        }
    }
    printf("\n");

 
}