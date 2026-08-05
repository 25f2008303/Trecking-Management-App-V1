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

#------------------------------------------------------------------------------------------------------------------------------------------------------

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
        MC.execute("""INSERT INTO staff(user_id,appstat) VALUES (?,?)""",(u,"pending"))
    MyDB.commit()
    MyDB.close()

    return redirect(url_for("login"))

#------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route("/admin/dashboard", methods=["GET","POST"])
def admindash():
    if session.get("role","").lower()!="admin":
        return redirect(url_for("login"))

    MyDB=connect()
    MC=MyDB.cursor()

    if request.method=="POST":
        tn=request.form.get("trek_name")
        loc=request.form.get("location")
        diff=request.form.get("difficulty")
        duration=request.form.get("duration_in_days")
        avail=request.form.get("available_slots")
        sd=request.form.get("start_date")
        ed=request.form.get("end_date")
        asid=request.form.get("assigned_staffid")

        MC.execute("""INSERT INTO treks(trek_name,location,difficulty,duration_in_days,available_slots,start_date,end_date,status,assigned_staffid) VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?)""",(tn,loc,diff,int(duration),int(avail),sd,ed,"open",asid if asid else None))

        MyDB.commit()
        MyDB.close()
        return redirect(url_for("admindash"))

    MC.execute("""SELECT COUNT(*) AS tu FROM users WHERE role='USER'""")
    tu=MC.fetchone()["tu"]

    MC.execute("""SELECT COUNT(*) AS ts FROM users WHERE role='STAFF'""")
    ts=MC.fetchone()["ts"]

    MC.execute("""SELECT COUNT(*) AS tt FROM treks""")
    tt=MC.fetchone()["tt"]

    MC.execute("""SELECT COUNT(*) AS tb FROM bookings""")
    tb=MC.fetchone()["tb"]

    MC.execute("""SELECT treks.*, users.FNAME AS staff_name FROM treks LEFT JOIN users ON treks.assigned_staffid = users.id ORDER BY treks.id DESC""")
    treks=MC.fetchall()

    MC.execute("""SELECT id,FNAME FROM users WHERE role='STAFF' ORDER BY FNAME""")
    staff_list=MC.fetchall()

    MyDB.close()

    return render_template("admindash.html",
        total_users=tu,
        total_staff=ts,
        total_treks=tt,
        total_bookings=tb,
        treks=treks,
        staff_list=staff_list)

@app.route("/admin/dashboard/trekedit/<int:id1>", methods=["GET","POST"])
def trekedit(id1):
    if session.get("role","").lower()!="admin":
        return redirect(url_for("login"))
    MyDB=connect()
    MC=MyDB.cursor()

    if request.method=="POST":
        tn=request.form.get("trek_name")
        loc=request.form.get("location")
        diff=request.form.get("difficulty")
        duration=request.form.get("duration_in_days")
        avail=request.form.get("available_slots")
        sd=request.form.get("start_date")
        ed=request.form.get("end_date")
        status=request.form.get("status")
        asid=request.form.get("assigned_staffid")

        MC.execute("""UPDATE treks SET trek_name=?,location=?,difficulty=?,duration_in_days=?,available_slots=?,start_date=?,
                end_date=?,status=?,assigned_staffid=? WHERE id=?""",(tn,loc,diff,int(duration),int(avail),sd,ed,status,asid if asid else None,id1))

        MyDB.commit()
        MyDB.close()
        
        return redirect(url_for("admindash"))
    MC.execute("SELECT * FROM treks WHERE id=?",(id1,))
    t=MC.fetchone()
    
    MC.execute("SELECT id, FNAME FROM users WHERE role='STAFF' ORDER BY FNAME")
    sl=MC.fetchall()

    MyDB.close()
    return render_template("trekedit.html",trek=t,staff_list=sl)

@app.route("/admin/dashboard/trekdel/<int:id1>")
def trekdel(id1):
    if session.get("role","").lower()!="admin":
        return redirect(url_for("login"))

    MyDB=connect()
    MC=MyDB.cursor()

    MC.execute("DELETE FROM treks WHERE id=?",(id1,))

    MyDB.commit()
    MyDB.close()
    return redirect(url_for("admindash"))

#------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route("/staff/dashboard",methods=["GET","POST"])
def staffdash():
    if session.get("role","").lower()!="staff":
        return redirect(url_for("login"))

    MyDB=connect()
    MC=MyDB.cursor()

    MC.execute("""SELECT * FROM treks WHERE assigned_staffid=? ORDER by id DESC""",(session.get("user_id"),))
    at=MC.fetchall()

    MyDB.close()

    return render_template("staffdash.html",assigned_treks=at)


@app.route("/staff/dashboard/managetreks/<int:id1>",methods=["GET","POST"]) 
def trekman(id1):
    if session.get("role","").lower()!="staff":
        return redirect(url_for("login"))
    MyDB=connect()
    MC=MyDB.cursor()

    if request.method=="POST":
        status=request.form.get("status")
        MC.execute("""UPDATE treks SET status=? WHERE id=? AND assigned_staffid=?""",(status,id1, session.get("user_id")))
        MyDB.commit()
        MyDB.close()
        
        return redirect(url_for("trekman",id1=id1))

    MC.execute("""SELECT * FROM treks WHERE id=? AND assigned_staffid = ?""",(id1, session.get("user_id")))
    t=MC.fetchone()
    MyDB.close()

    if t is None:
        return redirect(url_for("staffdash"))

    return render_template("trekman.html",trek=t)

#------------------------------------------------------------------------------------------------------------------------------------------------------    

@app.route("/user/dashboard")
def userdash():
    if session.get("role", "").lower() not in ("user", "trekker"):
        return redirect(url_for("login"))
    return render_template("userdash.html")


@app.route("/user/dashboard/availtreks")
def availtreks():
    if session.get("role","").lower() not in ("user","trekker"):
        return redirect(url_for("login"))
    
    MyDB=connect()
    MC=MyDB.cursor()
    
    MC.execute("""SELECT * FROM treks WHERE status='open' AND available_slots > 0 AND id NOT IN(SELECT trek_id FROM bookings WHERE user_id=? AND status IN
                ('booked','started','completed')) ORDER BY id DESC""",(session.get("user_id"),))
    t=MC.fetchall()

    MyDB.close()
    return render_template("availtreks.html",treks=t)

@app.route("/user/dashboard/currtreks")
def currtreks():
    if session.get("role","").lower() not in ("user","trekker"):
        return redirect(url_for("login"))

    MyDB=connect()
    MC=MyDB.cursor()

    MC.execute("""SELECT b.*, t.status as stat1, t.trek_name,t.location,t.start_date,t.end_date FROM bookings b JOIN treks t ON b.trek_id=t.id WHERE b.user_id=?
                AND b.status='booked' and t.status!='completed' ORDER BY b.id DESC""",(session.get("user_id"),))
    cb=MC.fetchall()

    MyDB.close()
    return render_template("currtreks.html",current=cb)
    
@app.route("/user/dashboard/trekhist")
def trekhist():
    if session.get("role","").lower() not in ("user","trekker"):
        return redirect(url_for("login"))

    MyDB=connect()
    MC=MyDB.cursor()

    MC.execute("""SELECT b.*,t.trek_name,t.location,t.start_date,t.end_date,t.duration_in_days FROM bookings b JOIN treks t ON b.trek_id=t.id
                WHERE b.user_id=? AND t.status IN ('completed') ORDER BY b.id DESC""",(session.get("user_id"),))
    hb=MC.fetchall()

    MyDB.close()
    return render_template("trekhist.html",history=hb)

#routes for looking and booking in one of the available treks:
@app.route("/user/dashboard/availtreks/booking/<int:id1>")
def trekdetails(id1):
    if session.get("role","").lower() not in ("user","trekker"):
        return redirect(url_for("login"))

    MyDB=connect()
    MC=MyDB.cursor()

    MC.execute("""SELECT * FROM treks WHERE id=? AND status='open' AND available_slots > 0""",(id1,))
    t=MC.fetchone()
    MyDB.close()
    
    return render_template("trekdetails.html",trek=t)

@app.route("/user/dashboard/availtreks/booking/<int:id1>/confirm",methods=["GET","POST"])
def trekconfirm(id1):
    if session.get("role","").lower() not in ("user", "trekker"):
        return redirect(url_for("login"))

    MyDB=connect()
    MC=MyDB.cursor()
    
    MC.execute("""INSERT INTO bookings(user_id,trek_id,booking_date,status) VALUES (?,?,date('now'),'booked')""",(session.get("user_id"),id1))
    MC.execute("""UPDATE treks SET available_slots=available_slots-1 WHERE id=? AND available_slots > 0""",(id1,))
    MyDB.commit()
    MyDB.close()

    return render_template("trekconfirm.html")

#route for cancelling booked trek
@app.route("/user/dashboard/currtreks/manage/<int:id1>")
def managebooking(id1):
    if session.get("role","").lower() not in ("user","trekker"):
        return redirect(url_for("login"))
    
    MyDB=connect()
    MC=MyDB.cursor()
    MC.execute("""SELECT b.trek_id,b.id,b.user_id,t.* FROM bookings b JOIN treks t ON b.trek_id=t.id WHERE b.id=? AND b.user_id=?"""
                ,(id1,session.get("user_id")))
    b=MC.fetchone()
    MyDB.close()

    return render_template("managebooking.html",booking=b)

@app.route("/user/dashboard/currtreks/manage/<int:id1>/cancel",methods=["GET","POST"])
def cancel(id1):
    if session.get("role","").lower() not in ("user","trekker"):
        return redirect(url_for("login"))
    
    MyDB=connect()
    MC=MyDB.cursor()

    MC.execute("""SELECT b.trek_id,b.id,b.user_id,t.* FROM bookings b JOIN treks t ON b.trek_id=t.id WHERE b.id=? AND b.user_id=?"""
                ,(id1,session.get("user_id")))
    b=MC.fetchone()
    
    if b is not None:
        MC.execute("""DELETE FROM bookings WHERE id=?""",(id1,))
        MC.execute("""UPDATE treks SET available_slots=available_slots+1 WHERE id=?""",(b["trek_id"],))
        MyDB.commit()
        
    MyDB.close()
    return render_template("cancel.html")

#------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

#------------------------------------------------------------------------------------------------------------------------------------------------------


if __name__=="__main__":
    InitialiseDB()
    app.run(debug=True)

    
