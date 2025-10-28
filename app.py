from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username:
        return "Username is required"
    if not password:
        return "Password is required"
    if len(password) < 6:
        return "Password too short"
    return "Registration successful"

if __name__ == '__main__':
    app.run(debug=True)
