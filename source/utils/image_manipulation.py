from PIL import Image


def replace_colors(image, red=(255, 0, 0), green=(0, 255, 0), blue=(0, 0, 255)):
    """
        Replaces the colors in the image with the given colors for the red, blue and green.
    """
    #Split up in red, green, blue and possible alpha (we simply ignore the alpha)
    channels = image.split()
    
    #Looping through all the pixels
    for point in [(x,y) for x in range(image.size[0]) for y in range(image.size[1])]:
        #percentages of colors
        rp = channels[0].getpixel(point) / 255.0
        gp = channels[1].getpixel(point) / 255.0
        bp = channels[2].getpixel(point) / 255.0
        
        #calculate new pixel value
        nrp = red[0] * rp + green[0] * gp + blue[0] * bp
        ngp = red[1] * rp + green[1] * gp + blue[1] * bp
        nbp = red[2] * rp + green[2] * gp + blue[2] * bp

        #sanitize
        nrp = int(round(min(nrp, 255)))
        ngp = int(round(min(ngp, 255)))
        nbp = int(round(min(nbp, 255)))
        
        channels[0].putpixel(point, nrp)
        channels[1].putpixel(point, ngp)
        channels[2].putpixel(point, nbp)
        
    return Image.new(image.mode, channels)
    