from flask import Flask,render_template,redirect,request,url_for,session
from models import db,User,Subject,Chapter,Quiz,Question,Score 
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime 


app=Flask(__name__)

app.config['SECRET_KEY']='devml08'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///quiz_master.db'  #URI for Flask Sqlalchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db.init_app(app)


# ====HomePage====
@app.route('/')
def home():
    return render_template('home.html')


#=====Register=====
@app.route('/register',methods=["POST","GET"])
def register():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        full_name=request.form['full_name']
        role='user'  #admins cannot register,only login.

        #cheching if user already exists
        existing_user=User.query.filter_by(email=email).first()
        if existing_user:
            return "User already exists!",400

        new_user=User(email=email,password=password,full_name=full_name,role=role)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login')) #redirect to login after successful registration
    return render_template('register.html')

#======Login=======
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')

        user=User.query.filter_by(email=email).first()

        if user and user.password==password:
            session['user_id']=user.id   #store user id in session
            session['role']=user.role
            if user.role=='admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('dashboard'))
        else:
            return "Invalid Login Credentials.Try Again.", 401
    return render_template('login.html')


#======Logout======
@app.route('/logout')
def logout():
    session.pop('user_id',None)
    session.pop('role',None)

    return redirect(url_for('login'))

#======for user dashboard============
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user=User.query.get(session['user_id'])
    quizzes=Quiz.query.all()  #get all the quizzes
    scores=Score.query.filter_by(user_id=user.id).all() #fetch all user scores
    chapters=Chapter.query.all()

    return render_template('user_dashboard.html',user=user,quizzes=quizzes,scores=scores,chapters=chapters)

@app.route('/user_search',methods=['GET'])  #search functionality for the user
def user_search():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    query=request.args.get('query','').strip()
    filter_by=request.args.get('filter')

    results=[]
    if filter_by=="subjects":
        results=Subject.query.filter(Subject.name.ilike(f"%{query}%")).all()
    elif filter_by=="quizzes":
        results=Quiz.query.filter(Quiz.title.ilike(f"%{query}%")).all()
    return render_template('user_search_results.html',results=results,filter_by=filter_by,query=query)


#==============Admin Dashboard=============
@app.route('/admin_dashboard',methods=['GET','POST'])
def admin_dashboard():
    if 'user_id' not in session or session.get('role') != 'admin':
        return "Access Denied. Admins only.", 403 
     

    users=User.query.filter(User.role!='admin').all()  #get all users except the admin
    subjects=Subject.query.all() #get all subjects 
    chapters=Chapter.query.all() #get all the chapters
    quizzes= Quiz.query.all()  #get all quizzes
    scores= Score.query.all() #get all the scores
    questions=Question.query.all()

    return render_template('admin_dashboard.html',
                            users=users,
                            subjects=subjects,
                            chapters=chapters,quizzes=quizzes,scores=scores,
                            questions=questions)

@app.route('/admin_search',methods=['GET'])  #search functionality for the admin
def admin_search():
    if 'user_id' not in session or session.get('role') !='admin':
        return "Access Denied.Admins Only!",403
    
    query=request.args.get('query','').strip()
    filter_by=request.args.get('filter')

    results=[]
    if filter_by=="users":
        results=User.query.filter(User.full_name.ilike(f"%{query}%")).all()
    elif filter_by=="subjects":
        results=Subject.query.filter(Subject.name.ilike(f"%{query}%")).all()
    elif filter_by=="quizzes":
        results=Quiz.query.filter(Quiz.title.ilike(f"%{query}%")).all()
    elif filter_by=="questions":
        results=Question.query.filter(Question.text.ilike(f"%{query}%")).all()
    return render_template('admin_search_results.html',results=results,filter_by=filter_by,query=query)    

        


#==========Delete User====================
@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return "Access Denied. Admins only.", 403
    user=User.query.get(user_id)
    if user:
        Score.query.filter_by(user_id=user.id).delete()
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('admin_dashboard'))  


#=========Subject Routes=====================
@app.route('/manage_subjects', methods=['GET', 'POST'])    #manage subjects
def manage_subjects():
    if 'user_id' not in session or session.get('role') != 'admin':
        return "Access Denied. Admins only.", 403  # Forbidden

    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            subject = Subject(name=name)
            db.session.add(subject)
            db.session.commit()
            return redirect(url_for('manage_subjects'))
    
    subjects = Subject.query.all()
    return render_template('manage_subjects.html', subjects=subjects) 


@app.route('/edit_subject/<int:subject_id>',methods=['GET','POST'])  #edit subjects
def edit_subject(subject_id):
    if 'user_id' not in session or session.get('role') !='admin':
        return "Access Denied.Admins only!",403
    
    subject=Subject.query.get_or_404(subject_id)
    if request.method=="POST":
        new_name=request.form.get('name')
        if new_name:
            subject.name=new_name 
            db.session.commit()
            return redirect(url_for('manage_subjects'))
    return render_template('edit_subject.html',subject=subject)



@app.route('/delete_subject/<int:subject_id>',methods=['POST'])  #Delete Subjects
def delete_subject(subject_id):
    if 'user_id' not in session or session.get('role')!='admin':
        return "Access denied.Admins only!",403
    
    subject=Subject.query.get(subject_id)
    if subject:
        db.session.delete(subject)
        db.session.commit()
    return redirect(url_for('admin_dashboard')) 


#=============Chapter Routes================   

@app.route('/manage_chapters', methods=['GET', 'POST'])  #Manage Subjects
def manage_chapters():
    if 'user_id' not in session or session.get('role') != 'admin':
        return "Access Denied. Admins only.", 403

    if request.method == 'POST':
        name = request.form.get('name')
        subject_id = request.form.get('subject_id')
        if name and subject_id:
            chapter = Chapter(name=name, subject_id=subject_id)
            db.session.add(chapter)
            db.session.commit()
    subjects= Subject.query.all()  
    subject_id=request.args.get('subject_id')
    subject=None
    chapters = []

    if subject_id:
        subject=Subject.query.get(subject_id)
        chapters=Chapter.query.filter_by(subject_id=subject_id).all()
    else:
        subject=None 
        chapters=Chapter.query.all()

    return render_template('manage_chapters.html', chapters=chapters,subjects=subjects,subject=subject,subject_id=subject.id if subject else None)


@app.route('/edit_chapter/<int:chapter_id>',methods=['GET','POST']) #Edit Chapters 
def edit_chapter(chapter_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return "Access Denied. Admins only.", 403 
    
    chapter=Chapter.query.get_or_404(chapter_id)
    subjects=Subject.query.all()

    if request.method=='POST':
        new_name=request.form.get('name')
        new_subject_id=request.form.get('subject_id')

        if new_name and new_subject_id:
            chapter.name=new_name
            chapter.subject_id=int(new_subject_id)
            db.session.commit()

            return redirect(url_for('manage_chapters'))
    return render_template('edit_chapter.html',chapter=chapter,subjects=subjects)
     


@app.route('/delete_chapter/<int:chapter_id>',methods=['POST']) #Delete chapters
def delete_chapter(chapter_id):
    if 'user_id' not in session or session.get('role')!='admin':
        return "Access Denied.Only Admins!",403
    
    chapter=Chapter.query.get_or_404(chapter_id)
    if chapter:
        db.session.delete(chapter)
        db.session.commit()
    return redirect(url_for('admin_dashboard')) 



#===============Quiz Routes================

@app.route('/manage_quizzes/',defaults={'chapter_id':None},methods=['GET','POST'])
@app.route('/manage_quizzes/<int:chapter_id>', methods=['GET', 'POST'])    #Manage Quizzes
def manage_quizzes(chapter_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return "Access Denied. Admins only.", 403
    
    if chapter_id is None:
        return "NO chapter selected.Please choose a chapter.",400
    chapter=Chapter.query.get_or_404(chapter_id)

    if request.method == 'POST':
        title = request.form.get('title')
        date_str=request.form.get('date')
        duration_str=request.form.get('duration')
        if title and date_str and duration_str:
            try:
                #convert date string to a date object
                quiz_date=datetime.strptime(date_str,"%Y-%m-%d").date()
                #converting the duration string to a time object
                quiz_duration=datetime.strptime(duration_str,"%H:%M").time()

                subject_id=chapter.subject_id
                if not subject_id:
                    return "Error:Chapter is not linked to any subject.",400

                quiz = Quiz(title=title, chapter_id=chapter_id,subject_id=subject_id,date=quiz_date,duration=quiz_duration)
                db.session.add(quiz)
                db.session.commit()

                return redirect(url_for('manage_quizzes',chapter_id=chapter_id))
            except ValueError:
                return "Invalid date or time format.Please enter a valid date (YYYY-MM-DD) and duration(HH:MM).",404
    
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    return render_template('manage_quizzes.html', quizzes=quizzes,chapter=chapter)



@app.route('/edit_quiz/<int:quiz_id>',methods=['GET','POST']) #Edit Quizzes
def edit_quiz(quiz_id):
    if 'user_id' not in session or session.get('role') !='admin':
        return "Access Denied.Admins only",403
    
    quiz=Quiz.query.get_or_404(quiz_id)
    chapters=Chapter.query.all()
    if not quiz:
        return "Quiz not found.",404
    if request.method=='POST':
        new_title=request.form.get('title')
        new_chapter_id=request.form.get('chapter_id')

        if new_title:
            quiz.title=new_title 
        if new_chapter_id:
            try:
                quiz.chapter_id=int(new_chapter_id)
            except ValueError:
                return "Invalid chapter ID",400 
        db.session.commit()

        if quiz.chapter_id is None:
            return "Error: This quiz is not linked to any chapter.", 400

        return redirect(url_for('manage_quizzes',chapter_id=quiz.chapter_id))

    return render_template('edit_quiz.html',quiz=quiz,chapters=chapters)        

@app.route('/delete_quiz/<int:quiz_id>',methods=['POST'])   # Delete Quizzes
def delete_quiz(quiz_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return "Access Denied. Admins only.", 403
       
    quiz=Quiz.query.get(quiz_id)
    if not quiz:
        return "Quiz not found.",404
    chapter_id=quiz.chapter_id
    db.session.delete(quiz)
    db.session.commit()
    return redirect(url_for('manage_quizzes',chapter_id=chapter_id))




#===========Question Routes===========

@app.route('/manage_questions',methods=['GET','POST'])
@app.route('/manage_questions/<int:quiz_id>',methods=['GET','POST'])  #Manage Questions
def manage_questions(quiz_id=None):
    if not session.get('user_id') or session.get('role') != 'admin':
        return "Access Denied. Admins only.", 403 
    if quiz_id is None:
        quiz_id=request.args.get('quiz_id',type=int)
    quiz=Quiz.query.get_or_404(quiz_id)
   

    if request.method=='POST':
        text= request.form.get('text')
        option_a=request.form.get('option_a')
        option_b=request.form.get('option_b')
        option_c=request.form.get('option_c')
        option_d=request.form.get('option_d')
        correct_option=request.form.get('correct_option')

        if text and option_a and option_b and option_c and option_d and correct_option:
            question=Question(text=text,option_a=option_a,option_b=option_b,option_c=option_c,option_d=option_d,correct_option=correct_option,quiz_id=quiz_id)

            db.session.add(question)
            db.session.commit()
    questions= Question.query.filter_by(quiz_id=quiz_id).all()
    return render_template('manage_questions.html',quiz=quiz,questions=questions)


@app.route('/edit_question/<int:question_id>',methods=['GET','POST'])  #Edit Questions
def edit_question(question_id):
    if not session.get('user_id') or session.get('role') != 'admin':
        return "Access Denied. Users only.", 403 
    
    question=Question.query.get_or_404(question_id)
    quizzes=Quiz.query.all()

    if request.method=='POST':
        text=request.form.get('text')
        option_a=request.form.get('option_a')
        option_b=request.form.get('option_b')
        option_c=request.form.get('option_c')
        option_d=request.form.get('option_d')
        correct_option=request.form.get('correct_option')
        quiz_id=request.form.get('quiz_id')

        if quiz_id is None or quiz_id.strip()=="":
            return "Quiz ID is required.",400
        
        try:
            quiz_id=int(quiz_id)
        except ValueError:
            return "Invalid Quiz ID.",400

        question.text=text 
        question.option_a=option_a 
        question.option_b=option_b
        question.option_c=option_c
        question.option_d=option_d
        question.correct_option=correct_option
        question.quiz_id=quiz_id     
        db.session.commit()
        return redirect(url_for('manage_questions',quiz_id=question.quiz_id))
    return render_template('edit_question.html',question=question,quizzes=quizzes)


@app.route('/delete_question/<int:question_id>',methods=['POST'])   #Delete Quizzes
def delete_question(question_id):
    if not session.get('user_id') or session.get('role') != 'admin':
        return "Access Denied. Admins only.", 403

    question=Question.query.get_or_404(question_id)
    quiz_id=question.quiz_id
    db.session.delete(question)
    db.session.commit() 

    return redirect(url_for('manage_questions',quiz_id=quiz_id))



#===============View Routes=============
@app.route('/view_subjects') #view all subjects
def view_subjects():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    subjects=Subject.query.all()
    return render_template('view_subjects.html',subjects=subjects)

@app.route('/subject/<int:subject_id>')  #view all chapters
def view_chapters(subject_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    subject=Subject.query.get_or_404(subject_id)
    chapters=Chapter.query.filter_by(subject_id=subject_id).all()
    return render_template('view_chapters.html',subject=subject,chapters=chapters)


@app.route('/chapter/<int:chapter_id>')  #view all quizzes
def view_quizzes(chapter_id):
    chapter=Chapter.query.get_or_404(chapter_id)
    quizzes=Quiz.query.filter_by(chapter_id=chapter.id).all()
    subject=Subject.query.get(chapter.subject_id) if chapter.subject_id else None

    return render_template('view_quizzes.html',chapter=chapter,quizzes=quizzes,subject=subject)


@app.route('/view_scores')    #view the scores
def view_scores():
    if not session.get('user_id') or session.get('role') != 'user':
        return "Access Denied. Users only.", 403

    scores = Score.query.filter_by(user_id=session['user_id']).all()
    return render_template('view_scores.html', scores=scores) 

 

@app.route('/take_quiz/<int:quiz_id>', methods=['GET', 'POST'])
def take_quiz(quiz_id):
    if not session.get('user_id') or session.get('role') != 'user':
        return "Access Denied. Users only.", 403

    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()

    if request.method == 'POST':
        score = 0
        for question in questions:
            selected_option = request.form.get(str(question.id))
            if selected_option and selected_option.upper()== question.correct_option.upper():
                score += 1
        #saving the scores 
        user_score = Score(user_id=session['user_id'], quiz_id=quiz_id, score=score)
        db.session.add(user_score)
        db.session.commit()

        return f""" 
        <h2>Quiz Completed!</h2>
        Quiz completed! Your score: {score}/{len(questions)} <br><br><br>
        <a href="{url_for('dashboard')}">Back to Dashboard</a>
        """

    return render_template('take_quiz.html', quiz=quiz, questions=questions)




def create_database():

        # check if an admin exists, if not we create one
        admin_email="admin123@gmail.com"
        existing_admin=User.query.filter_by(email=admin_email).first()

        if not existing_admin:
            admin=User(email=admin_email,password="admin123",full_name="Admin",role="admin")

            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")  





if __name__=="__main__":
    with app.app_context():
        db.create_all()
        create_database()
    app.run(debug=True)

