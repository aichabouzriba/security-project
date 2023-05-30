from flask import Flask, render_template, request

import random
import string

app = Flask(__name__)

# password checker backend

def check_length(password):
    if len(password) >= 12:
        return True
    return False


def check_symbol(password):
    symbols = "!\@#$%^&*()-+?_=,<>/'.:;[]`{}|~\" "
    if any(ch in symbols for ch in password):
        return True
    else:
        return False


def check_upper_alpha(password):
    if any(ch.isupper() for ch in password):
        return True
    return False


def check_lower_alpha(password):
    if any(ch.islower() for ch in password):
        return True
    return False


def check_digits(password):
    if any(ch.isdigit() for ch in password):
        return True
    return False


def check_PersonalInfo(password, fname, lname, pnbr, bdate):
    bd = bdate.replace("-", "")
    if fname in password:
        return False
    elif lname in password:
        return False
    elif pnbr in password:
        return False
    elif bd in password:
        return False
    else:
        return True


def checkIfInList(word):
    with open("dictionary/mostcommon.txt", "r", encoding="utf-8", errors="ignore") as f:
        contents = f.read()

    common_words = contents.split("\n")

    if (word.lower() in common_words):
            return True
    return False


def reverseVal(word):
    val = word[::-1]
    if checkIfInList(val):
        return True
    return False




def check_password(password, fname, lname, pnbr, bdate):
    arr = []
    if not check_length(password):
        arr.append("- Password does not meet the minimum recommended length of 12.")
    if not check_symbol(password):
        arr.append("- Password does not contain any symbols.")
    if not check_upper_alpha(password):
        arr.append("- Password does not contain any upper case letters.")
    if not check_lower_alpha(password):
        arr.append("- Password does not contain any lower case letters.")
    if not check_digits(password):
        arr.append("- Password does not contain any digits.")
    if not check_PersonalInfo(password, fname, lname, pnbr, bdate):
        arr.append("- Password contains personal information.")
    if checkIfInList(password):
        arr.append("- Password is a dictionary word.")
    if reverseVal(password):
        arr.append("- Password is a reversed dictionary word.")
    if (len(arr) == 0):
        arr.append("- Password has no vulnerabilities!")
    return arr


def password_score(password, fname, lname, pnbr, bdate):
    s=8
    if not check_length(password):
        s-=1
    if not check_symbol(password):
        s-=1
    if not check_upper_alpha(password):
        s-=1
    if not check_lower_alpha(password):
        s-=1
    if not check_digits(password):
        s-=1
    if not check_PersonalInfo(password, fname, lname, pnbr, bdate):
        s-=1
    if checkIfInList(password):
        s-=1
    if reverseVal(password):
        s-=1

    return s


#  password generator backend

def generate_password():
    all_letters = string.ascii_letters

    lower = all_letters[0:len(all_letters)//2]  # lowercase letters

    upper = all_letters[len(all_letters)//2:]  # uppercase letters

    numbers = string.digits  # numbers

    symbols = string.punctuation  # symbols

    mixed = lower + upper + numbers + symbols

    length = random.randint(12,15)

    password = random.sample(mixed, length)

    password = "".join(password)

    return password


#  passphrase generator backend

def generate_passphrase():
    with open("dictionary/Adjectives.txt", "r", encoding="utf-8", errors="ignore") as f:
        adj = f.read()
    adjectives = adj.split("\n")

    with open("dictionary/Subjects.txt", "r", encoding="utf-8", errors="ignore") as f:
        sbj = f.read()
    subjects = sbj.split("\n")

    with open("dictionary/Verbs.txt", "r", encoding="utf-8", errors="ignore") as f:
        vrb = f.read()
    verbs = vrb.split("\n")

    a= random.choice(adjectives)
    s= random.choice(subjects)
    v= random.choice(verbs)

    passphrase = a +' '+ s +' '+ v

    return passphrase


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/generate')
def generate():
    return render_template('generate.html')


@app.route('/strength_checker', methods=('GET', 'POST'))
def StrengthChecker():
    output = []
    if request.method == 'POST':
        fname = request.form.get('fn')
        lname = request.form.get('ln')
        pnbr = request.form.get('pn')
        bdate = request.form.get('bd')
        password = request.form.get('password')

        output = check_password(password, fname, lname, pnbr, bdate )
        score = password_score(password, fname, lname, pnbr, bdate)

    return render_template('test.html', output=output, score=score)


@app.route("/password_gen", methods=('GET','POST'))
def PasswordGenerator():
    output1 = []
    if request.method == 'POST':
        output1 = generate_password()

    return render_template('generate.html', output1=output1)


@app.route("/passphrase_gen", methods=('GET','POST'))
def PassphraseGenerator():
    output2 = []
    if request.method == 'POST':
        output2 = generate_passphrase()

    return render_template('generate.html', output2=output2)



if __name__ == '__main__':
    app.run(debug=True)