#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int avg = round(((float) image[i][j].rgbtBlue + (float) image[i][j].rgbtGreen + (float) image[i][j].rgbtRed) / 3);
            image[i][j].rgbtBlue = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtRed = avg;
        }
    }
    return;
}

// Convert image to sepia
// loop over each pixel
// for r g b value apply the specific sepia formula to get sepia value
// convert value to an int (no decimals) - round
// if value > 255 make it 255

void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sepiaRed = round(0.393 * (float) image[i][j].rgbtRed + 0.769 * (float) image[i][j].rgbtGreen + 0.189 *
                                 (float) image[i][j].rgbtBlue);
            int sepiaGreen = round(0.349 * (float) image[i][j].rgbtRed + 0.686 * (float) image[i][j].rgbtGreen + 0.168 *
                                   (float) image[i][j].rgbtBlue);
            int sepiaBlue = round(0.272 * (float) image[i][j].rgbtRed + 0.534 * (float) image[i][j].rgbtGreen + 0.131 *
                                  (float) image[i][j].rgbtBlue);

            if (sepiaRed < 255)
            {
                image[i][j].rgbtRed = sepiaRed;
            }
            else
            {
                image[i][j].rgbtRed = 255;
            }

            if (sepiaGreen < 255)
            {
                image[i][j].rgbtGreen = sepiaGreen;
            }
            else
            {
                image[i][j].rgbtGreen = 255;
            }

            if (sepiaBlue < 255)
            {
                image[i][j].rgbtBlue = sepiaBlue;
            }
            else
            {
                image[i][j].rgbtBlue = 255;
            }
        }
    }
    return;
}



void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = temp;
        }
    }
}



void blur(int height, int width, RGBTRIPLE image[height][width])
{

    // make a copy of the image to work with
    RGBTRIPLE imageCopy[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            imageCopy[i][j] = image[i][j];
        }
    }

    // loop over pixels in total image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // initialize total rgb + total pixel values
            float totalr = 0;
            float totalg = 0;
            float totalb = 0;
            int totalpix = 0;

            // check pixel within 1 / -1 of i
            for (int k = -1; k < 2; k++)
            {
                // check pixel within 1 / -1 of i
                for (int l = -1; l < 2; l++)
                {
                    // check pixel checked is in bounds
                    if (i + k >= 0 && j + l >= 0 && i + k <= height - 1 && j + l <= width - 1)
                    {
                        totalr = imageCopy[i + k][j + l].rgbtRed + totalr;
                        totalg = imageCopy[i + k][j + l].rgbtGreen + totalg;
                        totalb = imageCopy[i + k][j + l].rgbtBlue + totalb;
                        totalpix++;
                    }
                }
            }

            image[i][j].rgbtRed = round(totalr / totalpix);
            image[i][j].rgbtGreen = round(totalg / totalpix);
            image[i][j].rgbtBlue = round(totalb / totalpix);
        }
    }


}



