import streamlit as st
from streamlit.components.v1 import html
import os
import base64


base_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'hawkhack24unidatabase-1', 'imagess')


def get_image_base64(image_path):
    if not os.path.exists(image_path):
        st.error(f"Image file not found: {image_path}")
        return ""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def image_path(university):
    if university == "Wilfrid Laurier University Waterloo":
        return os.path.join(base_path, "laurier.png")
    elif university == "Toronto Metropolitan University":
        return os.path.join(base_path, "tmu.jpeg")
    elif university == "Wilfrid Laurier University (Brantford)":
        return os.path.join(base_path, "laurierB.jpg")
    elif university == "University of Waterloo":
        return os.path.join(base_path, "waterloo.jpg")
    elif university == "University of Toronto (St. George)":
        return os.path.join(base_path, "uoft.jpg")
    else:
        return os.path.join(base_path, "laurier.png")


data = {
    "Engineering": [
        {"university": "University A", "program": "Engineering Program 1"},
        {"university": "University B", "program": "Engineering Program 2"},
    ],
    "Commerce": [
        {"university": "University C", "program": "Business Program 1"},
        {"university": "University D", "program": "Business Program 2"},
    ],
    "Science": [
        {"university": "University E", "program": "Science Program 1"},
        {"university": "University F", "program": "Science Program 2"},
    ],
    "Arts": [
        {"university": "University G", "program": "Arts Program 1"},
        {"university": "University H", "program": "Arts Program 2"},
    ],
    "Fine Arts": [
        {"university": "University G", "program": "Arts Program 1"},
        {"university": "University H", "program": "Arts Program 2"},
    ],
    "Business Administration": [
        {"university": "University G", "program": "Arts Program 1"},
        {"university": "University H", "program": "Arts Program 2"},
    ],
    "Tech": [
        {"university": "University G", "program": "Arts Program 1"},
        {"university": "University H", "program": "Arts Program 2"},
    ]
}



st.markdown("""
    <style>
        .faculty-section {
            margin-bottom: 30px;
        }
        .carousel {
            margin-top: 20px;
        }
        .card {
            margin: 20px;
            
        }
        .carousel-inner {
            display: flex;
            justify-content: center;
        }
        .carousel-item {
            display: flex;
            justify-content: center; 
            align-items: center;
        }
            
        .box {
            width: 100%;
            max-width: 70rem;
        }
    </style>
""", unsafe_allow_html=True)


st.title("University Programs Recs!")


col1, col2 = st.columns([3,3])

col_iterator = iter([col1, col2])

for idx, (faculty, programs) in enumerate(data.items()):
    if idx % 2 == 0:
       
        col1, col2 = st.columns([7,7])
        
        col_iterator = iter([col1, col2])
    
    with next(col_iterator):
        st.markdown(f"<div class='faculty-section'><h2 style='text-align: center; font-size: 25px'>{faculty}</h2></div>", unsafe_allow_html=True)
        
       
        carousel_html = f"""
        <div id="carousel{faculty.replace(' ', '')}" class="carousel slide" data-ride="carousel">
          <div class="carousel-inner">
        """

        for idx, item in enumerate(programs):
            active_class = "active" if idx == 0 else ""
            img_path = image_path(item['university'])
            img_base64 = get_image_base64(img_path)
            carousel_html += f"""
            <div class="carousel-item {active_class}">
              <div class="card" style="width: 18rem; margin: auto;">
                <img class="card-img-top" src="data:image/jpg;base64,{img_base64}" alt="{item['university']}">
                <div class="card-body" style="display: flex; flex-direction: column; justify-content: center; align-items: center;">
                  <h5 class="card-title">{item['university']}</h5>
                  <p class="card-text">{item['program']}</p>
                </div>
              </div>
            </div>
            """

        carousel_html += f"""
          </div>
          <a class="carousel-control-prev" href="#carousel{faculty.replace(' ', '')}" role="button" data-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="sr-only">Previous</span>
          </a>
          <a class="carousel-control-next" href="#carousel{faculty.replace(' ', '')}" role="button" data-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="sr-only">Next</span>
          </a>
        </div>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
        """

        html(carousel_html, height=600)
