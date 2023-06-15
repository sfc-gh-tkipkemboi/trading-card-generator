import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import requests

st.set_page_config(
    page_title="Snowflake Summit Trading Card Generator App",
    page_icon="🎴",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://discuss.streamlit.io/',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is Trading Card Generator app made with Streamlit for Snowflake Summit!"
    }
)

TEMPLATE_IMAGE_PATH = "assets/template.png"


def fetch_github_profile_image(username):
    """Rate limit with token is 5000 API calls/hour or ~80 calls/minute"""
    headers = {'Authorization': f'token {st.secrets["github"]["token"]}'}
    try:
        response = requests.get(f"https://api.github.com/users/{username}", 
                                headers=headers)
        if response.status_code == 200:
            data = response.json()
            if "avatar_url" in data:
                avatar_url = data["avatar_url"]
                image_response = requests.get(avatar_url, headers=headers)
                if image_response.status_code == 200:
                    return image_response.content
    except Exception as e:
        st.error(f"An error occurred: {e}")
    return None

def add_text_to_card(draw, text, position, font_path, 
                     font_size=60, color=(255, 255, 255)):
    myFont = ImageFont.truetype(font_path, font_size)
    draw.text(position, text, font=myFont, fill=color)

def create_trading_card(person_image, person_position, output_path, text, 
                        github_username):
    card = Image.open(TEMPLATE_IMAGE_PATH).convert('RGBA')

    # New image with the same size as the template
    trading_card = Image.new('RGBA', card.size)

    # Composite card onto the trading card
    trading_card.alpha_composite(card)

    # Paste image onto the trading card
    mask = Image.new("L", person_image.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0) + person_image.size, fill=255)
    trading_card.paste(person_image, person_position, mask=mask)

    # Call draw Method to add 2D graphics in the trading card
    draw = ImageDraw.Draw(trading_card)

    # Load font
    font_path = "assets/RobotoMono-Bold.ttf"
    font_size = 40
    myFont = ImageFont.truetype(font_path, font_size)

    text_position = (220, 75)
    draw.text(text_position, text, font=myFont, fill=(255, 255, 255))

    # GitHub username
    add_text_to_card(draw, f"@{github_username}", (370, 685), font_size=30, 
                     font_path="assets/RobotoMono-VariableFont_wght.ttf")
    # Choice words
    add_text_to_card(draw, "multipage app maverick", (310, 750), font_size=25, 
                     font_path="assets/RobotoMono-VariableFont_wght.ttf")
    add_text_to_card(draw, "Pythonista", (100, 750), font_size=25, 
                     font_path="assets/RobotoMono-VariableFont_wght.ttf")
    # Number of apps built
    add_text_to_card(draw, "473", (100, 600), font_size=70, 
                     font_path="assets/BebasNeue-Regular.ttf")
    add_text_to_card(draw, "apps built", (100, 685), font_size=30, 
                     font_path="assets/RobotoMono-VariableFont_wght.ttf")

    # Save the trading card to a byte buffer
    output_buffer = io.BytesIO()
    trading_card.save(output_buffer, format='PNG')
    output_buffer.seek(0)

    return output_buffer


def main():
    st.title("Snowflake Summit Trading Card")

    # Fixed values for the position and size of the image
    image_x = 142
    image_y = 158
    image_size = 472

    # Initialize trading_card_buffer
    trading_card_buffer = None  

    with st.sidebar:
        person_image_option = st.radio("Select image source:", 
                                       ("Take selfie", 
                                        "GitHub profile"))
        text = st.text_input("Enter your name:", 'Tony Kipkemboi')
        github_username = st.text_input("Enter GitHub username:", 'tonykipkemboi').lower()

        with st.form(key='form'):
            if person_image_option == "Take selfie":
                img_file_buffer = st.camera_input("Take selfie")
                if img_file_buffer is not None:
                    # Convert the image to PIL format
                    person_image = Image.open(img_file_buffer).convert('RGBA')
                    person_image = person_image.resize((image_size, image_size))  
                    trading_card_buffer = create_trading_card(person_image, 
                                                              (image_x, image_y), 
                                                              "output.png", text, github_username)

            elif person_image_option == "GitHub profile":
                if github_username and text:
                    person_image_data = fetch_github_profile_image(github_username)
                    if person_image_data:
                        person_image = Image.open(io.BytesIO(person_image_data)).convert('RGBA')
                        person_image = person_image.resize((image_size, 
                                                            image_size))
                        trading_card_buffer = create_trading_card(person_image, 
                                                                  (image_x, image_y), 
                                                                  "output.png", text, github_username)
                    else:
                        st.error("Failed to fetch GitHub profile image. Please check the GitHub username.")
            submit_button = st.form_submit_button(label='Generate Trading Card')

    if 'submit_button' in locals() and submit_button and 'trading_card_buffer' in locals():
        st.image(trading_card_buffer, 
                 use_column_width=True)
        
        st.download_button("Download Card", 
                           trading_card_buffer, 
                           file_name="trading_card.png", 
                           mime="image/png",
                           use_container_width=True
                           )

if __name__ == '__main__':
    main()

