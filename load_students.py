
__STUDENTS_FILENAME__ = 'students.txt'


def load_students():
    with open(__STUDENTS_FILENAME__, 'r', encoding='utf8') as students_file:
        students_str = students_file.read()
        students_lst = []
        for student in students_str.split('\n'):
            if student is not '':
                students_lst.append(student)
        return students_lst
