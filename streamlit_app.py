import streamlit as st
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
# import cv2
import requests
from io import BytesIO
from urllib.request import urlopen

# req = requests.get("https://github.com/googlefonts/roboto/blob/master/src/hinted/Roboto-Regular.ttf?raw=true")

# roboto_font = ImageFont.truetype(BytesIO(req.content), 72)

# im = cv2.imread('template.png')
# height = im.shape[0]
# width = im.shape[1]

# Open pitcher and pitch images
person = Image.open('person1.png')
card = Image.open('template.png').convert('RGBA')
rectangle = Image.open('rectangle.png')

rectangle.paste(person,(120,120))
# rectangle.show()

rectangle.alpha_composite(card,(0,0))
# rectangle.show()

# Call draw Method to add 2D graphics in an image
draw = ImageDraw.Draw(rectangle)
 
# Custom font style and font size
# myFont = ImageFont.truetype('FreeMono.ttf', 65)
# truetype_url = 'https://github.com/googlefonts/roboto/blob/master/src/hinted/Roboto-Regular.ttf?raw=true'
# roboto_font = ImageFont.truetype(urlopen(truetype_url), size=10)
# roboto_font = ImageFont.load_default()
myFont = ImageFont.truetype(r'BebasNeue-Regular.ttf', 60)
# font = ImageFont.truetype(r'C:\Users\System-Pc\Desktop\arial.ttf', 70)

# Add Text to an image
draw.text((200, 80), "Caroline Frasca", font=myFont, fill =(255, 255, 255))

rectangle.show()

# Create a blank grey image
# wip_img = Image.new("RGBA", (756, 1051), "#f2f2f2")
# # Load the santa hat
# circle = Image.open("mask.png")
# # At first this is just a black rectangle of the same size as the hat
# shadow = Image.new("RGBA", circle.size, color="black")

# # Coordinates at which to draw the hat and shadow
# hat_coords = (25, 25)
# # shadow_coords = (30, 30)

# # Custom-mask the shadow so it has the same shape as the santa hat
# # wip_img.paste(shadow, shadow_coords, mask=circle)
# # Now paste the hat on top of the shadow
# wip_img.paste(circle, box=hat_coords, mask=circle)
# wip_img.show()
# wip_img.save("result.png")
# card.paste(rectangle)
# card.show()

# rectangle.paste(card)
# rectangle.show()

# person.paste(card)
# person.show()
# new_image = card.paste(card, (0,0))
# new_image.show()
# fg.paste(bg, (0,0))
# rectangle = Image.open('rectangle.png')
# rectangle.show()
# w, h = fg.width, fg.height
# w = width
# h = height

# merge = st.button("Merge images")
# pasted = rectangle.paste(person, (0,0))
# pasted = card.paste(person,(0,0),mask=card)
# pasted.show()
  
# if merge:
#     # new_image = bg.resize((756, 1051))
# # No transparency mask specified, 
# # simulating an raster overlay
#     # bg.paste(fg, (0,0), mask = fg,)
#     # fg.paste(bg, (0,0))
#     resized_person = rectangle.paste(person, (0,0))
#     resized_person.show()

    # new_image.show()

    # bg.show()

# if merge:
#     # Iterate over rows and columns
#     for y in range(h):
#         for x in range(w):
#             # Get components of foreground pixel
#             r, g, b, a = fg.getpixel((x,y))
#             # If foreground is opaque, overwrite background with foreground
#             # if a>128:
#             #     bg.putpixel((x,y), (r,g,b))

#     # Save result    
#     bg.save('result.png')
#     st.image('result.png')
