from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
from pytz import timezone
import pytz

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change to a real secret key in production

# List of time zones (shortened for demonstration)
timezones = ['Pacific/Auckland', 'Australia/Sydney', 'Asia/Tokyo', 'Europe/London',
             'Europe/Berlin', 'America/New_York', 'America/Los_Angeles', 'America/Sao_Paulo']

@app.route('/', methods=['GET', 'POST'])
def select_locations():
    if request.method == 'POST':
        session['location1'] = request.form['location1']
        session['location2'] = request.form['location2']
        return redirect(url_for('select_format'))
    return render_template('select_locations.html', timezones=timezones)

@app.route('/select_format', methods=['GET', 'POST'])
def select_format():
    if request.method == 'POST':
        session['time_format'] = request.form['time_format']
        return redirect(url_for('enter_time'))
    return render_template('select_format.html')

@app.route('/enter_time', methods=['GET', 'POST'])
def enter_time():
    if request.method == 'POST':
        user_time = request.form['user_time']
        format_string = "%Y-%m-%d %H:%M:%S"
        naive_dt = datetime.strptime(user_time, format_string)
        tz1 = timezone(session['location1'])
        tz2 = timezone(session['location2'])
        localized_dt = tz1.localize(naive_dt)
        tz2_dt = localized_dt.astimezone(tz2)
        if session['time_format'] == '12':
            final_time = tz2_dt.strftime('%Y-%m-%d %I:%M:%S %p')
        else:
            final_time = tz2_dt.strftime('%Y-%m-%d %H:%M:%S')
        session['final_time'] = final_time
        return redirect(url_for('results'))
    return render_template('enter_time.html', location2=session['location2'])

@app.route('/results')
def results():
    final_time = session.get('final_time', 'No time converted')
    return render_template('results.html', final_time=final_time)

if __name__ == "__main__":
    app.run(debug=True)
