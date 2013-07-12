from flask import Flask, render_template, request, redirect
import hackbright_app

app = Flask(__name__)

# Code goes here

# @app.route("/")
# def helloworld():
#     return "Hello world \n we are awesome"

@app.route("/student")
def get_student():
    hackbright_app.connect_to_db()
    student_github = request.args.get("github")
    row = hackbright_app.get_student_by_github(student_github)
    html = render_template("student_info.html", first_name=row[0], 
                                                last_name=row[1], 
                                                github=row[2])
    return html

@app.route("/grade")
def get_grade():
    hackbright_app.connect_to_db()
    student_github = request.args.get("github")
    rows = hackbright_app.show_grades_by_student(student_github)
    print "this is working - woot"
    print "row is %r" %rows
    html = render_template("student_grades.html", projects=rows)
    return html

@app.route("/new_student")
def make_student():
    return render_template("new_student.html")

@app.route("/create_student")
def create_student():
    hackbright_app.connect_to_db()

    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    student_github = request.args.get("github")

    hackbright_app.make_new_student(first_name, last_name, student_github)
    return redirect("/student?github="+student_github)

# @app.route("/new_project")
# def make_project():
#     return render_template("new_project.html")

# @app.route("/create_project")
# def create_project():
#     hackbright_app.connect_to_db()

#     title = request.args.get("title")
#     description



@app.route("/new_grade")
def make_grade():
    return render_template("assign_grade.html")

@app.route("/assign_grade")
def assign_grade():
    hackbright_app.connect_to_db()

    student_github = request.args.get("student_github")
    project_title = request.args.get("project_title")
    grade = request.args.get("grade")

    hackbright_app.assign_grade(student_github, project_title, grade)
    return redirect("/grade?github="+student_github)

@app.route("/")
def get_github():
    return render_template("get_github.html")
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    student_github = request.args.get("github")


    # return hackbright_app.get_student_by_github(student_github)

if __name__=="__main__":
    app.run(debug=True)