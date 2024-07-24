import streamlit as st
import numpy as np
from PIL import Image
from geopy.geocoders import Nominatim
import pandas as pd
from geopy.exc import GeocoderUnavailable, GeocoderTimedOut
from tensorflow.keras.models import load_model
from math import radians, sin, cos, sqrt, atan2

# Set the page configuration
st.set_page_config(page_title="Youth Farming Website")

# Define the custom CSS styles
def set_custom_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #E0F7FA;
        }
        h1 {
            color: #01579B;
        }
        h2, h3, h4, h5, h6 {
            color: #455A64;
        }
        .stButton>button {
            background-color: #009688;
            color: white;
            border-radius: 5px;
        }
        .stButton>button:hover {
            background-color: #00796B;
            color: white;
        }
        .stTextInput>div>div>input {
            background-color: #C8E6C9;
            border-color: #388E3C;
            color: #1B5E20;
        }
        .stMarkdown {
            color: #455A64;
        }
        .css-1d391kg {
            background-color: #B2DFDB !important;
        }
        .css-145kmo2, .css-17eq0hr, .css-1avcm0n, .css-1n76uvr, .css-19t9p9f, .css-1d0tddc {
            color: #00796B !important;
        }
        .stRadio > label {
            color: #01579B;
        }
        .stRadio > div > div {
            color: #01579B;
        }
        .closest-soil {
            background-color: #C5E1A5;
            padding: 10px;
            border-radius: 5px;
        }
        .closest-soil p {
            color: #000000;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the function to set the custom styles
set_custom_styles()

# Initialize session state if not already initialized
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

# Navigation functions
def navigate_to(page):
    st.session_state.page = page

def home_page():
    st.title("Yuvaa Farming")
    st.write("Welcome to our Youth Farming website!")
    st.write("Please login, sign up, or use the GPS-based fertilizer recommendation to get started.")
    if st.button("Login"):
        navigate_to('Login')
    if st.button("Sign Up"):
        navigate_to('Signup')
    if st.button("GPS-based Fertilizer Recommendation"):
        navigate_to('GPS-based Fertilizer Recommendation')

def login_page():
    st.title("User Login")
    username = st.text_input("Username (Your Phone Number)", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login", key="login_button"):
        if username == "admin" and password == "password":
            st.write("Logged in successfully!")
            navigate_to('Main')
        else:
            st.write("Invalid username or password.")

def signup_page():
    st.title("User Signup")
    username = st.text_input("Username (Your Phone Number)", key="signup_username")
    password = st.text_input("Password", type="password", key="signup_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")
    if st.button("Sign Up", key="signup_button"):
        if password == confirm_password:
            st.write("Signup successful!")
            navigate_to('Login')
        else:
            st.write("Passwords do not match.")

def main_page():
    st.title("Main Application")
    st.text('Upload an image for prediction')
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])
    
    st.write("Select the month for sowing your crop:")
    selected_month = st.selectbox("Month:", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        if st.button('Predict'):
            with st.spinner('Predicting...'):
                prediction = predict(uploaded_file)
                predicted_class = np.argmax(prediction)
                classes = ['Black Soil', 'Cinder Soil', 'Laterite Soil', 'Peat Soil', 'Yellow Soil']
                st.success(f'Predicted Class: {classes[predicted_class]}')
                st.write('Confidence:', round(prediction[0][predicted_class] * 100, 2), '%')
                
                recommended_crops, recommended_fertilizer = get_recommendations(classes[predicted_class])
                st.write('Recommended Crops:')
                for crop in recommended_crops:
                    st.write(f"- {crop}")
                st.write('Recommended Fertilizer:', recommended_fertilizer)

def predict(image):
    img = Image.open(image)
    img = img.resize((220, 220))
    img = np.expand_dims(img, axis=0)
    img = img / 255.0
    model = load_model('my_model.h5')
    prediction = model.predict(img)
    return prediction

def get_recommendations(soil_type):
    recommendations = {
        'Black Soil': (['Cotton', 'Sugarcane','Rice','Linseed','Jawar','chilly','Ragi','Maize', 'Wheat'], 'N-P-K 10-10-10'),
        'Cinder Soil': (['Barley', 'Cabbage', 'Carrot','Pea','Potato','Tomato','Raddish','Onion','Spinach'], 'N-P-K 5-10-5'),
        'Laterite Soil': (['Cashew', 'Cassava', 'Pineapple', 'Rubber', 'Jackfruit', 'Coconut', 'Tamarind', 'Black Pepper', 'Ginger'], 'N-P-K 8-8-8'),
        'Peat Soil': (['Cranberry', 'Potato', 'Rice', 'Soybean', 'Blueberries','Sphagnum Moss','Bog Rosemary', 'Bog Bean'], 'N-P-K 5-10-20'),
        'Yellow Soil': (['Maize', 'Sorghum', 'Sunflower', 'Tomato', 'Groundnut', 'Soybean', 'Cotton', 'Mustard', 'Sugarcane', 'Turmeric'], 'N-P-K 15-5-10'),

        
        
    }
    return recommendations.get(soil_type, ([], ''))

def about_us_page():
    st.title("About Us")
    st.write("We are passionate about revolutionizing farming practices using technology.")
    st.write("Our mission is to empower farmers and promote sustainable agriculture.")
    
def demand_in_market():
    st.title("Demand in Market")
    st.write("Select the month to see the market demand and recommended fertilizers:")
    selected_month = st.selectbox("Month:", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
    month_recommendations = {
        "January": (["Cotton", "Sugarcane", "Wheat", "Rice", "Linseed", "Jawar", "chilly", "Ragi", "Maize", "Groundnut", "Soybean", "Cotton", "Mustard"], "N-P-K 10-10-10"),
        "February": (["Barley", "Cabbage", "Carrot", "Pea", "Potato", "Tomato", "Raddish", "Onion", "Spinach", "Rice", "Linseed", "Jawar", "chilly", "Ragi", "Maize"], "N-P-K 5-10-5"),
        "March": (["Pineapple", "Cabbage", "Carrot", "Cashew", "Cassava", "Pineapple", "Rubber", "Jackfruit", "Coconut", "Tamarind", "Black Pepper", "Ginger", "Rice", "Linseed", "Jawar", "chilly", "Ragi", "Maize"], "N-P-K 8-8-8"),
        "April": (["Corn", "Rice", "Wheat", "Pineapple", "Cabbage", "Carrot", "Cashew", "Cassava", "Pineapple", "Rubber", "Jackfruit", "Coconut", "Tamarind", "Black Pepper", "Ginger", "Rice", "Linseed", "Jawar", "chilly", "Ragi", "Maize"], "N-P-K 10-10-10"),
        "May": (["Cotton", "Soybean", "Peanut", "Corn", "Rice", "Wheat", "Pineapple", "Cabbage", "Carrot", "Cashew", "Cassava", "Pineapple", "Rubber", "Jackfruit", "Coconut", "Tamarind", "Black Pepper", "Ginger", "Rice", "Linseed", "Jawar", "chilly", "Ragi", "Maize"], "N-P-K 5-10-5"),
        "June": (["Barley", "Rice", "Soybean", "Cotton", "Mustard", "Cotton", "Soybean", "Peanut", "Corn", "Rice", "Wheat", "Pineapple", "Cabbage", "Carrot", "Cashew", "Cassava", "Pineapple", "Rubber", "Jackfruit", "Coconut", "Tamarind", "Black Pepper", "Ginger", "Rice", "Linseed", "Jawar", "chilly", "Ragi", "Maize"], "N-P-K 8-8-8"),
        "July": (["Cotton", "Peanut", "Sunflower", "Cotton", "Soybean", "Peanut", "Corn", "Rice", "Wheat", "Pineapple", "Cabbage", "Carrot", "Cashew", "Cassava", "Pineapple", "Rubber", "Jackfruit", "Coconut", "Tamarind", "Black Pepper", "Ginger", "Rice", "Linseed", "Jawar", "chilly", "Ragi", "Maize"], "N-P-K 5-10-20"),
        "August": (["Corn", "Tomato", "Cucumber", "Cotton", "Soybean", "Peanut", "Corn", "Rice", "Wheat", "Pineapple", "Cabbage", "Carrot", "Cashew", "Cassava", "Pineapple", "Rubber", "Jackfruit", "Coconut", "Tamarind", "Black Pepper", "Ginger", "Rice", "Linseed", "Jawar", "chilly", "Ragi", "Maize"], "N-P-K 10-10-10"),
        "September": (["Wheat", "Barley", "Lettuce", "Cotton", "Soybean", "Peanut", "Corn", "Rice", "Wheat", "Pineapple", "Cabbage", "Carrot", "Cashew", "Cassava", "Pineapple", "Rubber", "Jackfruit", "Coconut", "Tamarind", "Black Pepper", "Ginger", "Rice", "Linseed", "Jawar", "chilly", "Ragi", "Maize"], "N-P-K 5-10-5"),
        "October": (["Soybean", "Pea", "Carrot", "Corn", "Rice", "Wheat", "Pineapple", "Cabbage", "Carrot", "Cashew", "Cassava", "Pineapple", "Rubber", "Jackfruit", "Coconut", "Tamarind", "Black Pepper", "Ginger", "Rice", "Linseed", "Jawar", "chilly", "Ragi", "Maize"], "N-P-K 8-8-8"),
        "November": (["Maize", "Sorghum", "Sunflower", "Corn", "Rice", "Wheat", "Pineapple", "Cabbage", "Carrot", "Cashew", "Cassava", "Pineapple", "Rubber", "Jackfruit", "Coconut", "Tamarind", "Black Pepper", "Ginger", "Rice", "Linseed", "Jawar", "chilly", "Ragi", "Maize"], "N-P-K 15-5-10"),
        "December": (["Cabbage", "Carrot", "Potato", "Cotton", "Soybean", "Peanut", "Corn", "Rice", "Wheat", "Pineapple", "Cabbage", "Carrot", "Cashew", "Cassava", "Pineapple", "Rubber", "Jackfruit", "Coconut", "Tamarind", "Black Pepper", "Ginger", "Rice", "Linseed", "Jawar", "chilly", "Ragi", "Maize"], "N-P-K 5-10-20")
    }
    st.write(f"Market demand for {selected_month}:", month_recommendations[selected_month][0])
    st.write("Recommended fertilizer:", month_recommendations[selected_month][1])


def projects_page():
    st.title("Projects")
    st.write("Explore our latest projects and initiatives in the field of agriculture technology.")
    st.write("From soil health monitoring to crop prediction, we're working on innovative solutions to address farming challenges.")

def contact_us_page():
    st.title("Contact Us")
    st.write("Have questions or feedback? Reach out to us!")
    st.write("Email: contact@yuvaa-farming.com")
    st.write("Phone: 123-456-7890")
    st.write("Address: 123 Farming Street, Agriculture City, Country")

def gps_fertilizer_recommendation():
    st.title("GPS-based Fertilizer Recommendation")

    soil_data = pd.read_csv('tamilnadu_soil_data.csv')

    location = st.text_input("Enter your location (address or coordinates)", "")
    latitude = st.text_input("Enter your latitude (optional)", "")
    longitude = st.text_input("Enter your longitude (optional)", "")

    if st.button("Get Recommendations"):
        if location:
            try:
                geolocator = Nominatim(user_agent="my_app")
                location_obj = geolocator.geocode(location, timeout=10)
                if location_obj:
                    lat, lon = location_obj.latitude, location_obj.longitude
                else:
                    st.write("Unable to geocode the provided location.")
                    return
            except (GeocoderUnavailable, GeocoderTimedOut):
                st.write("Geocoding service is unavailable. Please enter coordinates manually.")
                return
        elif latitude and longitude:
            try:
                lat = float(latitude)
                lon = float(longitude)
            except ValueError:
                st.write("Invalid latitude or longitude values.")
                return
        else:
            st.write("Please provide a location or coordinates.")
            return

        def haversine(lat1, lon1, lat2, lon2):
            try:
                R = 6371.0
                lat1 = radians(lat1)
                lon1 = radians(lon1)
                lat2 = radians(lat2)
                lon2 = radians(lon2)
                dlon = lon2 - lon1
                dlat = lat2 - lat1
                a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
                c = 2 * atan2(sqrt(a), sqrt(1 - a))
                distance = R * c
                return distance
            except Exception as e:
                print("Error in haversine calculation:", e)
                return None

        try:
            soil_data['distance'] = soil_data.apply(
                lambda row: haversine(lat, lon, row['latitude'], row['longitude']), axis=1
            )
            closest_soil = soil_data.loc[soil_data['distance'].idxmin()]

            # Display closest soil data with custom styling
            st.markdown(
                f"""
                <div class="closest-soil">
                    <p><strong>Closest Soil Data:</strong></p>
                    <p>Latitude: {closest_soil['latitude']}</p>
                    <p>Longitude: {closest_soil['longitude']}</p>
                    <p>Soil Type: {closest_soil['soil_type']}</p>
                    <p><strong>Recommended Crops:</strong> {closest_soil['recommended_crops']}</p>
                    <p>pH: {closest_soil['pH']}</p>
                    <p>Recommended Fertilizer: {closest_soil['recommended_fertilizer']}</p>
                </div>
                """, unsafe_allow_html=True
            )

        except KeyError as e:
            st.write(f"Missing expected column in soil data: {e}")
        except Exception as e:
            st.write(f"An error occurred: {e}")

# Define the pages and their corresponding functions
pages = {
    'Home': home_page,
    'Login': login_page,
    'Signup': signup_page,
    'Main': main_page,
    'About Us': about_us_page,
    'Demand in Market': demand_in_market,
    'Projects': projects_page,
    'Contact Us': contact_us_page,
    'GPS-based Fertilizer Recommendation': gps_fertilizer_recommendation
}

# Display the selected page
selection = st.sidebar.selectbox("Navigation", ["Home", "Login", "Signup", "Main", 
                                                "GPS-based Fertilizer Recommendation", 
                                                "Demand in Market", "Contact Us", "Projects", 
                                                "About Us"])
pages[selection]()

