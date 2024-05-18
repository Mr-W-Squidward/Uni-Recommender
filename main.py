import streamlit as st
import bcrypt
from pymongo import MongoClient

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['university_courses']
users_collection = db['users']
course_collection = db['user_courses']

st.title("University Matcher")

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# Initialize session state for form toggle
if 'show_register' not in st.session_state:
    st.session_state.show_register = False

# Initialize session state for form data
if 'register_data' not in st.session_state:
    st.session_state.register_data = {
        'new_username': '',
        'new_password': '',
        'new_password_confirm': ''
    }

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Toggle form display
def toggle_forms():
    st.session_state.show_register = not st.session_state.show_register
    if st.session_state.show_register:
        st.session_state.register_data = {
            'new_username': '',
            'new_password': '',
            'new_password_confirm': ''
        }

# Logout function
def logout():
    st.session_state.logged_in = False
    st.session_state.current_user = None

# Logout
if st.session_state.logged_in:
    st.sidebar.header(f"Welcome, {st.session_state.current_user}")
    if st.sidebar.button("Logout"):
        logout()
        st.experimental_rerun()

    if 'available_courses' not in st.session_state:
        # 4U Course List
        st.session_state.available_courses = {
            "MCV4U", "MHF4U", "MDM4U", "SPH4U", "SCH4U", "SBI4U", "ENG4U", "EWC4U", "AMU4M", "AVI4M", 
            "ATC4M", "ADA4M", "ASM4M", "BAT4M", "BBM4M", "BOH4M", "CGW4U", "CGU4M", "CGR4M", "CGO4M",
            "CHI4U", "CHY4U", "CIA4U", "CLN4U", "CPW4U", "LVV4U", "ICS4U", "FSF4U", "FEF4U", "FIF4U",
            "PLF4M", "PSK4U", "HZT4U", "HSB4U", "HFA4U", "HHS4U", "HHG4M", "HNB4M", "HSE4M", "HSC4M",
            "TPJ4M", "TMJ4M", "TDJ4M", "TGJ4M", "TEJ4M", "THJ4M"
        }

    with st.form(key='course_form'):
        # Course input
        course_code = st.selectbox('Course Code', st.session_state.available_courses)
        grade = st.number_input('Percentage Grade (%)', min_value=0, max_value=100)

        submit_button = st.form_submit_button(label="Add Course")

    if submit_button:
        # Course validation
        if (0 <= grade <= 100):
            course_collection.insert_one({'username': st.session_state.current_user, 'course_code': course_code, 'grade': grade})
            st.session_state.available_courses.remove(course_code)
            st.success(f"Successfully added course: {course_code} with grade: {grade}%")
            st.experimental_rerun()  # Refresh the page to update the list of courses

    # Show courses and removal button
    courses_from_db = list(course_collection.find({'username': st.session_state.current_user}))
    if courses_from_db:
        st.write("Added Courses: ")
        for index, course in enumerate(courses_from_db):
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                st.write(course['course_code'])
            with col2:
                st.write(course['grade'], '%')
            with col3:
                # Remove course button
                remove_button_key = f"remove_button_{index}"
                if st.button(f"Remove {course['course_code']}", key=remove_button_key):
                    st.session_state.available_courses.add(course['course_code'])
                    course_collection.delete_one({'_id': course['_id']})
                    st.experimental_rerun()
else:
    if st.session_state.show_register:
        st.sidebar.header("Create a New Account")
        st.sidebar.button("Back To Login", on_click=toggle_forms)
        st.session_state.register_data['new_username'] = st.sidebar.text_input("New Username", value=st.session_state.register_data['new_username'])
        st.session_state.register_data['new_password'] = st.sidebar.text_input("New Password", type="password", value=st.session_state.register_data['new_password'])
        st.session_state.register_data['new_password_confirm'] = st.sidebar.text_input("Confirm New Password", type="password", value=st.session_state.register_data['new_password_confirm'])

        if st.sidebar.button("Register"):
            new_username = st.session_state.register_data['new_username']
            new_password = st.session_state.register_data['new_password']
            new_password_confirm = st.session_state.register_data['new_password_confirm']

            if new_username and new_password and new_password == new_password_confirm:
                existing_user = users_collection.find_one({'username': new_username})
                if existing_user:
                    st.sidebar.error("Username already exists. Please choose another.")
                else:
                    hashed_password = hash_password(new_password)
                    users_collection.insert_one({'username': new_username, 'password': hashed_password})
                    st.sidebar.success("User registered successfully. Please log in.")
                    toggle_forms()
            else:
                st.sidebar.error("Please provide matching passwords and a username.")
    else:
        st.sidebar.header("Login")
        st.sidebar.button("Create a New Account", on_click=toggle_forms)
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            user = users_collection.find_one({'username': username})
            if user and check_password(password, user['password']):
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.experimental_rerun()
            else:
                st.sidebar.error('Username/password is incorrect')

# Implement image carousel with learn more button n stuff for universities after backend done