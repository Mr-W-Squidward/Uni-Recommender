import streamlit as st
import bcrypt
from pymongo import MongoClient
import pandas as pd
import datapuller
import random
import os
import base64

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['university_courses']
users_collection = db['users']
course_collection = db['user_courses']
recommended_collection = db['recommended_programs']

# Password encryption
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# Function to toggle forms
def toggle_forms():
    st.session_state.show_register = not st.session_state.show_register
    if st.session_state.show_register:
        st.session_state.register_data = {
            'new_username': '',
            'new_password': '',
            'new_password_confirm': ''
        }

def logout():
    st.session_state.logged_in = False
    st.session_state.current_user = None

def load_required_courses():
    return pd.read_csv('.\HawkHacksDBV2 - Sheet1.csv')

# Image base64
def get_image_base64(image_paths):
    base64_images = []
    for image_path in image_paths:
        if not os.path.exists(image_path):
            st.error(f"Image file not found: {image_path}")
        else:
            with open(image_path, "rb") as image_file:
                base64_images.append(base64.b64encode(image_file.read()).decode())
    return base64_images

# Image paths for each university
def image_path(university):
    base_path = os.path.join(os.path.expanduser('~'), 'streamlitthing', 'imagess')
    image_files = {
        "Wilfrid Laurier University Waterloo": ["laurier1.png", "laurier2.jpg", "laurier3.jpg"],
        "Toronto Metropolitan University": ["tmu1.jpg", "tmu2.jpg", "tmu3.jpg"],
        "Wilfrid Laurier University (Brantford)": ["laurierb1.jpg", "laurierb2.jpg", "laurierb3.jpg"],
        "University of Waterloo": ["waterloo1.jpg", "waterloo2.png", "waterloo3.jpg"],
        "University of Toronto (St. George)": ["uoft1.jpg", "uoft2.jpg", "uoft3.jpg"],
    }
    return [os.path.join(base_path, img) for img in image_files.get(university, ["laurier1.png"])]

def initialize_image_index(university):
    if f'{university}_image_index' not in st.session_state:
        st.session_state[f'{university}_image_index'] = 0

def get_university_images(university):
    initialize_image_index(university)
    image_list = image_path(university)
    current_index = st.session_state[f'{university}_image_index']
    return image_list, current_index

def change_image_index(university, direction):
    image_list, current_index = get_university_images(university)
    if direction == "next":
        st.session_state[f'{university}_image_index'] = (current_index + 1) % len(image_list)
    else:
        st.session_state[f'{university}_image_index'] = (current_index - 1) % len(image_list)

st.set_page_config(
    page_title="University Matcher",
    page_icon=":shark:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("University Matcher")

if 'show_register' not in st.session_state:
    st.session_state.show_register = False

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

if 'available_courses' not in st.session_state:
    st.session_state.available_courses = {
        "MCV4U", "MHF4U", "MDM4U", "SPH4U", "SCH4U", "SBI4U", "ENG4U", "EWC4U", "AMU4M", "AVI4M",
        "ATC4M", "ADA4M", "ASM4M", "BAT4M", "BBM4M", "BOH4M", "CGW4U", "CGU4M", "CGR4M", "CGO4M",
        "CHI4U", "CHY4U", "CIA4U", "CLN4U", "CPW4U", "LVV4U", "ICS4U", "FSF4U", "FEF4U", "FIF4U",
        "PLF4M", "PSK4U", "HZT4U", "HSB4U", "HFA4U", "HHS4U", "HHG4M", "HNB4M", "HSE4M", "HSC4M",
        "TPJ4M", "TMJ4M", "TDJ4M", "TGJ4M", "TEJ4M", "THJ4M"
    }

# Recalculate recommended programs
def calculate_recommended_programs():
    courses_from_db = list(course_collection.find({'username': st.session_state.current_user}))

    st.session_state.course_data = {course['course_code']: course['grade'] for course in courses_from_db}

    # Compare entered courses with required courses and find recommended programs
    recommended_programs = datapuller.get_recommended_programs(st.session_state.course_data)
    random.shuffle(recommended_programs)
    
    if recommended_programs is not None and len(recommended_programs) > 0:
        recommended_collection.delete_many({'username': st.session_state.current_user})
        
        for program in recommended_programs:
            if isinstance(program, dict):
                program_data = {
                    'username': st.session_state.current_user,
                    'university': program.get('University'),
                    'degree': program.get('Degree'),
                    'program': program.get('Program'),
                    'minimum_grade': program.get('Minimum Grade')
                }
                recommended_collection.insert_one(program_data)
            else:
                st.error("Invalid data format for recommended program.")
        st.session_state.recommended_programs_stored = True
        st.write("Recommended Programs stored successfully.")
    else:
        st.session_state.recommended_programs_stored = False
        st.error("You do not meet the required courses criteria or no programs found.")

# Logout
if st.session_state.logged_in:
    st.sidebar.header(f"Welcome, {st.session_state.current_user}")
    if st.sidebar.button("Logout"):
        logout()
        st.experimental_rerun()

    if 'available_courses' not in st.session_state:
        st.session_state.available_courses = set([
            "MCV4U", "MHF4U", "MDM4U", "SPH4U", "SCH4U", "SBI4U", "ENG4U", "EWC4U", "AMU4M", "AVI4M",
            "ATC4M", "ADA4M", "ASM4M", "BAT4M", "BBM4M", "BOH4M", "CGW4U", "CGU4M", "CGR4M", "CGO4M",
            "CHI4U", "CHY4U", "CIA4U", "CLN4U", "CPW4U", "LVV4U", "ICS4U", "FSF4U", "FEF4U", "FIF4U",
            "PLF4M", "PSK4U", "HZT4U", "HSB4U", "HFA4U", "HHS4U", "HHG4M", "HNB4M", "HSE4M", "HSC4M",
            "TPJ4M", "TMJ4M", "TDJ4M", "TGJ4M", "TEJ4M", "THJ4M"
        ])

    # Get rid of None values before sorting
    filtered_courses = [course for course in st.session_state.available_courses if course is not None]
    sorted_courses = sorted(filtered_courses)  # Sort courses alphabetically

    with st.form(key='course_form'):
        course_code = st.selectbox('Course Code', sorted_courses)
        grade = st.number_input('Percentage Grade (%)', min_value=0, max_value=100)

        if 'course_data' not in st.session_state:
            st.session_state.course_data = {}

        submit_button = st.form_submit_button(label="Add Course")

    if submit_button:
        if (0 <= grade <= 100):
            st.session_state.course_data[course_code] = grade
            course_collection.insert_one({'username': st.session_state.current_user, 'course_code': course_code, 'grade': grade})
            st.session_state.available_courses.remove(course_code)
            st.success(f"Successfully added course: {course_code} with grade: {grade}%")
            st.experimental_rerun()  # Refresh the page after adding a course
        else:
            st.error("Please enter a valid grade between 0 and 100.")

    st.subheader("Courses Entered:")

    courses_from_db = list(course_collection.find({'username': st.session_state.current_user}))
    filtered_courses_from_db = [course for course in courses_from_db if course.get('course_code') is not None]
    courses_from_db_sorted = sorted(filtered_courses_from_db, key=lambda x: x['course_code'])

    for index, course in enumerate(courses_from_db_sorted):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.write(course['course_code'])
        with col2:
            st.write(course['grade'], '%')
        with col3:
            remove_button_key = f"remove_button_{index}"
            if st.button(f"Remove {course['course_code']}", key=remove_button_key):
                st.session_state.available_courses.add(course['course_code'])
                course_collection.delete_one({'_id': course['_id']})
                st.experimental_rerun()

    if st.button("Find Programs"):
        calculate_recommended_programs()

    # Display recommended programs only if found
    if 'recommended_programs_stored' in st.session_state and st.session_state.recommended_programs_stored:
        st.subheader("Recommended Programs:")
        recommended_programs = list(recommended_collection.find({'username': st.session_state.current_user}))
        if recommended_programs:
            grouped_programs = {}
            for program in recommended_programs:
                university = program['university']
                if university not in grouped_programs:
                    grouped_programs[university] = []
                grouped_programs[university].append(program)

            for university, programs in grouped_programs.items():
                st.write(f"**{university}**")
                program_image_paths = image_path(university)
                program_image_base64 = get_image_base64(program_image_paths)

                if program_image_base64:
                    initialize_image_index(university)
                    current_index = st.session_state[f'{university}_image_index']
                    image_url = f"data:image/png;base64,{program_image_base64[current_index]}"
                    st.image(image_url, use_column_width=True)
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if st.button("Previous", key=f"prev_{university}"):
                            change_image_index(university, "prev")
                            st.experimental_rerun()
                    with col2:
                        if st.button("Next", key=f"next_{university}"):
                            change_image_index(university, "next")
                            st.experimental_rerun()

                for program in programs:
                    st.write(f"{program['degree']} - {program['program']} (Min Grade: {int(program['minimum_grade'] * 100)}%)")
        
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