import streamlit as st

st.title("University Matcher")

if 'available_courses' not in st.session_state:
  st.session_state.available_courses = {
    "MCV4U", "MHF4U", "MDM4U", "SPH4U", "SCH4U", "SBI4U", "ENG4U", "EWC4U", "AMU4M", "AVI4M", 
    "ATC4M", "ADA4M", "ASM4M", "BAT4M", "BBM4M", "BOH4M", "CGW4U", "CGU4M", "CGR4M", "CGO4M",
    "CHI4U", "CHY4U", "CIA4U", "CLN4U", "CPW4U", "LVV4U", "ICS4U", "FSF4U", "FEF4U", "FIF4U",
    "PLF4M", "PSK4U", "HZT4U", "HSB4U", "HFA4U", "HHS4U", "HHG4M", "HNB4M", "HSE4M", "HSC4M",
    "TPJ4M", "TMJ4M", "TDJ4M", "TGJ4M", "TEJ4M", "THJ4M" # Available 4U Courses
  }

with st.form(key='course_form'):
  course_code = st.selectbox('Course Code', st.session_state.available_courses)
  grade = st.number_input('Percentage Grade (%)')

  submit_button = st.form_submit_button(label="Add Course")

if submit_button:
  if 'courses' not in st.session_state:
    st.session_state.courses = []

  if (0 <= grade <= 100):
    st.session_state.courses.append({'course_code': course_code, 'grade': grade})
    st.session_state.available_courses.remove(course_code)
    st.success(f"Successfully added course: {course_code} with grade: {grade}%")

# Show courses and removal button
if st.session_state.get('courses', []):
    st.write("Added Courses: ")
    courses_copy = st.session_state.courses[:]  # Copy courses list
    for course in courses_copy:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.write(course['course_code'])
        with col2:
            st.write(course['grade'], '%')
        with col3:
            if st.button(f"Remove {course['course_code']}", on_click=None):
                st.session_state.available_courses.add(course['course_code'])
                st.session_state.courses.remove(course)
                courses_to_display = st.session_state.courses[:]
