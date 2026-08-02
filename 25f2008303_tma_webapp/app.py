import flask
from database import InitialiseDB

app=flask.Flask(__name__)
app.secret_key="key"

@app.route("/")
def home():
    return flask.render_template("home.html")

if __name__=="__main__":
    InitialiseDB()
    app.run(debug=True)

    
