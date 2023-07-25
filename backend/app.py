from werkzeug.utils import escape
import numpy as np
from wtforms.validators import InputRequired, DataRequired, Length
from wtforms import StringField, TextAreaField, SubmitField, SelectField, IntegerField
from wtforms.fields import DateField
from flask_wtf import FlaskForm
from flask_cors import CORS
import datetime
from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify


app = Flask(__name__, template_folder='templates')
CORS(app)

# Flash needs some session info, and session does not work without secret key
app.config["SECRET_KEY"] = "secretkey"

app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = "3286"
app.config['MYSQL_DB'] = 'quizapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['MYSQL_PORT'] = 3306


mysql = MySQL(app)


class NewQuizForm(FlaskForm):
    duration = IntegerField("duration", validators=[InputRequired("Input is required!"),
                                                    DataRequired(
        "Data is required")])
    dt = DateField('DatePicker', format='%Y-%m-%d')
    dt_last = DateField('DatePicker', format='%Y-%m-%d')

    hour1 = SelectField("hour1", coerce=int, choices=[
        (0, '00'), (1, '01'), (2, '02'),
        (3, '03'), (4, '04'), (5, '05'),
        (6, '06'), (7, '07'), (8, '08'),
        (9, '09'), (10, '10'), (11, '11')])

    minutes1 = SelectField("minutes1", coerce=int, choices=[
        (0, '00'), (1, '05'), (2, '10'),
        (3, '15'), (4, '20'), (5, '25'),
        (6, '30'), (7, '35'), (8, '40'),
        (9, '45'), (10, '50'), (11, '55')])

    ampm = SelectField("ampm", coerce=int, choices=[(0, 'am'), (1, 'pm')])

    hour2 = SelectField("hour2", coerce=int, choices=[
        (0, '00'), (1, '01'), (2, '02'),
        (3, '03'), (4, '04'), (5, '05'),
        (6, '06'), (7, '07'), (8, '08'),
        (9, '09'), (10, '10'), (11, '11')])

    minutes2 = SelectField("minutes2", coerce=int, choices=[
        (0, '00'), (1, '05'), (2, '10'),
        (3, '15'), (4, '20'), (5, '25'),
        (6, '30'), (7, '35'), (8, '40'),
        (9, '45'), (10, '50'), (11, '55')])
    ampm2 = SelectField("ampm2", coerce=int, choices=[(0, 'am'), (1, 'pm')])
    # totalScorePossible = SelectField("totalScorePossible", coerce=int, choices=[
    #    (0, 0), (1, 10), (2, 20),
    #    (3, 30), (4, 40), (5, 50),
    #    (6, 60), (7, 70), (8, 80),
    #    (9, 90), (10, 100)])
    submit = SubmitField("submit")


class QuestionForm(FlaskForm):
    coursename = StringField("coursename", validators=[InputRequired("Input is required!"),
                                                       DataRequired(
                                                           "Data is required"),
                                                       Length(min=5, max=1000, message="Input must be between 5 and 1000 characters long.")])
    description = TextAreaField("Description", validators=[InputRequired("Input is required!"),
                                                           DataRequired(
                                                               "Data is required"),
                                                           Length(min=5, max=1000, message="Input must be between 5 and 1000 characters long.")])
    choice1 = TextAreaField("Choice1", validators=[InputRequired("Input is required!"),
                                                   DataRequired(
                                                       "Data is required"),
                                                   Length(min=5, max=1000, message="Input must be between 5 and 1000 characters long.")])
    choice2 = TextAreaField("Choice2", validators=[InputRequired("Input is required!"),
                                                   DataRequired(
                                                       "Data is required"),
                                                   Length(min=5, max=1000, message="Input must be between 5 and 1000 characters long.")])
    choice3 = TextAreaField("Choice3", validators=[InputRequired("Input is required!"),
                                                   DataRequired(
                                                       "Data is required"),
                                                   Length(min=5, max=1000, message="Input must be between 5 and 1000 characters long.")])
    choice4 = TextAreaField("Choice4", validators=[InputRequired("Input is required!"),
                                                   DataRequired(
                                                       "Data is required"),
                                                   Length(min=5, max=1000, message="Input must be between 5 and 1000 characters long.")])
    choice5 = TextAreaField("Choice5")
    choice6 = TextAreaField("Choice6")
    correctanswer = SelectField("CorrectAnswer", coerce=int, choices=[
        (0, 1), (1, 2), (2, 3),
        (3, 4), (4, 5), (5, 6)])


class NewQuestionForm(QuestionForm):
    submit = SubmitField("Submit")


class DeleteQuestionForm(FlaskForm):
    submit = SubmitField("Delete question")


class DeleteQuizForm(FlaskForm):
    submit = SubmitField("Delete quiz")


class EditQuestionForm(QuestionForm):
    submit = SubmitField("Update question")


class EditQuizForm(NewQuizForm):
    submit = SubmitField("Update quiz")


class FilterForm(FlaskForm):
    coursename = SelectField("CourseName", coerce=int)
    description = StringField("Description", validators=[Length(max=20)])
    sortby = SelectField("Sortby", coerce=int, choices=[
                         (0, "---"), (1, "Oldest to newest"), (2, "Newest to oldest")])
    submit = SubmitField("Filter")


# We need the GET method because we need to show the form in new template
@app.route("/question/<int:question_id>/edit", methods=["GET", "POST"])
def edit_question(question_id):
    cur = mysql.connection.cursor()
    cur.execute("USE quizapp")
    cur.execute(
        """SELECT * FROM Questions WHERE Question_ID=%s ORDER BY Question_ID DESC""", (question_id,))
    row = cur.fetchone()

    try:
        question = {
            'id': row["Question_ID"],
            'coursename': row["Course_Name"],
            'description': row["Question_Desc"],
            'Choice1': row["Choice1"],
            'Choice2': row["Choice2"],
            'Choice3': row["Choice3"],
            'Choice4': row["Choice4"],
            'Choice5': row["Choice5"],
            'Choice6': row["Choice6"],
            'correctAnswer': row["Correct_Answer"]
        }
    except:
        question = {}

    if question:
        form = EditQuestionForm()
        choices = [(1, "Choice 1"), (2, "Choice 2"), (3, "Choice 3"),
                   (4, "Choice 4"), (5, "Choice 5"), (6, "Choice 6")]

        form.correctanswer.choices = choices
        if form.validate_on_submit():
            cur.execute("USE quizapp")
            cur.execute("""UPDATE Questions SET Course_Name=%s, Question_Desc=%s, Choice1=%s,
                        Choice2=%s,Choice3=%s,Choice4=%s,Choice5=%s,Choice6=%s,Correct_Answer=%s 
                        WHERE Question_ID=%s""", (
                escape(form.coursename.data),
                escape(form.description.data),
                escape(form.choice1.data),
                escape(form.choice2.data),
                escape(form.choice3.data),
                escape(form.choice4.data),
                escape(form.choice5.data),
                escape(form.choice6.data),
                escape(form.correctanswer.data),
                question_id
            ))
            mysql.connection.commit()
            flash("Question has been successfully updated!", "success")

            return redirect(url_for("question", question_id=question_id))

        form.coursename.data = question["coursename"]
        form.description.data = question["description"]
        form.choice1.data = question["Choice1"]
        form.choice2.data = question["Choice2"]
        form.choice3.data = question["Choice3"]
        form.choice4.data = question["Choice4"]
        form.choice5.data = question["Choice5"]
        form.choice6.data = question["Choice6"]
        form.correctanswer.data = question["correctAnswer"]

        return render_template("edit_question.html", question=question, form=form)
    return redirect(url_for("home"))


@app.route("/quiz/<int:quiz_id>/edit", methods=["GET", "POST"])
def edit_quiz(quiz_id):
    cur = mysql.connection.cursor()
    cur.execute("USE quizapp")
    cur.execute(
        """SELECT * FROM QuizTable WHERE QuizID=%s ORDER BY QuizID DESC""", (quiz_id,))
    row = cur.fetchone()

    try:
        quiz = {
            "QuizID": row["QuizID"],
            "Quiz_Datetime": row["Quiz_Datetime"],
            "NumofParticipants": row["NumofParticipants"],
            "NumofQuestions": row["NumofQuestions"],
            "TotalScorePossible": row["TotalScorePossible"],
            "Duration": row["Duration"],
            "Quiz_Status": row["Quiz_Status"],
            "Quiz_Start_Time": row["Quiz_Start_Time"],
            "Quiz_End_Time": row["Quiz_End_Time"]
        }
        cur.execute("USE quizapp")
        cur.execute(
            """SELECT * FROM SelectedQuestions WHERE QuizID=%s""", (quiz_id,))

        questions_db = cur.fetchall()
        try:
            questions = []
            for row in questions_db:
                question = {
                    'id': row["Question_ID"],
                    'coursename': row["Course_Name"],
                    'description': row["Question_Desc"],
                    'Choice1': row["Choice1"],
                    'Choice2': row["Choice2"],
                    'Choice3': row["Choice3"],
                    'Choice4': row["Choice4"],
                    'Choice5': row["Choice5"],
                    'Choice6': row["Choice6"],
                    'Is_Selected': 1
                }
                questions.append(question)
        except:
            questions = {}

    except:
        quiz = {}

    if quiz:
        form = EditQuizForm()

        if form.validate_on_submit() and request.method == "POST":

            question_num_array = ["{}".format(i+1)
                                  for i in range(len(questions))]
            values = []
            # Calculate the total possible score given the user inputs for each question
            for key in request.form:
                if key in question_num_array:
                    values.append(int(request.form[key]))

            now = datetime.datetime.now()
            now = now.strftime('%Y-%m-%d %H:%M:%S')

            hour_array = ['0{}'.format(i) if i < 10 else '{}'.format(i)
                          for i in range(12)]
            minutes_array = ['0{}'.format(
                i*5) if i*5 < 10 else '{}'.format(i*5) for i in range(12)]
            ampm_array = ["am", "pm"]

            if ampm_array[form.ampm.data] == "pm":
                form_hour1 = "{}".format(form.hour1.data + 12)
            else:
                form_hour1 = hour_array[form.hour1.data]
            if ampm_array[form.ampm2.data] == "pm":
                form_hour2 = "{}".format(form.hour2.data + 12)
            else:
                form_hour2 = hour_array[form.hour2.data]

            form_time1 = datetime.datetime.strptime("{} {}:{}:00".format(
                form.dt.data, form_hour1, minutes_array[form.minutes1.data]), '%Y-%m-%d %H:%M:%S')
            form_time1 = form_time1.strftime('%Y-%m-%d %H:%M:%S')
            form_time2 = datetime.datetime.strptime("{} {}:{}:00".format(
                form.dt_last.data, form_hour2, minutes_array[form.minutes2.data]), '%Y-%m-%d %H:%M:%S')
            form_time2 = form_time2.strftime('%Y-%m-%d %H:%M:%S')

            cur.execute("USE quizapp")
            cur.execute("""UPDATE QuizTable SET Quiz_Datetime=%s, NumofQuestions=%s, TotalScorePossible=%s,
                        Duration=%s, Quiz_Start_Time=%s, Quiz_End_Time=%s WHERE QuizID=%s""", (
                now,
                len(values),
                sum(values),
                escape(form.duration.data),
                form_time1,
                form_time2,
                quiz_id
            ))
            mysql.connection.commit()
            flash("Quiz {} has been successfully updated!".format(
                quiz_id), "success")

            return redirect(url_for("quiz", quiz_id=quiz_id))

        form.duration.data = quiz["Duration"]

        return render_template("edit_quiz.html", quiz=quiz, form=form, questions=questions)
    return redirect(url_for("home"))


@app.route("/question/<int:question_id>/add-to-quiz-questions", methods=["POST", "GET"])
def add_to_quiz_questions(question_id):
    cur = mysql.connection.cursor()
    cur.execute("USE quizapp")
    cur.execute(
        """SELECT * FROM Questions WHERE Question_ID=%s""", (question_id,))
    row = cur.fetchone()

    cur.execute("""SELECT * FROM SelectedQuestions""")
    selected_q = cur.fetchall()
    count_selected_questions = 0
    selected_q_id = []
    for srow in selected_q:
        count_selected_questions += 1
        selected_q_id.append(srow["Question_ID"])
    try:
        question = {
            "id": row["Question_ID"],
            "coursename": row["Course_Name"],
            "description": row["Question_Desc"],
            "Choice1": row["Choice1"],
            "Choice2": row["Choice2"],
            "Choice3": row["Choice3"],
            "Choice4": row["Choice4"],
            "Choice5": row["Choice5"],
            "Choice6": row["Choice6"],
            "correctAnswer": row["Correct_Answer"],
            "q_Score": row["Question_Score"],
            "Added_Time": row["Added_Datetime"],
            "Question_Number": count_selected_questions + 1
        }
    except:
        question = {}

    if question:
        if not question_id in selected_q_id:
            cur.execute("""INSERT INTO SelectedQuestions
                            (Question_ID, Course_Name, Question_Desc, Choice1, Choice2, Choice3, Choice4, Choice5, 
                            Choice6, Correct_Answer, Question_Score, Added_Datetime) 
                            SELECT Question_ID, Course_Name, Question_Desc, Choice1, Choice2, Choice3, Choice4, Choice5, 
                            Choice6, Correct_Answer, Question_Score, Added_Datetime 
                            FROM Questions 
                            WHERE Question_ID=%s""", (question_id,))
            mysql.connection.commit()

            flash(
                "Question has been successfully added to the selected questions.", "success")
        else:
            flash("This question already exists in selected questions.", "danger")
    else:
        flash("This question does not exist.", "danger")

    return redirect(url_for("home"))


@app.route("/question/<int:question_id>/remove-from-quiz-questions", methods=["POST", "GET"])
def remove_from_quiz_questions(question_id):
    cur = mysql.connection.cursor()
    cur.execute("USE quizapp")
    cur.execute(
        """SELECT * FROM SelectedQuestions WHERE Question_ID=%s""", (question_id,))
    row = cur.fetchone()

    try:
        question = {
            "id": row["Question_ID"],
            "coursename": row["Course_Name"],
            "description": row["Question_Desc"],
            "Choice1": row["Choice1"],
            "Choice2": row["Choice2"],
            "Choice3": row["Choice3"],
            "Choice4": row["Choice4"],
            "Choice5": row["Choice5"],
            "Choice6": row["Choice6"],
            "correctAnswer": row["Correct_Answer"],
            "q_Score": row["Question_Score"],
            "Added_Time": row["Added_Datetime"]
        }
    except:
        question = {}

    if question:
        cur.execute(
            """DELETE FROM SelectedQuestions WHERE Question_ID=%s""", (question_id,))
        mysql.connection.commit()

        flash(
            "Question has been successfully removed from the selected questions.", "success")
    else:
        flash("This question does not exist in selected questions.", "danger")

    return redirect(url_for("home"))


@app.route("/quiz/<int:quiz_id>/delete", methods=["POST"])
def delete_quiz(quiz_id):
    cur = mysql.connection.cursor()
    cur.execute("USE quizapp")
    cur.execute(
        """SELECT * FROM QuizTable WHERE QuizID=%s ORDER BY QuizID DESC""", (quiz_id,))
    row = cur.fetchone()

    try:
        quiz = {
            "QuizID": row["QuizID"],
            "Quiz_Datetime": row["Quiz_Datetime"],
            "NumofParticipants": row["NumofParticipants"],
            "NumofQuestions": row["NumofQuestions"],
            "TotalScorePossible": row["TotalScorePossible"],
            "Duration": row["Duration"],
            "Quiz_Status": row["Quiz_Status"],
            "Quiz_Start_Time": row["Quiz_Start_Time"],
            "Quiz_End_Time": row["Quiz_End_Time"]
        }
    except:
        quiz = {}

    if quiz:
        cur.execute(
            """DELETE FROM QuizTable WHERE QuizID = %s ;""", (quiz_id,))
        mysql.connection.commit()

        flash("Quiz {} has been successfully deleted.".format(quiz_id), "success")
    else:
        flash("This quiz {} does not exist.".format(quiz_id), "danger")

    return redirect(url_for("home"))


@app.route("/question/<int:question_id>/delete", methods=["POST"])
def delete_question(question_id):
    cur = mysql.connection.cursor()
    cur.execute("USE quizapp")
    cur.execute(
        """SELECT * FROM Questions WHERE Question_ID=%s ORDER BY Question_ID DESC""", (question_id,))
    row = cur.fetchone()

    try:
        question = {
            "id": row["Question_ID"],
            "coursename": row["Course_Name"],
            "description": row["Question_Desc"],
            "Choice1": row["Choice1"],
            "Choice2": row["Choice2"],
            "Choice3": row["Choice3"],
            "Choice4": row["Choice4"],
            "Choice5": row["Choice5"],
            "Choice6": row["Choice6"],
            "correctAnswer": row["Correct_Answer"]
        }
    except:
        question = {}

    if question:
        cur.execute(
            """DELETE FROM Questions WHERE Question_ID = %s ;""", (question_id,))
        mysql.connection.commit()

        flash("Question has been successfully deleted.", "success")
    else:
        flash("This question does not exist.", "danger")

    return redirect(url_for("home"))


@app.route("/question/<int:question_id>")
def question(question_id):
    cur = mysql.connection.cursor()
    cur.execute("USE quizapp")
    cur.execute(
        """SELECT * FROM Questions WHERE Question_ID=%s ORDER BY Question_ID DESC""", (question_id,))
    row = cur.fetchone()

    try:
        question = {
            "id": row["Question_ID"],
            "coursename": row["Course_Name"],
            "description": row["Question_Desc"],
            "Choice1": row["Choice1"],
            "Choice2": row["Choice2"],
            "Choice3": row["Choice3"],
            "Choice4": row["Choice4"],
            "Choice5": row["Choice5"],
            "Choice6": row["Choice6"],
            "correctAnswer": row["Correct_Answer"]
        }
    except:
        question = {}
    if question:
        deleteQuestionForm = DeleteQuestionForm()

        return render_template("question.html", question=question, deleteQuestionForm=deleteQuestionForm)
    return redirect(url_for("home"))


@app.route("/quiz/<int:quiz_id>")
def quiz(quiz_id):
    cur = mysql.connection.cursor()
    cur.execute("USE quizapp")
    cur.execute(
        """SELECT * FROM QuizTable WHERE QuizID=%s ORDER BY QuizID DESC""", (quiz_id,))
    row = cur.fetchone()

    try:
        quiz = {
            "QuizID": row["QuizID"],
            "Quiz_Datetime": row["Quiz_Datetime"],
            "NumofParticipants": row["NumofParticipants"],
            "NumofQuestions": row["NumofQuestions"],
            "TotalScorePossible": row["TotalScorePossible"],
            "Duration": row["Duration"],
            "Quiz_Status": row["Quiz_Status"],
            "Quiz_Start_Time": row["Quiz_Start_Time"],
            "Quiz_End_Time": row["Quiz_End_Time"]
        }
        cur.execute("USE quizapp")
        cur.execute(
            """SELECT * FROM SelectedQuestions WHERE QuizID=%s""", (quiz_id,))

        questions_db = cur.fetchall()
        try:
            questions = []
            for row in questions_db:
                question = {
                    'id': row["Question_ID"],
                    'coursename': row["Course_Name"],
                    'description': row["Question_Desc"],
                    'Choice1': row["Choice1"],
                    'Choice2': row["Choice2"],
                    'Choice3': row["Choice3"],
                    'Choice4': row["Choice4"],
                    'Choice5': row["Choice5"],
                    'Choice6': row["Choice6"],
                    'Is_Selected': 1
                }
                questions.append(question)
        except:
            questions = {}

    except:
        quiz = {}
    if quiz:
        deleteQuizForm = DeleteQuizForm()

        return render_template("quiz.html", quiz=quiz, deleteQuizForm=deleteQuizForm, questions=questions)
    return redirect(url_for("home"))


@app.route('/api', methods=["GET"])
def API():

    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT  * FROM SelectedQuestions ORDER BY Question_Number ASC")
    data = cur.fetchall()

    result = [dict((k, value)
                   for i, (k, value) in enumerate(row.items())) for row in data]
    cur.execute(
        "SELECT  * FROM QuizTable WHERE QuizID = ( SELECT MAX(QuizID) FROM QuizTable )")
    data = cur.fetchall()
    cur.close()

    data = [dict((k, value)
                 for i, (k, value) in enumerate(row.items())) for row in data]

    return jsonify({"questions": result, "quiz": data})  # jsonify(data)


@app.route('/api/checkIP', methods=["GET"])
def checkIPAddress():

    quiz_id = request.args.get('quizId')
    ip_address = request.args.get('ipAddress')

    cur = mysql.connection.cursor()
    cur.execute("USE quizapp")
    cur.execute(
        """SELECT * FROM Results WHERE QuizID=%s AND Student_Name=%s""", (quiz_id, ip_address))
    data = cur.fetchall()
    results = []
    for row in data:
        result = {
            "QuizID": row["QuizID"],
            "IP": row["Student_Name"],
            "TotalScore": row["TotalScore"]
        }
        results.append(result)

    if results:
        data = [dict((k, value) for i, (k, value) in enumerate(row.items()))
                for row in data]
        cur.execute("USE quizapp")
        cur.execute(
            """SELECT TotalScorePossible FROM QuizTable WHERE QuizID=%s""", (quiz_id,))
        tsp_data = cur.fetchall()
        tsp = 0
        for row in tsp_data:
            tsp = row["TotalScorePossible"]
        data[0]["TotalScorePossible"] = tsp
        return jsonify({"results": data})
    else:
        return "False"


@app.route('/show-quizzes', methods=["GET"])
def show_quizzes():

    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT  * FROM QuizTable")
    data = cur.fetchall()
    result = [dict((cur.description[i][0], value)
                   for i, value in enumerate(row)) for row in data]

    cur.close()

    return jsonify({"quizzes": result})


@app.route('/userlog', methods=["GET"])
def userlog():

    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT  * FROM UserLog")
    data = cur.fetchall()
    result_log = [dict((cur.description[i][0], value)
                       for i, value in enumerate(row)) for row in data]

    cur.execute(
        "SELECT  * FROM Results")
    data = cur.fetchall()
    results = [dict((cur.description[i][0], value)
                    for i, value in enumerate(row)) for row in data]

    cur.close()

    return jsonify({"userlog": result_log,
                    "results": results})


@app.route('/quiz/show-results', methods=["GET"])
def show_results():

    return render_template("results.html")


@app.route('/api/resultpage')
def result_page():

    # Get the required data from Results table
    cur = mysql.connection.cursor()
    cur.execute("USE quizapp")
    cur.execute("SELECT * FROM Results ORDER BY QuizID DESC")
    results_from_db = cur.fetchall()

    results = []
    quiz_ids = []
    for row in results_from_db:
        result = {
            'QuizID': row["QuizID"],
            'Student_Name': row["Student_Name"],
            'StudentID': row["StudentID"],
            'NumofQuestions': row["NumofQuestions"],
            'NumofQuestionsAnswered': row["NumofQuestionsAnswered"],
            'TotalScore': row["TotalScore"]
        }
        results.append(result)
        quiz_ids.append(row["QuizID"])

    if results:

        cur.execute(
            "SELECT QuizID, TotalScorePossible FROM QuizTable WHERE QuizID IN ({})".format(
                ','.join(['%s']*len(quiz_ids))),
            quiz_ids
        )

        total_score_db = cur.fetchall()

        total_scores = []
        quiz_ids_score = []
        for row in total_score_db:
            total_score = {
                "QuizID": row["QuizID"],
                "TotalScorePossible": row["TotalScorePossible"]
            }
            total_scores.append(total_score)
            quiz_ids_score.append(row["QuizID"])

        for i in range(len(results)):
            for j in range(len(quiz_ids_score)):
                if results[i]["QuizID"] == total_scores[j]["QuizID"]:
                    results[i]["TotalPossibleScore"] = total_scores[j]["TotalScorePossible"]

    # search filter
    search = request.args.get('search')
    if search:
        search = "%" + search + "%"
        cur.execute("USE quizapp")
        cur.execute(
            """SELECT * FROM Results WHERE QuizID LIKE %s OR Student_Name LIKE %s ORDER BY QuizID DESC""", (search, search))
        results_from_db = cur.fetchall()

        results = []
        for row in results_from_db:
            result = {
                'QuizID': row["QuizID"],
                'Student_Name': row["Student_Name"],
                'StudentID': row["StudentID"],
                'NumofQuestions': row["NumofQuestions"],
                'NumofQuestionsAnswered': row["NumofQuestionsAnswered"],
                'TotalScore': row["TotalScore"]
            }
            results.append(result)
    total = len(results)

    # pagination
    start = request.args.get('start', type=int, default=-1)
    length = request.args.get('length', type=int, default=-1)
    if start != -1 and length != -1:
        results = results[start:start + length]

    # response
    return {
        'data': [result for result in results],
        'total': total,
    }


@app.route('/quiz/show-quiz-table', methods=["GET"])
def show_quiz_table():

    return render_template("quiz_table.html")


@app.route('/api/quiztablepage')
def quiz_table_page():

    # Get the required data from Results table
    cur = mysql.connection.cursor()
    cur.execute("USE quizapp")
    cur.execute("SELECT * FROM QuizTable ORDER BY QuizID DESC")
    results_from_db = cur.fetchall()

    results = []
    for row in results_from_db:
        result = {
            'QuizID': row["QuizID"],
            'Quiz_Datetime': row["Quiz_Datetime"],
            'NumofParticipants': row["NumofParticipants"],
            'NumofQuestions': row["NumofQuestions"],
            'TotalScorePossible': row["TotalScorePossible"],
            'Duration': row["Duration"],
            'Quiz_Status': row["Quiz_Status"],
            'Quiz_Start_Time': row["Quiz_Start_Time"],
            'Quiz_End_Time': row["Quiz_End_Time"]
        }
        results.append(result)

    # search filter
    search = request.args.get('search')
    if search:
        search = "%" + search + "%"
        cur.execute("USE quizapp")
        cur.execute(
            """SELECT * FROM QuizTable WHERE QuizID LIKE %s  ORDER BY QuizID DESC""", (search,))
        results_from_db = cur.fetchall()

        results = []
        for row in results_from_db:
            result = {
                'QuizID': row["QuizID"],
                'Quiz_Datetime': row["Quiz_Datetime"],
                'NumofParticipants': row["NumofParticipants"],
                'NumofQuestions': row["NumofQuestions"],
                'TotalScorePossible': row["TotalScorePossible"],
                'Duration': row["Duration"],
                'Quiz_Status': row["Quiz_Status"],
                'Quiz_Start_Time': row["Quiz_Start_Time"],
                'Quiz_End_Time': row["Quiz_End_Time"]
            }
            results.append(result)
    total = len(results)

    # pagination
    start = request.args.get('start', type=int, default=-1)
    length = request.args.get('length', type=int, default=-1)
    if start != -1 and length != -1:
        results = results[start:start + length]

    # response
    return {
        'data': [result for result in results],
        'total': total,
    }


@app.route('/quiz/show-student-answers', methods=["GET"])
def show_student_answer():

    return render_template("user_log.html")


@app.route('/api/studentanswerspage')
def student_answer_page():

    # Get the required data from Results table
    cur = mysql.connection.cursor()
    cur.execute("USE quizapp")
    cur.execute(
        "SELECT * FROM UserLog ORDER BY QuizID DESC, Course_Name DESC, Student_Name ASC, Question_Number ASC")
    results_from_db = cur.fetchall()

    results = []
    for row in results_from_db:
        result = {
            'QuizID': row["QuizID"],
            'Course_Name': row["Course_Name"],
            'Question_ID': row["Question_ID"],
            'Student_Name': row["Student_Name"],
            'StudentID': row["StudentID"],
            'Question_Number': row["Question_Number"],
            'SelectedChoice': row["SelectedChoice"],
            'Correct_Answer': row["Correct_Answer"],
            'Status': "Correct" if row["SelectedChoice"] == row["Correct_Answer"] else "Wrong"
        }
        results.append(result)

    # search filter
    search = request.args.get('search')
    if search:
        search = "%" + search + "%"
        cur.execute("USE quizapp")
        cur.execute(
            """SELECT * FROM UserLog WHERE QuizID LIKE %s OR Course_Name LIKE %s OR Student_Name LIKE %s
            ORDER BY QuizID DESC, Course_Name DESC, Student_Name ASC, 
            Question_Number ASC""", (search, search, search))
        results_from_db = cur.fetchall()

        results = []
        for row in results_from_db:
            result = {
                'QuizID': row["QuizID"],
                'Course_Name': row["Course_Name"],
                'Question_ID': row["Question_ID"],
                'Student_Name': row["Student_Name"],
                'StudentID': row["StudentID"],
                'Question_Number': row["Question_Number"],
                'SelectedChoice': row["SelectedChoice"],
                'Correct_Answer': row["Correct_Answer"],
                'Status': "Correct" if row["SelectedChoice"] == row["Correct_Answer"] else "Wrong"
            }
            results.append(result)
    total = len(results)

    # pagination
    start = request.args.get('start', type=int, default=-1)
    length = request.args.get('length', type=int, default=-1)
    if start != -1 and length != -1:
        results = results[start:start + length]

    # response
    return {
        'data': [result for result in results],
        'total': total,
    }


@app.route('/addUserLogResults', methods=["POST", "GET"])
def add_UserLog():

    # print(request.json['body']['arr'])

    # dataset = request.json['body']

    data_userlog = request.json['body']['arr']
    data_results = request.json['body']['resultArr']

    cur = mysql.connection.cursor()
    cur.execute("USE quizapp")
    cur.execute("SELECT Question_ID, Question_Score FROM SelectedQuestions")
    result_from_db = cur.fetchall()

    score_data = []
    for row in result_from_db:
        score = {
            "{}".format(row["Question_ID"]): row["Question_Score"]
        }
        score_data.append(score)

    totalScore = 0
    for i in range(len(data_userlog)):

        if data_userlog[i][6] == data_userlog[i][7]:
            totalScore += score_data[i]["{}".format(data_userlog[i][2])]

        cur.execute("USE quizapp")
        cur.execute("""INSERT INTO UserLog 
                (QuizID, Course_Name, Question_ID, Student_Name, StudentID, Question_Number, SelectedChoice, Correct_Answer) 
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (
                        data_userlog[i][0],
                        data_userlog[i][1],
                        data_userlog[i][2],
                        data_userlog[i][3],
                        data_userlog[i][4],
                        data_userlog[i][5],
                        data_userlog[i][6],
                        data_userlog[i][7]
                    ))
        mysql.connection.commit()

    cur.close()

    cur = mysql.connection.cursor()

    cur.execute("USE quizapp")
    cur.execute("""INSERT INTO Results 
            (QuizID, Student_Name, StudentID, NumofQuestions, NumofQuestionsAnswered, TotalScore) 
            VALUES(%s,%s,%s,%s,%s,%s)""",
                (
                    data_results[0],
                    data_results[1],
                    data_results[2],
                    data_results[3],
                    data_results[4],
                    totalScore
                ))
    mysql.connection.commit()

    cur.execute("USE quizapp")
    cur.execute(
        """UPDATE QuizTable SET NumofParticipants=NumofParticipants+1 WHERE QuizID=%s""", (data_results[0],))
    mysql.connection.commit()
    cur.close()

    return "Done"


@app.route('/result-table', methods=["GET"])
def resultAPI():

    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT  * FROM Results")
    data = cur.fetchall()
    result = [dict((cur.description[i][0], value)
                   for i, value in enumerate(row)) for row in data]

    cur.close()

    return jsonify({"results": result})


@app.route('/home', methods=["GET", "POST"])
def home():

    form = FilterForm(request.args, meta={"csrf": False})

    cur = mysql.connection.cursor()
    cur.execute("USE quizapp;")
    cur.execute("SELECT * FROM Questions ORDER BY Question_ID DESC;")
    questions_from_db = cur.fetchall()

    # To check if the question is included in the SelectedQuestions
    cur.execute("SELECT Question_ID FROM SelectedQuestions;")
    id_from_db = cur.fetchall()
    sel_quest_id = []
    for row in id_from_db:
        sel_quest_id.append(row["Question_ID"])

    questions = []
    for row in questions_from_db:
        question = {
            'id': row["Question_ID"],
            'coursename': row["Course_Name"],
            'description': row["Question_Desc"],
            'Choice1': row["Choice1"],
            'Choice2': row["Choice2"],
            'Choice3': row["Choice3"],
            'Choice4': row["Choice4"],
            'Choice5': row["Choice5"],
            'Choice6': row["Choice6"],
            'Is_Selected': 1 if row["Question_ID"] in sel_quest_id else 0
        }
        questions.append(question)

    course_list = [(0, "")]
    crs_list = [""]
    for index, q in enumerate(np.unique([item["coursename"] for item in questions])):
        course_list.append((index + 1, q))
        crs_list.append(q)

    form.coursename.choices = course_list
    query = """SELECT * FROM Questions"""

    if form.validate():
        if form.coursename.data:
            query += " WHERE Course_Name = '{}'".format(
                crs_list[form.coursename.data])
            if form.description.data.strip():
                query += " AND Question_Desc LIKE '%{}%'".format(
                    escape(form.description.data.strip()))
                if form.sortby.data:
                    if form.sortby.data == 1:
                        query += " ORDER BY Added_Datetime ASC"
                    if form.sortby.data == 2:
                        query += " ORDER BY Added_Datetime DESC"
        elif form.description.data.strip():
            query += " WHERE Question_Desc LIKE '%{}%'".format(
                escape(form.description.data.strip()))
            if form.sortby.data:
                if form.sortby.data == 1:
                    query += " ORDER BY Added_Datetime ASC"
                if form.sortby.data == 2:
                    query += " ORDER BY Added_Datetime DESC"
        elif form.sortby.data:
            if form.sortby.data == 1:
                query += " ORDER BY Added_Datetime ASC"
            if form.sortby.data == 2:
                query += " ORDER BY Added_Datetime DESC"
        query += " ;"
        cur.execute(query)
        questions_from_db = cur.fetchall()

        # To check if the question is included in the SelectedQuestions
        cur.execute("SELECT Question_ID FROM SelectedQuestions;")
        id_from_db = cur.fetchall()
        sel_quest_id = []
        for row in id_from_db:
            sel_quest_id.append(row["Question_ID"])
        questions = []
        for row in questions_from_db:
            question = {
                'id': row["Question_ID"],
                'coursename': row["Course_Name"],
                'description': row["Question_Desc"],
                'Choice1': row["Choice1"],
                'Choice2': row["Choice2"],
                'Choice3': row["Choice3"],
                'Choice4': row["Choice4"],
                'Choice5': row["Choice5"],
                'Choice6': row["Choice6"],
                'Is_Selected': 1 if row["Question_ID"] in sel_quest_id else 0
            }
            questions.append(question)

    else:
        cur.execute("SELECT * FROM Questions ORDER BY Question_ID DESC;")
        questions_from_db = cur.fetchall()

        # To check if the question is included in the SelectedQuestions
        cur.execute("SELECT Question_ID FROM SelectedQuestions;")
        id_from_db = cur.fetchall()
        sel_quest_id = []
        for row in id_from_db:
            sel_quest_id.append(row["Question_ID"])
        try:
            questions = []
            for row in questions_from_db:
                question = {
                    'id': row["Question_ID"],
                    'coursename': row["Course_Name"],
                    'description': row["Question_Desc"],
                    'Choice1': row["Choice1"],
                    'Choice2': row["Choice2"],
                    'Choice3': row["Choice3"],
                    'Choice4': row["Choice4"],
                    'Choice5': row["Choice5"],
                    'Choice6': row["Choice6"],
                    'Is_Selected': 1 if row["Question_ID"] in sel_quest_id else 0
                }
                questions.append(question)
        except:
            questions = []

    return render_template("home.html", questions=questions, form=form)

# to show the file contents in the static folder
# @app.route('/static/<filename>')
# def static(filename):
#    return send_from_directory("static", filename)


@app.route("/quiz/history", methods=["GET", "POST"])
def show_quiz_history():

    # get the previous quizzes
    cur = mysql.connection.cursor()
    cur.execute("USE quizapp")
    cur.execute("SELECT Course_Name FROM SelectedQuestions")
    courseName = cur.fetchone()
    try:
        courseName = courseName["Course_Name"]
    except:
        courseName = ''
    cur.execute(
        "SELECT * FROM QuizTable WHERE Quiz_Status = 'finished' ORDER BY QuizID ASC")

    prev_quizzes = cur.fetchall()

    try:
        prev_quiz = []
        for row in prev_quizzes:
            quiz = {
                'QuizID': row["QuizID"],
                'Quiz_Datetime': row["Quiz_Datetime"],
                'NumofParticipants': row["NumofParticipants"],
                'NumofQuestions': row["NumofQuestions"],
                'TotalScorePossible': row["TotalScorePossible"],
                'Duration': row["Duration"],
                'Quiz_Status': row["Quiz_Status"],
                'Quiz_Start_Time': row["Quiz_Start_Time"],
                'Quiz_End_Time': row["Quiz_End_Time"],
                'CourseName': courseName
            }
            prev_quiz.append(quiz)
    except:
        prev_quiz = []

    # get the active quizzes
    cur.execute(
        "SELECT * FROM QuizTable WHERE Quiz_Status = 'active' ORDER BY QuizID ASC")

    active_quizzes = cur.fetchall()

    try:
        act_quiz = []
        for row in active_quizzes:
            quiz = {
                'QuizID': row["QuizID"],
                'Quiz_Datetime': row["Quiz_Datetime"],
                'NumofParticipants': row["NumofParticipants"],
                'NumofQuestions': row["NumofQuestions"],
                'TotalScorePossible': row["TotalScorePossible"],
                'Duration': row["Duration"],
                'Quiz_Status': row["Quiz_Status"],
                'Quiz_Start_Time': row["Quiz_Start_Time"],
                'Quiz_End_Time': row["Quiz_End_Time"],
                'CourseName': courseName
            }
            act_quiz.append(quiz)
    except:
        act_quiz = []

    return render_template("quiz_history.html", prev_quizzes=prev_quiz, active_quizzes=act_quiz)


@app.route("/quiz/new", methods=["POST", "GET"])
def new_quiz():

    form = NewQuizForm()

    cur = mysql.connection.cursor()
    cur.execute("USE quizapp")
    cur.execute("SELECT * FROM SelectedQuestions")
    questions_from_db = cur.fetchall()

    questions = []
    for row in questions_from_db:
        question = {
            'id': row["Question_ID"],
            'coursename': row["Course_Name"],
            'description': row["Question_Desc"],
            'Choice1': row["Choice1"],
            'Choice2': row["Choice2"],
            'Choice3': row["Choice3"],
            'Choice4': row["Choice4"],
            'Choice5': row["Choice5"],
            'Choice6': row["Choice6"],
            'Is_Selected': 1
        }
        questions.append(question)

    if form.validate_on_submit() and request.method == "POST" and questions:

        question_num_array = ["{}".format(i+1) for i in range(len(questions))]
        question_num_array_dummy = [i+1 for i in range(len(questions))]

        cur = mysql.connection.cursor()
        cur.execute("USE quizapp")
        cur.execute(
            "SELECT Question_ID FROM SelectedQuestions ORDER BY Question_ID ASC")
        question_ids_db = cur.fetchall()

        question_ids = []
        for row in question_ids_db:
            question_ids.append(row["Question_ID"])

        for i in range(len(question_num_array_dummy)):
            cur.execute("""UPDATE SelectedQuestions SET Question_Number=%s WHERE Question_ID=%s""", (
                question_num_array_dummy[i],
                question_ids[i]
            ))
            mysql.connection.commit()

        values = []
        # Calculate the total possible score given the user inputs for each question
        for key in request.form:
            if key in question_num_array:
                values.append(int(request.form[key]))

        cur.execute("USE quizapp")

        now = datetime.datetime.now()
        now = now.strftime('%Y-%m-%d %H:%M:%S')

        hour_array = ['0{}'.format(i) if i < 10 else '{}'.format(i)
                      for i in range(12)]
        minutes_array = ['0{}'.format(
            i*5) if i*5 < 10 else '{}'.format(i*5) for i in range(12)]
        ampm_array = ["am", "pm"]

        if ampm_array[form.ampm.data] == "pm":
            form_hour1 = "{}".format(form.hour1.data + 12)
        else:
            form_hour1 = hour_array[form.hour1.data]
        if ampm_array[form.ampm2.data] == "pm":
            form_hour2 = "{}".format(form.hour2.data + 12)
        else:
            form_hour2 = hour_array[form.hour2.data]

        form_time1 = datetime.datetime.strptime("{} {}:{}:00".format(
            form.dt.data, form_hour1, minutes_array[form.minutes1.data]), '%Y-%m-%d %H:%M:%S')
        form_time1 = form_time1.strftime('%Y-%m-%d %H:%M:%S')
        form_time2 = datetime.datetime.strptime("{} {}:{}:00".format(
            form.dt_last.data, form_hour2, minutes_array[form.minutes2.data]), '%Y-%m-%d %H:%M:%S')
        form_time2 = form_time2.strftime('%Y-%m-%d %H:%M:%S')

        cur.execute("""INSERT INTO QuizTable
                        (Quiz_Datetime, NumofParticipants, NumofQuestions, TotalScorePossible, Duration, Quiz_Status, Quiz_Start_Time, Quiz_End_Time) 
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (
                        now,
                        0,
                        len(questions_from_db),
                        sum(values),
                        escape(form.duration.data),
                        "active",
                        form_time1,
                        form_time2
                    )
                    )
        mysql.connection.commit()

        cur.execute("USE quizapp")
        for i in range(len(values)):
            cur.execute("""UPDATE SelectedQuestions SET Question_Score=%s WHERE Question_Number=%s""", (
                values[i],
                question_num_array_dummy[i]
            ))

            mysql.connection.commit()

        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("USE quizapp")

        # get the newly generated Quiz ID
        cur.execute(
            "SELECT  * FROM QuizTable WHERE QuizID = ( SELECT MAX(QuizID) FROM QuizTable )")

        new_quiz = cur.fetchall()

        for row in new_quiz:
            quizID = row["QuizID"]

        cur.execute("""SELECT COUNT(*) FROM SelectedQuestions""")
        num_of_questions = cur.fetchone()

        question_count = num_of_questions["COUNT(*)"]
        cur.execute("USE quizapp")
        cur.executemany("""UPDATE SelectedQuestions SET QuizID=%s""", [
                        (quizID,) for i in range(question_count)])

        mysql.connection.commit()

        cur.close()

        flash("The Quiz has been successfully created!", "success")

        return redirect(url_for("home"))
    if form.errors:
        flash("{}".format(form.errors), "danger")
    return render_template("new_quiz.html", form=form, questions=questions)


@app.route("/question/new", methods=["GET", "POST"])
def new_question():

    form = NewQuestionForm()

    if form.validate_on_submit():

        now = datetime.datetime.now()
        now = now.strftime('%Y-%m-%d %H:%M:%S')

        correctAnswerChoice = ""

        if form.correctanswer.data == 0:
            correctAnswerChoice = escape(form.choice1.data)
        elif form.correctanswer.data == 1:
            correctAnswerChoice = escape(form.choice2.data)
        elif form.correctanswer.data == 2:
            correctAnswerChoice = escape(form.choice3.data)
        elif form.correctanswer.data == 3:
            correctAnswerChoice = escape(form.choice4.data)
        elif form.correctanswer.data == 4:
            correctAnswerChoice = escape(form.choice5.data)
        elif form.correctanswer.data == 5:
            correctAnswerChoice = escape(form.choice6.data)

        cur = mysql.connection.cursor()
        cur.execute("USE quizapp")
        cur.execute("""INSERT INTO Questions
                        (Course_Name, Question_Desc, Choice1, Choice2, Choice3, Choice4, Choice5, Choice6, Correct_Answer, Question_Score, Added_Datetime) 
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (
                        escape(form.coursename.data),
                        escape(form.description.data),
                        escape(form.choice1.data),
                        escape(form.choice2.data),
                        escape(form.choice3.data),
                        escape(form.choice4.data),
                        escape(form.choice5.data),
                        escape(form.choice6.data),
                        correctAnswerChoice,
                        int(0),
                        now
                    )
                    )
        mysql.connection.commit()
        cur.close()

        flash("Question has been successfully submitted!", "success")

        return redirect(url_for("home"))
    if form.errors:
        flash("{}".format(form.errors), "danger")
    return render_template("new_question.html", form=form)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
