#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

#define bytes 512

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // checks # of inputs entered
    if (argc != 2)
    {
        fprintf(stderr, "Please only enter 1 input\n");
        return 1;
    }

    // remember input
    char *input = argv[1];

    // open input file
    FILE *inptr = fopen(input, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", input);
        return 2;
    }

    BYTE buffer[512];
    int counter = 0;

    char filename[8];
    FILE *outptr = NULL;

    while (true)
    {
        // read a block of the memory card image
        size_t bytesRead = fread(buffer, sizeof(BYTE), bytes, inptr);

        // ends loop when we reach end of the card
        if (bytesRead == 0 && feof(inptr))
        {
            break;
        }

        // conditions to be a jpeg
        bool containsJpegHeader = buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0;

        // if we find a jpeg close previous file
        if (containsJpegHeader && outptr != NULL)
        {
            fclose(outptr);
            counter++;
        }

        // if we found a JPEG, we need to open the file for writing
        if (containsJpegHeader)
        {
            sprintf(filename, "%03i.jpg", counter);
            outptr = fopen(filename, "w");
        }

        // write anytime we have an open file
        if (outptr != NULL)
        {
            fwrite(buffer, sizeof(BYTE), bytesRead, outptr);
        }
    }

    // close last jpeg file
    fclose(outptr);

    // close input
    fclose(inptr);

    // success
    return 0;
}