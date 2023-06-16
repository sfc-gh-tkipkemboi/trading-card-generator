import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import requests

import smtplib
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
from email.mime.base import MIMEBase 
from email import encoders

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

@st.cache_data
def fetch_github_profile_image_and_python_repos(username):
    """Fetch profile image and Python repos"""
    headers = {'Authorization': f'token {st.secrets["github"]["token"]}'}
    python_repos_count = 0
    try:
        # Fetch user data
        response = requests.get(f"https://api.github.com/users/{username}", 
                                headers=headers)
        if response.status_code == 200:
            data = response.json()
            if "avatar_url" in data:
                avatar_url = data["avatar_url"]
                image_response = requests.get(avatar_url, headers=headers)
                if image_response.status_code == 200:
                    profile_image = image_response.content
                    
        # Fetch repos data
        repos_response = requests.get(f"https://api.github.com/users/{username}/repos", 
                                      headers=headers)
        if repos_response.status_code == 200:
            repos_data = repos_response.json()
            for repo in repos_data:
                if repo["language"] == "Python":
                    python_repos_count += 1

        return profile_image, python_repos_count
    except Exception as e:
        st.error(f"An error occurred: {e}")
    return None, 0

def add_text_to_card(draw, text, position, font_path, 
                     font_size=60, color=(255, 255, 255)):
    myFont = ImageFont.truetype(font_path, font_size)
    draw.text(position, text, font=myFont, fill=color)

def create_trading_card(person_image, person_position, output_path, text, 
                        github_username, num_repos, choice_words):
    
    if not isinstance(choice_words, list):
        choice_words = []
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
    font_path = "assets/SpaceGrotesk-Bold.ttf"
    font_size = 50
    myFont = ImageFont.truetype(font_path, font_size)

    text_position = (190, 75)
    draw.text(text_position, text, font=myFont, fill=(255, 255, 255))

    # GitHub username
    add_text_to_card(draw, f"@{github_username}", (370, 680), font_size=30, 
                     font_path="assets/SpaceGrotesk-Light.ttf")
    # Choice words
    if choice_words:
        words_per_line = 2  # Limit the number of words per line to 2
        for i, word in enumerate(choice_words):
            line = i // words_per_line
            position_in_line = i % words_per_line
            x_position = 100 + position_in_line * 320  # Adjust as needed for spacing between words
            y_position = 730 + line * 35  # Adjust as needed for spacing between lines
            add_text_to_card(draw, word, (x_position, y_position), font_size=20, 
                            font_path="assets/SpaceGrotesk-Light.ttf")
            
    # Number of apps built
    add_text_to_card(draw, str(num_repos), (100, 600), font_size=70, 
                    font_path="assets/SpaceGrotesk-Bold.ttf")

    add_text_to_card(draw, "Python repos", (100, 680), font_size=30, 
                     font_path="assets/SpaceGrotesk-Bold.ttf")

    # Save the trading card to a byte buffer
    output_buffer = io.BytesIO()
    trading_card.save(output_buffer, format='PNG')
    output_buffer.seek(0)

    return output_buffer

def send_email(to_address, subject, body, trading_card_buffer):
    msg = MIMEMultipart()
    msg['From'] = st.secrets["email"]["gmail"]
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Attach the trading card
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(trading_card_buffer.getvalue())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="trading_card.png"')
    msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(st.secrets["email"]["gmail"], st.secrets["email"]["pass"])
        text = msg.as_string()
        server.sendmail(st.secrets["email"]["gmail"], to_address, text)
        server.quit()
        st.success("Email sent successfully!")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def main():
    st.title("Snowflake Summit Trading Card")

    # Fixed values for the position and size of the image
    image_x = 142
    image_y = 158
    image_size = 472

    # Initialize trading_card_buffer
    trading_card_buffer = None  

    with st.sidebar:
        person_image_option = st.radio("Select image source:", ("Take selfie", "GitHub profile"))
        text = st.text_input("Enter your name:", placeholder='Bertram Gilfoyle')
        github_username = st.text_input("Enter GitHub username:", placeholder='gilfoyle').lower()

        # Fetch GitHub details as soon as a username is entered
        person_image_data, python_repos_count = None, 0
        if github_username:
            person_image_data, python_repos_count = fetch_github_profile_image_and_python_repos(github_username)

        email = st.text_input("Enter your email address (optional):", 
                              placeholder="gilfoyle@sandpiper.com", 
                              help="We will send you the generated image!")

        # Choice words
        choice_words_options = ["multipage app maverick", 
                                "Pythonista", 
                                "Data wizard", 
                                "I love Streamlit"]
        chosen_words = st.multiselect("Choose your favorite words:", 
                                      choice_words_options, key='chosen_words')

    if person_image_option == "Take selfie":
        with st.form(key='selfie_form'):
            img_file_buffer = st.camera_input("Take selfie 📸", 
                                              help="Click on the `Take Photo` below to snap a selfie!")
            if img_file_buffer is not None:
                person_image = Image.open(img_file_buffer).convert('RGBA')
                person_image = person_image.resize((image_size, image_size)) 
                trading_card_buffer = create_trading_card(person_image, 
                                                          (image_x, image_y),
                                                           "output.png", text, 
                                                           github_username, 
                                                           python_repos_count, 
                                                           chosen_words)
            selfie_submit_button = st.form_submit_button(label='Generate and Email Card', 
                                                         use_container_width=True, 
                                                         type="primary")

    elif person_image_option == "GitHub profile":
        with st.sidebar.form(key='github_form'):
            if github_username and text and person_image_data:
                person_image = Image.open(io.BytesIO(person_image_data)).convert('RGBA')
                person_image = person_image.resize((image_size, image_size))
                trading_card_buffer = create_trading_card(person_image, 
                                                          (image_x, image_y), 
                                                          "output.png", text, 
                                                          github_username, 
                                                          python_repos_count, 
                                                          chosen_words)
            else:
                st.error("Failed to fetch GitHub profile image. Please check the GitHub username.")
            github_submit_button = st.form_submit_button(label='Generate and Email Card',
                                                         use_container_width=True, 
                                                         type="primary")

    if (('selfie_submit_button' in locals() and selfie_submit_button) or ('github_submit_button' in locals() and github_submit_button)) and 'trading_card_buffer' in locals():
        st.image(trading_card_buffer, use_column_width=True)

        if email:
            subject = "Your Custom Trading Card from Snowflake Summit is Ready! 🎈"
            body = f"""
Hello {text.split(' ')[0]},

We're excited to share that your custom trading card, crafted at the Snowflake Summit, is ready! We've attached it to this email for you. 

This unique card represents your participation and engagement at the Streamlit booth. We hope you love it as much as we enjoyed chatting with you.

Feel free to share your card on social media platforms using our event hashtag, #SnowflakeSummit. We'd love to see how you're displaying your card!

To learn more about Streamlit, visit https://streamlit.io and also check out our community forum at https://discuss.streamlit.io for inspiration and support.

Thank you for being a part of Snowflake Summit. We look forward to your continued participation in our community!

Happy Streamlit-ing! 🎈
"""

            send_email(email, subject, body, trading_card_buffer)


if __name__ == '__main__':
    main()


