from typing import List
from college import Student, Course
import utils

def calculate_gpa(student: Student, courses: List[Course]) -> float:
    '''
    This function takes a student and a list of course
    It should compute the GPA for the student
    The GPA is the sum(hours of course * grade in course) / sum(hours of course)
    The grades come in the form: 'A+', 'A' and so on.
    But you can convert the grades to points using a static method in the course class
    To know how to use the Student and Course classes, see the file "college.py"  
    '''
    #TODO: ADD YOUR CODE HERE
    sum_hours_grade=0
    sum_hours=0
    for element in courses:
        #Search for the student in the courses grades to ensure no partial or zero coverage
        if student.id in element.grades:
            sum_hours_grade+=element.hours*element.convert_grade_to_points(element.grades[student.id])
            sum_hours+=element.hours

    #To avoid division by 0
    if sum_hours==0:
        return 0.0
    return sum_hours_grade/sum_hours