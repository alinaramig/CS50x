// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Opens imput file
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // Opens output file
    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // Assignes factor of volume change
    float factor = atof(argv[3]);

    // Copy header from input file to output file

    // Creates location to store header
    uint8_t header[HEADER_SIZE];

    // Copys header into the ouutput file
    fread(&header, HEADER_SIZE, 1, input);
    
    fwrite(&header, HEADER_SIZE, 1, output);
    
    // Creates buffer to store samples
    int16_t buffer; 

    //Reads to buffer
    while (fread(&buffer, sizeof(int16_t), 1, input))
    {
        buffer *= factor;
        fwrite(&buffer, sizeof(int16_t), 1, output);
    }

    // Close files
    fclose(input);
    fclose(output);
}
