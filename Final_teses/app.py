from flask import (
        redirect, render_template, request, session, url_for, Flask
)

application = Flask(__name__)

@application.route("/")
def index():
    return render_template('index.html')

@application.route("/index.html")
def home():
    return render_template('index.html')

@application.route("/Experimento.html")
def Experimento():
    return render_template('Experimento.html')

@application.route("/FAQ.html")
def FAQ():
    return render_template('FAQ.html')

@application.route("/Sugestoes.html")
def Sugestoes():
    return render_template('Sugestoes.html')

@application.route("/experimento_strobo.html")
def experimento_strobo():
    return render_template('experimento_strobo.html')

@application.route("/teoria.html")
def teoria():
    return render_template('teoria.html')

if __name__ == "__main__":
    application.run(host="0.0.0.0", port='8080')
