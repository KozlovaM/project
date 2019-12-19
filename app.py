from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///opros.db'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    surname = db.Column(db.Text)
    age = db.Column(db.Integer)
    town = db.Column(db.Text)
    gender = db.Column(db.Text)


class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)


class Answers(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    q1 = db.Column(db.Integer)
    q2 = db.Column(db.Integer)
    q3 = db.Column(db.Integer)

@app.route('/questions')
def question_page():
    questions = Questions.query.all()
    return render_template(
        'questions.html',
        questions=questions
    )

@app.route('/process', methods=['get'])
def answer_process():
    if not request.args:
        return redirect(url_for('question_page'))
    name = request.args.get('name')
    surname = request.args.get('surname')
    age = request.args.get('age')
    town = request.args.get('town')
    gender = request.args.get('gender')
    user = User(
        name=name,
        surname=surname,
        age=age,
        town=town,
        gender=gender
    )
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)
    q1 = request.args.get('q1')
    q2 = request.args.get('q2')
    q3 = request.args.get('q3')
    answer = Answers(id=user.id, q1=q1, q2=q2, q3=q3)
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('stats'))


@app.route('/stats')
def stats():
    all_info = {}
    age_stats = db.session.query(
        func.avg(User.age),
        func.min(User.age),
        func.max(User.age)
    ).one()
    all_info['age_mean'] = age_stats[0]
    all_info['age_min'] = age_stats[1]
    all_info['age_max'] = age_stats[2]
    all_info['total_count'] = User.query.count()
    all_info['q2_mean'] = db.session.query(func.avg(Answers.q2)).one()[0]
    q2_answers = db.session.query(Answers.q2).all()
    return render_template('results.html', all_info=all_info)

if __name__ == '__main__':
    app.run(debug=True)