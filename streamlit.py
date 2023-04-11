import streamlit as st
import folium
from PIL import Image, ExifTags
from streamlit_folium import st_folium
import requests
import io

st.set_page_config(layout='wide', page_title='Project Wildfire')
st.title('Project Wildfire :fire:')

my_upload = st.file_uploader('Upload your picture here', type=["png", "jpg", "jpeg"])
col1, col2 = st.columns(2)

# return GPS informations
def display_image_location(image):
    data = dict()
    exif = image.getexif()
    if exif:
        ifd = exif.get_ifd(0x8825) # retrieve gps exif infos
        for key, val in ifd.items():
            data[ExifTags.GPSTAGS[key]] = val
    coordinates = degrees_to_decimals((data['GPSLatitudeRef'], data['GPSLatitude'])), degrees_to_decimals((data['GPSLongitudeRef'], data['GPSLongitude']))

    map = folium.Map(location=coordinates, zoom_start=16)
    folium.Marker(
        coordinates, popup="Fire location", tooltip="Fire location"
    ).add_to(map)
    st_folium(map, width=725)
    
# convert GPS to decimals degrees
def degrees_to_decimals(degrees_coord):
    direction, (degrees, minutes, seconds) = degrees_coord[0], degrees_coord[1]
    dtd = float(degrees) + float(minutes)/60 + float(seconds)/3600
    if direction in ('S','W'):
        dtd*= -1
    return dtd


# display original uploaded image and GPS coordinates
def display_img_gps_location(upload):

    with col1:
        st.header('Detected image')
        st.image(upload)
    
    with col2:
        st.header('Fire location')
        display_image_location(Image.open(my_upload))
    
# run trained model on uploaded image through POST request to API
if st.button("Detect"):
    if my_upload is not None:
        files = {"file": my_upload}
        res = requests.post(url="https://wildfire-project-backend.herokuapp.com/image-detector", files=files)
        display_img_gps_location(res)    


# import requests
# import streamlit as st

# # Get the uploaded image file from Streamlit
# uploaded_file = st.file_uploader("Choose an image file")

# # Check if the file was uploaded
# if uploaded_file is not None:

#     # Set up the requests parameters
#     url = "https://example.com/upload"
#     files = {"file": uploaded_file}

#     # Send the post request with the image file
#     response = requests.post(url, files=files)

#     # Check the response status
#     print(response.status_code)