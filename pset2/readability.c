#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>


int main(void)
{
    //Gets text from the user
    string text = get_string("Text:\n");
    
    //Finds string lenth
    int length = strlen(text);
    
    //Declares l
    int l = 0;
    
    //Counts letters of string
    for (int n = 0; n < length; n += 1)
    {
        char c = text[n];
        if (isalpha(c) != 0)
        {
            l += 1;
        }
    }
    
    //Declares w
    int w = 1;
   
    //counts words of string
    for (int n = 0; n < length; n += 1)
    {
        if (text[n] == ' ')
        {
            w += 1;
        }
       
    }
   
    //Declares s
    int s = 0;
   
    //Finds sentances in a string
    for (int n = 0; n < length; n += 1)
    {
        if ((text[n] == '.') || (text[n] == '?') || (text[n] ==  '!'))
        {
            s += 1;
        } 
    }
    
   // Defines W
    float W = (float) w / 100;
   
    //Declares L
    float L = l / W;
   
    //Declares S
    float S = s / W;
   
    //Grade Level Function
    int index = round(.0588 * L - 0.296 * S - 15.8);
   
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
