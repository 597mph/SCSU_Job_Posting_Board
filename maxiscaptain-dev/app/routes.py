from flask_mail import Mail, Message
from app import USERNAME, app
from time import gmtime, strftime
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import *
from app.models import *
from app import db
import sys

mail = Mail(app)

def if_admin():
    if current_user.role == "Admin":
        return True
    return False

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/test')
def test():
    return render_template('test.html')

#create search function
@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():

        #get data from submmited form
        search = form.searched.data

        profile = User.query.filter(User.username.like('%' +  search + '%'))
        profile = profile.order_by(User.username).all()



        #Query the database
        return render_template("search.html", form=form, searched = search, user = profile, )
    return render_template("search.html", form=form)

#pass searched items to navbar
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

#when user clicks on the searched profile
@app.route('/search/<username>')
@login_required
def clickedSearched(username):
    user = User.query.filter_by(username=username).first_or_404()
    #if current user is faculty
    if current_user.role == "Faculty":
        return render_template('fac_search.html', user=user)

    #if current user is student
    if current_user.role == "Student":
        return render_template('stu_search.html', user=user)

    #if current user is faculty
    if current_user.role == "Employer":
        return render_template('emp_search.html', user=user)
    

@app.route('/signup', methods=['GET', 'POST'])
def signUp():
    form = CreateAccountForm()
    if form.validate_on_submit():
        username = form.username.data
        useremail = form.email.data
        first = form.first.data
        last = form.last.data
        password = form.password.data
        passwordRetype = form.passwordRetype.data
        accountType = form.accountType.data
        

        user = db.session.query(User).filter_by(username=username).first()
        email = db.session.query(User).filter_by(email = useremail).first()
        
        if user or email or (password != passwordRetype):
            print('Creation Failed.', file=sys.stdout)
            return render_template("signup.html", form=form)
            
        else:
            u = User(username=username, email = useremail, role=accountType)
            u.set_password(password)
            db.session.add(u)
            db.session.commit()

            if u.role == "Student":
                p = StudentProfile(user_id = u.id, email=u.email, username = u.username, first = first, last = last)
            if u.role == "Faculty":
                p = FacultyProfile(user_id = u.id, email=u.email, username = u.username, first = first, last = last)
            if u.role == "Employer":
                p = EmployerProfile(user_id = u.id, email=u.email, username = u.username, first = first, last = last)
       
            db.session.add(p)
            db.session.commit()
            print("Creation successful.", file=sys.stdout)
            return redirect(url_for("login"))
    return render_template('signup.html', form=form)
 
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            print('Login Failed', file=sys.stderr)
            flash('Login Unsuccessful!')
            return redirect(url_for('login'))
        
        login_user(user)
        print('Login Successful', file=sys.stderr) 
        flash('Welcome Back!') 
        if current_user.role == "Student":
            return redirect(url_for("stu_profile", username=current_user.username))
        if current_user.role == "Faculty":
            return redirect(url_for("fac_profile", username=current_user.username))
        if current_user.role == "Employer":
            return redirect(url_for("emp_profile", username=current_user.username))
        if current_user.role == "Admin":
            return render_template("admin.html")    
    return render_template('login.html', form=form)
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/stu_change', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(id=current_user.id).first()
        flash('Password Changed Successfully')

        if user.check_password(form.old_pass.data) and form.new_pass.data == form.new_pass_retype.data:
            user.set_password(form.new_pass.data)
            db.session.commit()
            print('Password Changed!', file=sys.stdout)
        else:
            print('Password Change Failed!', file=sys.stdout)
        return render_template('stu_change.html', form=form)
    return render_template('stu_change.html', form=form)
    
@app.route('/stu_delete', methods=['GET', 'POST'])
def delete_record():
    form = DeleteForm()
    if form.validate_on_submit():
        to_delete = db.session.query(User).filter_by(username=form.username.data).first()
        flash('User Deleted!')

        if to_delete is not None:
            db.session.delete(to_delete)
            db.session.commit()

        form.username.data= ''
        return redirect(url_for('login'))
    return render_template('stu_delete.html', form=form)

@app.route('/fac_update', methods=['GET', 'POST'])
def update_faculty():
    form = FacultyProfileForm()
    if form.validate_on_submit():
        profile = db.session.query(FacultyProfile).filter_by(user_id=current_user.id).first() 
        profile.first = form.first.data 
        profile.last = form.last.data 
        profile.address = form.address.data
        profile.phone = form.phone.data 
        profile.email = form.email.data
        profile.school = form.school.data
        profile.department = form.department.data
        profile.office = form.office.data
        flash('Profile Updated Successfully!')
        db.session.commit()
        return redirect(url_for('fac_profile', username = current_user.username))
    return render_template('fac_update.html', form=form) 

@app.route('/emp_update', methods=['GET', 'POST'])
def update_employer():
    form = EmployerProfileForm()
    if form.validate_on_submit():
        profile = db.session.query(EmployerProfile).filter_by(user_id=current_user.id).first()
        profile.first = form.first.data 
        profile.last = form.last.data 
        profile.organization = form.business_name.data
        profile.title = form.title.data
        profile.email = form.email.data 
        profile.phone = form.phone.data
        profile.address = form.address.data
        profile.expertise = form.expertise.data
        flash('Profile Updated Successfully!')
        db.session.commit()
        return redirect(url_for('emp_profile', username = current_user.username))
    return render_template('emp_update.html', form=form)

@app.route('/fac_delete', methods=['GET', 'POST'])
def delete_faculty():
    form = DeleteForm()
    if form.validate_on_submit():
        to_delete = db.session.query(User).filter_by(username=form.username.data).first()
        flash('User Deleted!')

        if to_delete is not None:
            db.session.delete(to_delete)
            db.session.commit()

        form.username.data = ''
        return redirect(url_for('login'))
    return render_template('fac_delete.html', form=form)

@app.route('/fac_change', methods=['GET', 'POST'])
def change_faculty():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(id=current_user.id).first()
        flash('Password Changed Successfully')

        if user.check_password(form.old_pass.data) and form.new_pass.data == form.new_pass_retype.data:
            user.set_password(form.new_pass.data)
            db.session.commit()
            print('Password Changed!', file=sys.stdout)
        else:
            print('Password Change Failed!', file=sys.stdout)
        return render_template('fac_change.html', form=form)
    return render_template('fac_change.html', form=form)

@app.route('/fac_manage_apps', methods=['GET', 'POST'])
@login_required
def fac_manage_apps():
    applications = db.session.query(Applicant).order_by(Applicant.id.desc()).all()
    if request.method == 'POST':
        if request.form.get('accept'):
            buttonID = request.form.get("accept").strip('Accept ')
            app = db.session.query(Applicant).filter_by(id=buttonID).first()
            accept = ApplicationAccept(
                        id = app.id,
                        user_id = app.user_id,
                        username = app.username,
                        entry_id = app.entry_id,
                        entry_text = app.entry_text,
                        employer_id = app.employer_id,
                        first = app.first,
                        last = app.last       
            )
            db.session.add(accept)
            db.session.delete(app)
            db.session.commit()
            return render_template('fac_manage_apps.html', applications=applications)
        if request.form.get('decline'):
            buttonID = request.form.get("decline").strip('Decline ')
            app = db.session.query(Applicant).filter_by(id=buttonID).first()
            db.session.delete(app)
            db.session.commit()
            return render_template('fac_manage_apps.html', applications=applications)
    return render_template('fac_manage_apps.html', applications=applications)

@app.route('/stu_display_listings', methods=['GET', 'POST'])
@login_required
def stu_display_listings():
    cur = db.session.query(Entry).order_by(Entry.id.desc()).all()
    if request.method == 'POST':
        if request.form.get('apply'):
            buttonID = request.form.get("apply").strip('Apply to Listing ')
            student = db.session.query(StudentProfile).filter_by(user_id = current_user.id).first()
            entry = db.session.query(Entry).filter_by(id = buttonID).first()
            entry.applicant += ', ' + str(current_user.id)
            applicant = Applicant(user_id = current_user.id, username = current_user.username, entry_id = buttonID, employer_id = entry.user_id,
                                  first = student.first, last = student.last, entry_text=entry.text)
            db.session.add(applicant)
            db.session.commit()
            return render_template('stu_display_listings.html', cur=cur)
    return render_template('stu_display_listings.html', cur=cur)

@app.route('/emp_change', methods=['GET', 'POST'])
def change_employer():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(id=current_user.id).first()
        flash('Password Changed Successfully')

        if user.check_password(form.old_pass.data) and form.new_pass.data == form.new_pass_retype.data:
            user.set_password(form.new_pass.data)
            db.session.commit()
            print('Password Changed!', file=sys.stdout)
        else:
            print('Password Change Failed!', file=sys.stdout)
        return render_template('emp_change.html', form=form)
    return render_template('emp_change.html', form=form)

@app.route('/emp_delete', methods=['GET', 'POST'])
def delete_employer():
    form = DeleteForm()
    if form.validate_on_submit():
        to_delete = db.session.query(User).filter_by(username=form.username.data).first()
        flash('User Deleted!')

        if to_delete is not None:
            db.session.delete(to_delete)
            db.session.commit()

        form.username.data = ''
        return redirect(url_for('login'))
    return render_template('emp_delete.html', form=form)

@app.route('/emp_display_listings', methods=['GET', 'POST'])
@login_required
def emp_display_listings():
    cur = db.session.query(Entry).order_by(Entry.id.desc()).all()
    return render_template('emp_display_listings.html', cur=cur)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_entry():
    form = EntryForm()
    if form.validate_on_submit():
        title = form.title.data
        email = form.email.data
        phone = form.phone.data
        text = form.text.data
        date_time = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

        e = Entry(title=title, email=email, phone=phone, text=text, 
                  datetime=date_time, user_id = current_user.id, username = current_user.username, applicant = '0')
        db.session.add(e)
        db.session.commit()
        print("Post created.", file=sys.stdout)
        
        form.title.data = ''
        form.email.data = ''
        form.phone.data = ''
        form.text.data = ''
        return render_template('create_entry.html', form=form)
    return render_template('create_entry.html', form=form)

@app.route('/faculty/<username>')
@login_required
def fac_profile(username):
    user = db.session.query(User).filter_by(username=username).first()
    profile = db.session.query(FacultyProfile).filter_by(user_id=user.id).first()
  
    posts = [{'author': user, 'body': 'Test Post #1'},
             {'author': user, 'body': 'Test Post #2'}]
    return render_template('fac_profile.html', user=user, posts=posts, profile=profile)

@app.route('/employer/<username>')
@login_required
def emp_profile(username):
    user = db.session.query(User).filter_by(username=username).first()
    profile = db.session.query(EmployerProfile).filter_by(user_id=user.id).first()
  
    posts = [{'author': user, 'body': 'Test Post #1'},
             {'author': user, 'body': 'Test Post #2'}]
    return render_template('emp_profile.html', user=user, posts=posts, profile=profile)

@app.route('/api/data_fac')
def access_api_fac():
    query = FacultyProfile.query

    #search
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            FacultyProfile.first.like(f'%{search}%'),
            FacultyProfile.last.like(f'%{search}%'),
            FacultyProfile.address.like(f'%{search}%'),
            FacultyProfile.phone.like(f'%{search}%'),
            FacultyProfile.email.like(f'%{search}%'),
            FacultyProfile.school.like(f'%{search}%'),
            FacultyProfile.department.like(f'%{search}%'),
            FacultyProfile.office.like(f'%{search}%')))

    total_filtered = query.count()

    #sort
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_first = request.args.get(f'columns[{col_index}][data]')
        if col_first not in ['first', 'last', 'address', 'phone', 'email', 'school', 'department', 'office']:
            col_first = 'first'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(FacultyProfile, col_first)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1

    if order:
        query = query.order_by(*order)

    #pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    #response
    return {
        'data': [user.to_dict() for user in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': FacultyProfile.query.count(),
        'draw': request.args.get('draw', type=int)}

@app.route('/api/data_emp')   
def access_api_emp():
    query = EmployerProfile.query

    #search
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            EmployerProfile.first.like(f'%{search}%'),
            EmployerProfile.last.like(f'%{search}%'),
            EmployerProfile.title.like(f'%{search}%'),
            EmployerProfile.organization.like(f'%{search}%'),
            EmployerProfile.address.like(f'%{search}%'),
            EmployerProfile.phone.like(f'%{search}%'),
            EmployerProfile.email.like(f'%{search}%'),
            EmployerProfile.expertise.like(f'%{search}%')))

    total_filtered = query.count()

    #sort
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_first = request.args.get(f'columns[{col_index}][data]')
        if col_first not in ['first', 'last', 'title', 'organization', 'address', 'phone', 'email', 'expertise']:
            col_first = 'first'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(EmployerProfile, col_first)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1

    if order:
        query = query.order_by(*order)

    #pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    #response
    return {
        'data': [user.to_dict() for user in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': EmployerProfile.query.count(),
        'draw': request.args.get('draw', type=int)}

@app.route('/emp_my_listings', methods=['GET', 'POST'])
@login_required
def emp_my_listings():
    listings = db.session.query(Entry).filter_by(user_id = current_user.id).all()
    applicants = db.session.query(ApplicationAccept).filter_by(employer_id = current_user.id).all()
    if request.method == 'POST':
        if request.form.get('delete'):
            buttonID = request.form.get("delete").strip('Delete Application ID: ')
            print('test ' + buttonID, file=sys.stdout)
            to_delete=db.session.query(ApplicationAccept).filter_by(id=buttonID).first()
            if to_delete is not None:
                db.session.delete(to_delete)
                db.session.commit()
                return render_template('emp_my_listings.html', cur = listings, applicants = applicants)
            return render_template('emp_my_listings.html', cur = listings, applicants = applicants)
        if request.form.get("mail"):
            return redirect(url_for('emp_mail'))
        if request.form.get("profile"):
            buttonID = request.form.get("profile")
            print(buttonID, file=sys.stdout)
            return redirect(url_for('emp_search', username = buttonID))
    return render_template('emp_my_listings.html', cur = listings, applicants = applicants)
    
@app.route("/emp_search/<username>", methods=["GET", "POST"])
@login_required
def emp_search(username):
    user = db.session.query(StudentProfile).filter_by(username = username).first()
    return render_template('emp_search.html', profile = user)

@app.route('/stu_mail', methods=['GET', 'POST'])
@login_required
def stu_mail():
    form = MailForm()
    if form.validate_on_submit():
        recipient = form.email.data
        message = form.message.data
        subject = 'Test Flask email'
        msg = Message(subject, recipients=[recipient], body = message)
        mail.send(msg)
        form.email.data = ''
        form.message.data = ''
    return render_template('stu_mail.html', form=form)

@app.route('/fac_mail', methods=['GET', 'POST'])
@login_required
def fac_mail():
    form = MailForm()
    if form.validate_on_submit():
        recipient = form.email.data
        message = form.message.data
        subject = 'Test Flask email'
        msg = Message(subject, recipients=[recipient], body = message)
        mail.send(msg)
        form.email.data = ''
        form.message.data = ''
    return render_template('fac_mail.html', form=form)

@app.route('/emp_mail', methods=['GET', 'POST'])
@login_required
def emp_mail():
    form = MailForm()
    if form.validate_on_submit():
        recipient = form.email.data
        message = form.message.data
        subject = 'Test Flask email'
        msg = Message(subject, recipients=[recipient], body = message)
        mail.send(msg)
        form.email.data = ''
        form.message.data = ''
    return render_template('emp_mail.html', form=form)


@app.route('/stu_my_listings', methods=['GET', 'POST'])
@login_required
def stu_my_listings():
    preapproved = db.session.query(Applicant).filter_by(user_id = current_user.id).all()
    approved = db.session.query(ApplicationAccept).filter_by(user_id =current_user.id).all()
    return render_template('stu_my_listings.html', preapproved = preapproved, approved = approved)

@app.route('/student/<username>')
@login_required
def stu_profile(username):
    user = db.session.query(User).filter_by(username=username).first()
    profile = db.session.query(StudentProfile).filter_by(user_id=user.id).first()

    posts = [{'author': user, 'body': 'Test Post #1'},
             {'author': user, 'body': 'Test Post #2'}]
    return render_template('stu_profile.html', user=user, posts=posts, profile=profile)

@app.route('/stu_update', methods=['GET', 'POST'])
def update_student():
    form = StudentProfileForm()
    if form.validate_on_submit():
        profile = db.session.query(StudentProfile).filter_by(user_id=current_user.id).first() 
        profile.first = form.first.data 
        profile.last = form.last.data 
        profile.address = form.address.data 
        profile.email = form.email.data 
        profile.major = form.major.data 
        profile.grade = form.grade.data 
        profile.phone = form.phone.data
        profile.school = form.school.data
        flash('Profile Updated Successfully!')
        db.session.commit()
        return redirect(url_for('stu_profile', username = current_user.username))
    return render_template('stu_update.html', form=form)

@app.route('/stu_direct')
@login_required
def stu_direct():
    return render_template('stu_direct.html')
     
@app.route('/stu_direct_table_stu')
@login_required
def stu_direct_table_stu():
    return render_template('stu_direct_table_stu.html', title='Student Information')

@app.route('/stu_direct_table_fac')
@login_required
def stu_direct_table_fac():
    return render_template('stu_direct_table_fac.html', title='Faculty Information')

@app.route('/stu_direct_table_emp')
@login_required
def stu_direct_table_emp():
    return render_template('stu_direct_table_emp.html', title='Employer Information')

@app.route('/fac_direct')
@login_required
def fac_direct():
    return render_template('fac_direct.html')
    
@app.route('/fac_direct_table_stu')
@login_required
def fac_direct_table_stu():
    return render_template('fac_direct_table_stu.html', title="Student Information")
     
@app.route('/fac_direct_table_fac')
@login_required
def fac_direct_table_fac():
    return render_template('fac_direct_table_fac.html', title="Faculty Information")
     
@app.route('/fac_direct_table_emp')
@login_required
def fac_direct_table_emp():
    return render_template('fac_direct_table_emp.html', title="Employer Information")
     
@app.route('/emp_direct')
@login_required
def emp_direct():
    return render_template('emp_direct.html')
    
@app.route('/emp_direct_table_stu')
@login_required
def emp_direct_table_stu():
    return render_template('emp_direct_table_stu.html', title="Student Information")
     
@app.route('/emp_direct_table_fac')
@login_required
def emp_direct_table_fac():
    return render_template('emp_direct_table_fac.html', title="Faculty Information")
  
@app.route('/emp_direct_table_emp')
@login_required
def emp_direct_table_emp():
    return render_template('emp_direct_table_emp.html', title="Employer Information")
     
@app.route('/api/data_stu')   
def access_api_stu():
    query = StudentProfile.query

    #search
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            StudentProfile.first.like(f'%{search}%'),
            StudentProfile.last.like(f'%{search}%'),
            StudentProfile.address.like(f'%{search}%'),
            StudentProfile.phone.like(f'%{search}%'),
            StudentProfile.email.like(f'%{search}%'),
            StudentProfile.major.like(f'%{search}%'),
            StudentProfile.grade.like(f'%{search}%'),
            StudentProfile.school.like(f'%{search}%')))

    total_filtered = query.count()

    #sort
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_first = request.args.get(f'columns[{col_index}][data]')
        if col_first not in ['first', 'last', 'address', 'phone', 'email', 'major', 'grade', 'school']:
            col_first = 'first'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(StudentProfile, col_first)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1

    if order:
        query = query.order_by(*order)

    #pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    #response
    return {
        'data': [user.to_dict() for user in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': StudentProfile.query.count(),
        'draw': request.args.get('draw', type=int)}