#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    // Verifty's there's 2 command line arguments
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    string code = argv[argc - 1];

    // Verify's that the argument is a letter
    for (int n = 0; code[n] != '\0'; n += 1)
    {
        if (!isalpha(code[n]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
        
    }
    // At this point we know that c can be turned into an charachter
    int length = strlen(code);

    // Verifying that the code is 26 charachters
    if (length != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
    //Converting argument to lowercase
    for (int n = 0; n < length; n += 1)
    {
        code[n] = tolower(code[n]);
    }
    
    //Checking there are no duplicates in the argument
    int booleanarray[26];
    
    //Creating a Boolean array
    for (int n = 0; n < 26; n += 1)
    {
        booleanarray[n] = 0;
    }
    
    //Comparing arrays
    for (int n = 0; n < 26; n += 1)
    {
        // Defines index. Trasnforms char into int. Transforms int into index #. 
        int index = (int)code[n] - 97;
        
        // Fails program if there is a duplicate
        if (booleanarray[index])
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
        
        // Adds 1 to the index
        booleanarray[index] += 1;
    }
   

    // Get plaintext from User
    string plaintext = get_string("plaintext: ");
    
    // Get length of plaintext
    int length_p = strlen(plaintext);

    // Cycle through alphabetical chars & print
    printf("ciphertext: ");

    for (int n = 0; n < length_p; n += 1)
    {
        int cnumber = plaintext[n];
        char letter = plaintext[n];


        // Checks if charachter is a letter
        if (isalpha(letter))
        {
            // Checks if charachter is upper or lowercase and converts it to ciphertext
            if (isupper(letter) != 0)
            {
                cnumber -= 65;
                cnumber += (code[cnumber] - 97 - cnumber);
                int final_number = cnumber % 26;
                final_number += 65;
                char final_letter = (char)final_number;
                printf("%c", final_letter);
            }
            else
            {
                cnumber -= 97;
                cnumber += (code[cnumber] - 97 - cnumber);
                int final_number = cnumber % 26;
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
    return 0;
}