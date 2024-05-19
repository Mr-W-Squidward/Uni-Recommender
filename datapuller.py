import pandas as pd

def get_recommended_programs(user_courses):
    # Load the CSV file
    df = pd.read_csv('./HawkHacksDBV2 - Sheet1.csv')

    # Filter only relevant columns (from column 4 onwards) and the 'Minimum Grade' column
    course_columns = df.columns[3:47]
    df = df[['University', 'Degree', 'Program'] + list(course_columns) + ['Minimum Grade']]

    # Initialize a list to hold recommended programs
    recommended_programs = []

    for index, row in df.iterrows():
        required_courses = row[course_columns]
        min_grade = row['Minimum Grade']

        meets_requirements = True
        for course in course_columns:
            if required_courses[course] and (course not in user_courses or user_courses[course] < min_grade):
                meets_requirements = False
                break

        if meets_requirements:
            recommended_programs.append({
                'University': row['University'],
                'Degree': row['Degree'],
                'Program': row['Program'],
                'Minimum Grade': min_grade
            })

    return recommended_programs