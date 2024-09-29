import streamlit as st
import requests
import jwt
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# API call to fetch the news data
login_api_url = os.getenv('LOGIN_URL')

secret_key = os.getenv('SECRET_KEY')  # The secret key used to sign the JWT

st.set_page_config(page_title="News Reader")
st.title("News Reader")

# Check if the user is already logged in by checking the session state
if "user_role" in st.session_state and st.session_state["user_role"]:
    if st.sidebar.button("Logout"):
        # Reset session state to clear user role and JWT token
        st.session_state["username"] = ""
        st.session_state["password"] = ""
        st.session_state["user_role"] = None
        st.session_state["jwt_token"] = None
        st.success("Logged out successfully. Please log in again.")
else:
    # Show login form if the user is not logged in
    st.subheader("Login")

# CSS for background and style
page_bg_img = '''
<style>
.stApp {
    background-image: url("https://img.freepik.com/premium-photo/crinkled-worn-page-black-white-text_285145-15590.jpg?w=900");
    background-size: cover;
}
h1, h3 {
    color: black;
}
div[data-testid="stTextInput"] label {
    color: black;
    font-size: 25px;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Initialize session state for username and password
if "username" not in st.session_state:
    st.session_state["username"] = ""

if "password" not in st.session_state:
    st.session_state["password"] = ""

if "user_role" not in st.session_state:
    st.session_state["user_role"] = None  # Store user role here

# Username and Password Inputs
st.session_state["username"] = st.text_input("Username", st.session_state["username"])
st.session_state["password"] = st.text_input("Password", st.session_state["password"], type="password")

# Function to send login request to backend
def login(username, password):
    try:
        response = requests.post(login_api_url, json={"username": username, "password": password})
        if response.status_code == 200:
            return response.json()  # Return the JWT token and role info
        else:
            st.error("Login failed. Please check your credentials.")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
        return None

# Function to decode the JWT token and extract the role
def decode_jwt(jwt_token):
    try:
        decoded_token = jwt.decode(jwt_token, secret_key, algorithms=["HS256"])
        roles = decoded_token.get("roles", [])
        if roles and len(roles) > 0:
            return roles[0].get("authority")
        else:
            return None
    except jwt.ExpiredSignatureError:
        st.error("Token has expired.")
        return None
    except jwt.InvalidTokenError:
        st.error("Invalid token.")
        return None

# Handle the submit button
if st.button("Submit"):
    username = st.session_state["username"]
    password = st.session_state["password"]
    
    #Call the login function to get the JWT token
    ans = login(username, password)
    
    if ans:
        jwt_token = ans.get("jwt")  # Extract JWT token from the response
        
        if jwt_token:
            #Decode the JWT token and extract the authority (role)
            user_role = decode_jwt(jwt_token)

            if user_role:
                # Store role and token in session state
                st.session_state["user_role"] = user_role
                st.session_state["jwt_token"] = jwt_token
                
                # st.write(f"User role: {user_role}")
                
                # Redirect to the appropriate page based on role
                if user_role == "ROLE_ADMIN":
                    st.switch_page(page="pages/Admin_👨‍💻.py")
                elif user_role == "ROLE_PREMIUM":
                    st.switch_page(page="pages/Premium_User_🤴.py")
                elif user_role == "ROLE_USER":
                    st.switch_page(page="pages/General_User_💁.py")
                else:
                    st.error("Unknown role.")
            else:
                st.error("Failed to extract user role.")
        else:
            st.error("No JWT token found.")
    else:
        st.error("Login failed.")

