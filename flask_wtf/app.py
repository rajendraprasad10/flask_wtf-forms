from flask import Flask, render_template
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, PasswordField, IntegerField, BooleanField, Form, FormField, FieldList,DateField
from wtforms.validators import InputRequired, Length, AnyOf, Email
from collections import namedtuple
# app configs
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Mysecret!'
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_SECRET_KEY'] = 'ADifferentSecret!'
app.config['WTF_CSRF_TIME_LIMIT'] = 3600
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LdCOsIUAAAAAMG4yO_vlS54s_gLBTLsnSrGsUBs'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LdCOsIUAAAAAISalDIPHIP4QGw7ainnG_yfYxyd'
# telephonic form
class TelephoneForm(Form):
    country_code = IntegerField('country code')
    area_code = IntegerField('area code')
    number = StringField('number')
# year form.
class YearForm(Form):
    year = IntegerField('year')
    total = IntegerField('total')

# login form
class LoginForm(FlaskForm):
    username = StringField('Your Username', validators=[InputRequired('A username is required!'), Length(min=4, max=8, message='Must be between 4 and 8 characters')])
    password = PasswordField('password', validators=[InputRequired('Password is required!'), AnyOf(values=['secret', 'password'])])
    age = IntegerField('age', default=24)
    true = BooleanField('Click here')
    email = StringField('email', validators=[Email()])
    home_phone = FormField(TelephoneForm)
    mobile_phone = FormField(TelephoneForm)
    years = FieldList(FormField(YearForm))
    recaptcha = RecaptchaField()
    date = DateField('date',format = '%Y-%m-%d')

# name form
class NameForm(LoginForm):
    first_name = StringField('first name')
    last_name = StringField('last name')

class User:
    def __init__(self, username, age, email):
        self.username = username
        self.age = age
        self.email = email

@app.route('/', methods=['GET', 'POST'])
def index():
    myuser = User('rajendra', 58, 'rajendra@gmail.com')

   # group = namedtuple('Group', ['year', 'total'])
    #g1 = group(2005, 1000)
    #g2 = group(2006, 1500)
    #g3 = group(2007, 1700)

    #years = {'years' : [g1, g2, g3]}

    form = NameForm(obj=myuser)#data=years

    #del form.mobile_phone

    if form.validate_on_submit():
        return '<h1>Username: {} Password: {} Age: {} True: {} Email: {}, Date: {}</h1>'.format(form.username.data, form.password.data, form.age.data, form.true.data, form.email.data,form.date.data)
        return '<h1>Country code: {}, Area code: {}, Number: {}'.format(form.mobile_phone.country_code.data, form.home_phone.area_code.data, form.home_phone.number.data)

       #output = '<h1>'

        #for f in form.years:
         #   output += 'Year: {}'.format(f.year.data)
          #  output += 'Total: {} <br>'.format(f.total.data)

        #output += '</h1>'

        #return output'''

    return render_template('index.html', form=form)


# dynamic forms
@app.route('/dynamic', methods = ['GET','POST'])
def dynamic():

    class DynamicForm(FlaskForm):
        pass
    DynamicForm.name = StringField('name')
    names = ['first_name', 'last_name', 'nik_name','midle_name']

    for name in names:
        setattr(DynamicForm, name, StringField(name))
    form = DynamicForm()

    if form.validate_on_submit():
        return '<h1> the name: {}'.format(form.name.data, form.date.data, form[name].data)
    
    return render_template('dynamic.html',form = form, names = names)
if __name__ == '__main__':
    app.run(debug=True)