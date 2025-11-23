import collections
from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
import math

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///car.db"
app.config['SQLALCHEMY_DATABASE_MODIFICATION'] = False
db = SQLAlchemy(app)

class most(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    qm1 = db.Column(db.String(10), nullable = False)
    qm2 = db.Column(db.String(10), nullable = False)
    qm3 = db.Column(db.String(10), nullable = False)
    qm4 = db.Column(db.String(10), nullable = False)
    qm5 = db.Column(db.String(10), nullable = False)
    def _repr_(self) -> str:
        return f"{self.sno} - {self.qm1} - {self.qm2} - {self.qm3} - {self.qm4} - {self.qm5}"
    
class least(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    ql1 = db.Column(db.String(10), nullable = False)
    ql2 = db.Column(db.String(10), nullable = False)
    ql3 = db.Column(db.String(10), nullable = False)
    ql4 = db.Column(db.String(10), nullable = False)
    ql5 = db.Column(db.String(10), nullable = False)
    def _repr_(self) -> str:
        return f"{self.sno} - {self.ql1} - {self.ql2} - {self.ql3} - {self.ql4} - {self.ql5}"
R = 0
I = 0
A = 0
S = 0
E = 0
C = 0
qma = 0
qmb= 0
qmc = 0
qmd = 0
qme = 0
qla = 0
qlb = 0
qlc = 0
qld = 0
qle = 0


@app.route('/', methods = ['GET','POST'])
def func():
    global qma,qmb,qmc,qmd,qme,qla,qlb,qlc,qld,qle
    if(request.method == 'POST'):
        qma = int(request.form['qma'])
        qla = int(request.form['qla'])
        qmb = int(request.form['qmb'])
        qlb = int(request.form['qlb'])
        qmc = int(request.form['qmc'])
        qlc = int(request.form['qlc'])
        qmd = int(request.form['qmd'])
        qld = int(request.form['qld'])
        qme = int(request.form['qme'])
        qle = int(request.form['qle'])

        career_mos = most(qm1 = qma,qm2 = qmb,qm3 = qmc,qm4 = qmd,qm5 = qme)
        career_les = least(ql1 = qla,ql2 = qlb,ql3 = qlc,ql4 = qld,ql5 = qle)
        db.session.add(career_mos)
        db.session.add(career_les)
        db.session.commit()
        return redirect('/results')
        
    return render_template("HTML_code.html")

def career():
    global qma,qmb,qmc,qmd,qme,qla,qlb,qlc,qld,qle,R,I,A,S,E,C
    func()
    qm = [qma, qmb, qmc, qmd, qme]
    ql = [qla, qlb, qlc, qld, qle]

    for choice in qm:
        if choice == 1: R += 2
        elif choice == 2: I += 2
        elif choice == 3: A += 2
        elif choice == 4: S += 2
        elif choice == 5: E += 2
        elif choice == 6: C += 2

    for choice in ql:
        if choice == 1: R -= 1
        elif choice == 2: I -= 1
        elif choice == 3: A -= 1
        elif choice == 4: S -= 1
        elif choice == 5: E -= 1
        elif choice == 6: C -= 1

    return R,I,A,S,E,C

def heighest():
      global qma,qmb,qmc,qmd,qme,qla,qlb,qlc,qld,qle,R,I,A,S,E,C
      scores = {'R': R, 'I': I, 'A': A, 'S': S, 'E': E, 'C': C}
      sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
      first = sorted_scores[0][0]
      firstscore = sorted_scores[0][1]
      second = sorted_scores[1][0]
      secondscore = sorted_scores[1][1]

      return first, second, firstscore, secondscore

HOLLAND_TYPES = {
    "R": {
        "name": "Realistic (The Doers)",
        "description": "Enjoy hands-on work with tools, machines, nature, and tangible results. "
        "They are often practical, mechanical, and athletic.",
        "careers": ["Mechanical Engineer", "Skilled Trades (Plumber, Electrician)", "Chef", 
                    "Physical Therapist", "Horticulturist", "Police Officer"],
    },
    "I": {
        "name": "Investigative (The Thinkers)",
        "description": "Enjoy working with ideas, data, and complex problems."
        " They are typically analytical, intellectual, curious, and precise.",
        "careers": ["Data Scientist", "Software Developer", "Research Analyst",
                     "Physician", "Chemist", "Economist"],
    },
    "A": {
        "name": "Artistic (The Creators)",
        "description": "Enjoy self-expression and creating new forms or designs. "
        "They are often imaginative, original, non-conforming, and emotional.",
        "careers": ["Graphic Designer", "Writer/Author", "Musician/Composer", "Architect", 
                    "Photographer", "Art Teacher"],
    },
    "S": {
        "name": "Social (The Helpers)",
        "description": "Enjoy working with people to inform, teach, heal, or serve."
        " They are typically helpful, friendly, empathetic, and responsible.",
        "careers": ["Teacher/Professor", "Counselor/Therapist", "Social Worker", "Nurse", 
                    "Human Resources Specialist", "Clergy/Minister"],
    },
    "E": {
        "name": "Enterprising (The Persuaders)",
        "description": "Enjoy leading, persuading, and managing others to achieve goals or financial gain."
        " They are often ambitious, energetic, sociable, and assertive.",
        "careers": ["Sales Manager", "Lawyer", "Marketing Executive", "Entrepreneur", "Real Estate Agent",
                     "Financial Manager"],
    },
    "C": {
        "name": "Conventional (The Organizers)",
        "description": "Enjoy working with data, rules, and established procedures."
        " They are typically orderly, careful, efficient, and good with detail.",
        "careers": ["Accountant", "Financial Analyst", "Librarian", "Bookkeeper", 
                    "Office Manager", "Auditor"],
    },
}

@app.route('/results')
def res():
    career()
    first,second,firstscore,secondscore = heighest()
    first_content = HOLLAND_TYPES.get(first, {})
    second_content = HOLLAND_TYPES.get(second, {})

    data = {
        'highest_code': first,
        'highest_score': firstscore,
        'highest_content': first_content,
        
        'second_highest_code': second,
        'second_highest_score': secondscore,
        'second_highest_content': second_content,
        
        'R': R, 'I': I, 'A': A, 'S': S, 'E': E, 'C': C
    }
    return render_template('HTML_result_code.html', data=data)

@app.route('/more')
def more():
    return render_template('HTML_recommended_code.html')
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True)
