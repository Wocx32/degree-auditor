
import random
from transcript import get_semesters
from degree_requirements import *
from pprint import pprint


def audit_bcs(complete_semester_data):
    
    requirements = BCS.copy()

    for semester in complete_semester_data[::-1]:
        for course in semester[1]:

            dept = course['dept']
            crse = course['crse']
            course_code = f'{dept} {crse}'

            if course['gr'].split(u'\xa0')[0] in unacceptable_grades:
                continue

            if requirements.get(course_code):
                requirements[course_code] -= 1

            elif dept in departments['humanities'] and requirements['humanities'] > 0:
                requirements['humanities'] -= 1

            elif dept in departments['social_sciences'] and requirements['social_sciences'] > 0:
                requirements['social_sciences'] -= 1

            elif dept in departments['humanities'] and requirements['humanities'] == 0:
                requirements['uni_electives'] -= 1

            elif dept in departments['social_sciences'] and requirements['social_sciences'] == 0:
                requirements['uni_electives'] -= 1

            elif dept in departments['science_lab_cs'] and course['is_lab']:
                requirements['science_lab_cs'] -= 1

            elif dept == 'COMP' or dept == 'CSCS':
                requirements['comp_electives'] -= 1

            else:
                user_inp = input(f"Course {course_code} not in database. Enter (1) add to humanities, (2) add to social sciences, (3) add to uni electives, (4) gamble: ")
                if user_inp == '1':
                    requirements['humanities'] -= 1
                elif user_inp == '2':
                    requirements['social_sciences'] -= 1
                elif user_inp == '3':
                    requirements['uni_electives'] -= 1
                else:
                    selected = random.choice(['humanities', 'social_sciences', 'uni_electives'])
                    requirements[selected] -= 1
    
    
    pprint(requirements)

if __name__ == '__main__':
    audit_bcs(get_semesters())
