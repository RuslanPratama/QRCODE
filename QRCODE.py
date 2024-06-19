import streamlit as st
import qrcode
from PIL import Image, ImageDraw
from io import BytesIO

# Function to convert HEX color to RGB
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Set the page title
st.title("QR Code Generator")

# Organization selection
orgs = ['AAPG', 'Kaldera']
org = st.radio("Select organization:", orgs)

# Set logo and color based on selected organization
if org == 'AAPG':
    Logo_link = '1.png'
    QRcolor = '#363062'
elif org == 'Kaldera':
    Logo_link = '2.png'
    QRcolor = '#952323'

# URL input
url = st.text_input("Enter URL:")

# Convert HEX color to RGB
rgb_color = hex_to_rgb(QRcolor)

# Logo processing
logo = Image.open(Logo_link)
basewidth = 650
wpercent = (basewidth/float(logo.size[0]))
hsize = int((float(logo.size[1])*float(wpercent)))
logo = logo.resize((basewidth, hsize))
QRcode = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    version = 10,
    box_size = 10,
    border = 5
)
QRcode.add_data(url)
QRcode.make()
QRcolor = rgb_color

QRimg = QRcode.make_image(
    fill_color=QRcolor, back_color="white").convert('RGB')

QRimg = QRimg.resize((1500, 1500))

# Create a mask for the logo
mask = Image.new('L', logo.size, 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((0, 0) + logo.size, fill=255)

pos = ((QRimg.size[0] - logo.size[0]) // 2,
    (QRimg.size[1] - logo.size[1]) // 2)
QRimg.paste(logo, pos, mask)

# Display QR code
st.image(QRimg, caption='Generated QR Code')

# Save QR code to a BytesIO object
buffered = BytesIO()
QRimg.save(buffered, format="PNG")
buffered.seek(0)

# Download button
st.download_button(
    label="Download QR Code",
    data=buffered,
    file_name="QR_code.png",
    mime="image/png"
)
