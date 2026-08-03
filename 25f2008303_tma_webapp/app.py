from flask import Flask,render_template,request,redirect,url_for,session
from database import InitialiseDB, connect

app=Flask(__name__)
app.secret_key="key"


#this fn to be used for later easy login operations nd check for password correct entry
def log(email):
    MyDB=connect()
    MC=MyDB.cursor()
    MC.execute("""SELECT * FROM users WHERE email=?""",(email,))
    u=MC.fetchone()
    MyDB.close()
    return u

#-------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="GET":
        return render_template("login.html")
    e=request.form.get("email")
    p=request.form.get("password")
    u=log(e)

    if u is None or u["password"]!=p:
        return render_template("login.html", error="Invalid email/password or user may not exist. Please check credentials again!")

    session["user_id"]=u["id"]
    session["role"]=u["role"]
    session["name"]=u["FNAME"]

    if u["role"].lower()=="admin":
        return redirect(url_for("admindash"))
    elif u["role"].lower()=="staff":
        return redirect(url_for("staffdash"))
    else:
        return redirect(url_for("userdash"))

#-------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="GET":
        return render_template("register.html")
    fn=request.form.get("FNAME")
    e=request.form.get("email")
    p=request.form.get("password")
    cp=request.form.get("confirm_password")
    role=request.form.get("role")

    if not fn or not e or not p or p!=cp:
        return render_template("register.html",error="Please enter all fields correctly and ensure not to missout any fields!")
    if role.lower() not in ("staff","user"):
        return render_template("register.html",error="Please enter the role as either User or Staff")

    if log(e) is not None:
        return render_template("register.html",error="This email is already registered!")

    MyDB=connect()
    MC=MyDB.cursor()
    MC.execute("""INSERT INTO users(FNAME,email,password,role,is_active) VALUES (?,?,?,?,?)""",(fn,e,p,role.upper(),1))
    u=MC.lastrowid
    
    if role.lower()=="staff":
        MC.execute("""INSERT INTO staff(user_id,approval_status) VALUES (?,?)""",(u,"pending"))
    MyDB.commit()
    MyDB.close()

    return redirect(url_for("login"))

#------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route("/admin/dashboard")
def admindash():
    if session.get("role","").lower()!="admin":
        return redirect(url_for("login"))
    return render_template("admindash.html")

@app.route("/staff/dashboard")
def staffdash():
    if session.get("role","").lower()!="staff":
        return redirect(url_for("login"))
    return render_template("staffdash.html")

@app.route("/user/dashboard")
def userdash():
    if session.get("role","").lower() not in ("user","trekker"):
        return redirect(url_for("login"))
    return render_template("userdash.html")

#------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

#------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__=="__main__":
    InitialiseDB()
    app.run(debug=True)

    
