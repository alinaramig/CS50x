#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    // Verifty's there's 2 command line arguments
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    
    string c = argv[argc - 1];
     
    // Verify's that the argument is a digit
    for (int n = 0; c[n] != '\0'; n += 1)
    {
        if (!isdigit(c[n]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    // At this point we know that c can be turned into an integer 
    int C = atoi(c);

    // Get plaintext from User
    string plaintext = get_string("plaintext: ");

    // Get length of string
    int length = strlen(plaintext);

    // Cycle through alphabetical chars & print
    printf("ciphertext: ");

    for (int n = 0; n < length; n += 1)
    {
        int place = plaintext[n];
        char letter = plaintext[n];

        // Checks if charachter is a letter
        if (isalpha(letter) != 0)
        {
            // Checks if charachter is upper or lowercase and converts it to ciphertext
            if (isupper(letter) != 0)
            {
                place -= 65;
                place += C;
                int final_number = place % 26;
                final_number += 65;
                char final_letter = (char)final_number;
                printf("%c", final_letter);
            }
            else
            {
                place -= 97;
                place += C;
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