from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'ibrahimwatts'  # Add a secret key for flash messages

# Placeholder for user data
users = []

# Placeholder for course and unit data
courses = ['Math', 'English', 'Science']
units = ['SIT11', 'SIT112', 'SIT115', 'SIT367', 'SIT233']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Check if the user already exists
        existing_user = next((u for u in users if u['email'] == email), None)

        if existing_user:
            flash('User already exists. Please log in.')
            return redirect(url_for('index'))

        # Check if the passwords match
        if password != confirm_password:
            flash('Passwords do not match. Please try again.')
            return redirect(url_for('index'))

        # Save user data
        user_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password,
            'courses': [],
            'units': []
        }
        users.append(user_data)

        flash('Registration successful. Please log in.')
        return redirect(url_for('index'))

    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = next((u for u in users if u['email'] == username and u['password'] == password), None)

        if user:
            return render_template('welcome.html', user=user)
        else:
            flash('Invalid username or password. Please try again.')
            return redirect(url_for('index'))

    return render_template('index.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/register_units')
def register_units():
    return render_template('register_units.html', units=units)

@app.route('/process_register_units', methods=['POST'])
def process_register_units():
    selected_units = request.form.getlist('units')
    users[0]['units'] = selected_units
    return redirect(url_for('confirmation', message='You have successfully registered for units!', details=selected_units, return_link='/login'))

@app.route('/enroll_courses')
def enroll_courses():
    return render_template('enroll_courses.html')

@app.route('/process_enroll_courses', methods=['POST'])
def process_enroll_courses():
    course = request.form.get('course')
    academic_year = request.form.get('academic_year')

    # Check if the user is already enrolled in a course
    if users[0]['courses']:
        return redirect(url_for('index'))

    users[0]['courses'].append({'course': course, 'academic_year': academic_year})
    return redirect(url_for('confirmation', message=f'You have successfully enrolled for {course} in {academic_year}!', return_link='/login'))

@app.route('/show_fee_balance')
def show_fee_balance():
    return render_template('confirmation.html', message='Your fees balance is Ksh 2,000.', return_link='/login')

@app.route('/student_information')
def student_information():
    return render_template('student_information.html', users=users, return_link='/login')

@app.route('/confirmation')
def confirmation():
    message = request.args.get('message')
    details = request.args.get('details')
    return_link = request.args.get('return_link')

    return render_template('confirmation.html', message=message, details=details, return_link=return_link)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
