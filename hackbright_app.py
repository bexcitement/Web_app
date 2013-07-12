import sqlite3
import shlex

DB = None
CONN = None

def get_student_by_github(github):
    try:
        query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
        DB.execute(query, (github,))
        row = DB.fetchone()
        return row  # we removed some nonsensical  -- wtf peeps?
        # Student: %s %s
        # Github account: %s % (row[0], row[1], row[2])
    except TypeError:
        print "Error: there is no student with that github handle."


def show_grades_by_student(github):
    query = """SELECT Grades.project_title, Grades.grade
                FROM Grades
                INNER JOIN Students
                ON Grades.student_github = Students.github
                WHERE Students.github = ?"""
    DB.execute(query, (github,))
    rows = DB.fetchall()
    # print """\
    # Grades for student %s:""" % github
    print "github is %r" %github
    return rows
 
def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)

def add_project(title, description, max_grade):
    try:
        query = """INSERT INTO Projects values (?, ?, ?)"""
        DB.execute(query, (title, description, max_grade))
        CONN.commit()
        print "Successfully added project %s with maximum grade %s" % (title, max_grade)
    except:
        print "There was a problem adding the project to the database."    

def find_project_by_title(title):
    try:
        query = """SELECT title, description, max_grade FROM Projects WHERE title = ?"""
        DB.execute(query, (title,))
        row = DB.fetchone()
        print """\
        Project title: %s
        Description: %s
        Maximum grade: %s""" % (row[0], row[1], row[2])
    except TypeError:
        print "Error: There is no project by that name."


def find_grade(github, project_title):
    try:
        query = """SELECT Students.first_name, Students.last_name,
                          Grades.project_title, Grades.grade
                    FROM Students
                    INNER JOIN Grades
                    ON Students.github = Grades.student_github
                    WHERE Students.github = ?
                    AND Grades.project_title = ?"""
        DB.execute(query, (github, project_title))
        row = DB.fetchone()
        print """\
        Student name: %s %s
        Project title: %s
        Grade: %s""" % (row[0], row[1], row[2], row[3])
    except:
        print "Error: something went wrong with finding the grade."

def assign_grade(student_github, project_title, grade):
    try:
        query = """INSERT INTO Grades values (?, ?, ?)"""
        DB.execute(query, (student_github, project_title, grade))
        CONN.commit()
        print "Successfully added %s's grade for project %s" % (student_github, project_title)
    except:
        print "There was a problem adding the grade to the database."


def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = shlex.split(input_string)
        command = tokens[0]
        args = tokens[1:]
        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "find_project":
            find_project_by_title(*args)
        elif command == "add_project":
            add_project(*args)
        elif command == "find_grade":
            find_grade(*args)
        elif command == "assign_grade":
            assign_grade(*args)
        elif command == "show_grades":
            show_grades_by_student(*args)

    CONN.close()

if __name__ == "__main__":
    main()
