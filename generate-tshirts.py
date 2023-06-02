import json
import os
from PIL import Image, ImageDraw, ImageFont

# Load the input images
background_image = Image.open("background.png")
tshirt_mask_image = Image.open("tshirt-mask.png")
logo_mask_image = Image.open("logo-mask.png")

# Load the font (assuming you have arial.ttf in the working directory)
font = ImageFont.truetype('opensans.ttf', 20)

# Create a new folder to store the output images
output_folder = 'output_images'
os.makedirs(output_folder, exist_ok=True)

# Load color schemes from a JSON file
with open("color_schemes.json", "r") as f:
    color_schemes = json.load(f)

for color_scheme in color_schemes:
    # Create a blank image of the same size as the background image
    output_image = Image.new("RGBA", background_image.size)

    # Extract tshirt and logo colors from the color scheme
    tshirt_color = tuple(color_scheme['tshirt_color'])
    logo_color = tuple(color_scheme['logo_color'])
    
    # Paste the tshirt-colored t-shirt onto the output image using the t-shirt mask
    output_image.paste(tshirt_color, mask=tshirt_mask_image)

    # Paste the logo-colored logo onto the output image using the logo mask
    output_image.paste(logo_color, mask=logo_mask_image)

    # Composite the output image with the background image
    final_output = Image.alpha_composite(background_image.convert("RGBA"), output_image)

    # Draw text on the final output image
    draw = ImageDraw.Draw(final_output)
    text = "Tshirt: " + color_scheme['tshirt_name'] + ", Logo: " + color_scheme['logo_name']
    
    x, y = 10, final_output.height - 30  # Position of the text
    fill = "black"  # Color of the text
    outline = "white"  # Color of the outline

    # Draw outline
    draw.text((x-1, y), text, font=font, fill=outline)
    draw.text((x+1, y), text, font=font, fill=outline)
    draw.text((x, y-1), text, font=font, fill=outline)
    draw.text((x, y+1), text, font=font, fill=outline)

    # Draw text
    draw.text((x, y), text, font=font, fill=fill)

    # Save the final output image in the output folder
    filename = color_scheme['tshirt_name'] + '-with-' + color_scheme['logo_name'] + '.png'
    output_path = os.path.join(output_folder, filename.replace(' ', '-'))
    final_output.save(output_path)