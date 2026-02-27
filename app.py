import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import numpy as np
import io
import os

st.set_page_config(page_title="Tamil Thumbnail Generator", layout="centered")

OUTPUT_SIZE = (1080, 1920)
TITLE_TEXT = "காயத்ரி மணமகள்"

INFO_TEXT = [
    "மணமகள் விவரம்",
    "பெயர் : காயத்ரி",
    "வயது : 23",
    "சொந்த : உண்டு",
    "வீடு",
    "இரண்டாம் திருமணம்",
    "குழந்தை இல்லை",
    "மேலும் தகவலுக்கு:",
    "PixcelVibe",
    "எதிர்பார்ப்பு இல்லை",
    "நல்ல மணமகன் தேவை"
]

# --------- Safe Font Loader ---------
def load_font(font_name, size):
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(base_dir, font_name)
        return ImageFont.truetype(font_path, size)
    except:
        return ImageFont.load_default()

# --------- Gradient Background ---------
def create_gradient(size):
    width, height = size
    gradient = np.zeros((height, width, 3), dtype=np.uint8)

    for y in range(height):
        ratio = y / height
        r = int(255 * ratio)
        g = int(180 * (1 - ratio))
        b = int(50 * (1 - ratio))
        gradient[y, :, :] = (b, g, r)

    return Image.fromarray(gradient)

# --------- Enhance Image ---------
def enhance_image(img):
    img = ImageEnhance.Brightness(img).enhance(1.1)
    img = ImageEnhance.Contrast(img).enhance(1.2)
    return img

# --------- Main Thumbnail Function ---------
def create_thumbnail(uploaded_image):
    bg = create_gradient(OUTPUT_SIZE)

    user_img = Image.open(uploaded_image).convert("RGBA")

    # Crop upper 70% (face focus)
    width, height = user_img.size
    user_img = user_img.crop((0, 0, width, int(height * 0.7)))

    # Resize
    user_img = user_img.resize((600, 1000))
    user_img = enhance_image(user_img)

    # Paste to right
    bg.paste(user_img, (450, 600), user_img)

    draw = ImageDraw.Draw(bg)

    # Load Fonts Safely
    title_font = load_font("NotoSansTamil-Bold.ttf", 120)
    normal_font = load_font("NotoSansTamil-Regular.ttf", 40)

    # Title
    draw.text((100, 100), TITLE_TEXT, fill="white", font=title_font)

    # Info Cards
    y = 500
    for text in INFO_TEXT:
        draw.rounded_rectangle(
            [(60, y), (540, y + 60)],
            radius=20,
            fill="white"
        )
        draw.text((80, y + 10), text, fill="blue", font=normal_font)
        y += 80

    # Bottom Red Curve
    draw.ellipse((0, 1650, 1080, 2100), fill="red")
    draw.text((420, 1750), "Shorts", fill="yellow", font=normal_font)

    return bg.convert("RGB")

# --------- Streamlit UI ---------
st.title("📱 Tamil Matrimonial Thumbnail Generator")

uploaded_file = st.file_uploader("Upload Girl Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    result = create_thumbnail(uploaded_file)

    st.image(result, caption="Preview", use_column_width=True)

    buf = io.BytesIO()
    result.save(buf, format="JPEG", quality=95)

    st.download_button(
        label="Download 1080x1920 JPG",
        data=buf.getvalue(),
        file_name="thumbnail.jpg",
        mime="image/jpeg"
    )
