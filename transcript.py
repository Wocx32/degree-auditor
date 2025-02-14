import re
from pprint import pprint
from requests import Session
from bs4 import BeautifulSoup
from datetime import datetime, UTC

from config import *

base_url = 'https://mysis-fccollege.empower-xl.com'
url = f'{base_url}/fusebox.cfm'
home_url = f'{base_url}/empower/fusebox.cfm'
trascript_url = f'{home_url}?fuseaction=WEBSRQ04'
login_url = f'{base_url}/ptl-includes/authentication/auth-onlogin.cfm'



def get_semesters():
    
    sess = Session()
    sess.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
    })

    page = sess.get(url)

    params = {
        "empower_usrn": username,
        "empower_pswd": password,
        "LoggedInToEmpower": "1",
        "logoninfo": datetime.now(tz=UTC).strftime('%m/%d/%Y %H:%M:%S'),
        "LoginToEmpower.x": "0",
        "LoginToEmpower.y": "0",
    }

    sess.post(login_url, data=params)
    page = sess.get(trascript_url).content

    soup = BeautifulSoup(page, 'html.parser')
    data = soup.find('div', id='UClass')
    pattern = re.compile(r'\bUClass\d*\b')

    semesters = data.find_all(id=pattern)

    sem_names = []
    
    rows = data.find_all('a')
    for i in rows:
        sem_names.append(i.text[9:].strip())


    sem_data = []

    for sem in semesters:
        rows = sem.find_all('tr')
        sem_data.append(clean_semester_data(extract_data(rows[1:-1])))

    sem_data = list(zip(sem_names, sem_data))

    return sem_data



def extract_data(rows):

    data = []

    for row in rows:
        
        td = row.find_all('td')
        
        contents = []

        for i in range(len(td)):

            if i == 0:
                if td[i].text.strip() == '':
                    data[-1][-1] = True
                    break

            if td[i].text.strip() != '':
                contents.append(td[i].text.strip())
            else:
                continue
        

        if contents:
            contents.append(False)
            data.append(contents)

    return data


def clean_semester_data(data: list):

    cleaned_semester_data = []

    for course in data:

        cleaned_data = {
            'dept': course[0],
            'crse': course[1],
            'sec': course[2],
            'title': course[3],
            'days': course[4],
            'time': course[5],
            'building': f'{course[6]} {course[7]}',
            'instr': course[8],
            'gr': course[9],
        }

        if len(course) > 11:
            cleaned_data['att'] = course[10]
            cleaned_data['ern'] = course[11]
            cleaned_data['pts'] = course[12]
            cleaned_data['is_lab'] = course[13]

        else:
            cleaned_data['att'] = None
            cleaned_data['ern'] = None
            cleaned_data['pts'] = None
            cleaned_data['is_lab'] = course[10]

        cleaned_semester_data.append(cleaned_data)
    
    return cleaned_semester_data



if __name__ == '__main__':

    pprint(get_semesters())