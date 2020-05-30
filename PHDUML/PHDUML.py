from flask import Flask,render_template,request,redirect
from flask.globals import session
from flask import *
from database import Db
import time
from werkzeug.utils import secure_filename
import os
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

ob = Db()

app = Flask(__name__)
app.secret_key="ggg"
userpic_path ="C:\\Users\\SHANi\\PycharmProjects\\PHDUML\\static\\userpic\\"
dataset="C:\\Users\\SHANi\\PycharmProjects\\PHDUML\\static\\dataset\\"
doctor_pic="C:\\Users\\SHANi\\PycharmProjects\\PHDUML\\static\\doctor_pic\\"

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/doctor_pic')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@app.route('/')
def main():
    return render_template("login_temp.html")

@app.route('/logout')
def logout():
    return redirect('/')


@app.route('/addtriningset')
def addtrainingset():
    return render_template("addtriningset.html")

@app.route('/adminhome')
def admin():
    return render_template("temp.html")

@app.route('/adminreply/<id>')
def adminreply(id):
    res=ob.selectOne("select * from complaint where id='"+id+"'")
    session["cid"]=id
    return render_template("adminreply.html", a=res)

@app.route('/adminviewdoc')
def adminviewdoc():
    q=ob.select("select * from doctor where sts='pending'")
    if len(q)>0:
        return render_template("adminviewdoc.html", a=q)
    else:
        return '''<script>alert ("There is no request"); window.location="/adminhome"</script>'''

@app.route('/adminviewrating')
def adminviewrating():
    ob=Db()
    res=ob.select("select avg(rating.rate)as rate1,doctor.* from rating, doctor where rating.did=doctor.did group by rating.did")

    return render_template("adminviewrating.html", a=res)

@app.route('/booking/<op_id>')
def booing(op_id):
    res=ob.selectOne("select doctor.dname,doctor.h_name,doctor.dimg,doctor.h_place,opschedule.* from opschedule,doctor where opschedule.did=doctor.did and opschedule.op_id='"+op_id+"'")
    return render_template("booking.html",a=res)

@app.route('/docprofile')
def docprofile():

    id=session['lid']
    q=ob.selectOne("select * from doctor where lid='"+str(id)+"'")

    return render_template("docprofile.html",a=q)

@app.route('/updatedocprofile', methods=['POST'])
def updatedocprofile():

    id=session['lid']
    n=request.form['n']
    p=request.form['p']
    s=request.form['s']
    g=request.form['g']
    d=request.form['d']
    hn=request.form['hn']
    hp=request.form['hp']
    pl = request.form['pl']
    dis = request.form['dis']
    hpo=request.form['hpo']
    hpi=request.form['hpi']
    q=request.form['q']
    picture=request.files['img']
    if picture and allowed_file(picture.filename):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = timestr + secure_filename(picture.filename)
        picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        q=ob.update("update doctor set dname='"+n+"' ,gender='"+g+"',d_dob='"+d+"',dplace='"+pl+"',dist='"+dis+"',spec='"+s+"',dimg='"+filename+"',dphone='"+p+"',h_name='"+hn+"',h_place='"+hp+"',h_post='"+hpo+"',h_pin='"+hpi+"',qualification='"+q+"' where lid='"+str(id)+"'")
    else:
        q = ob.update(
            "update doctor set dname='" + n + "' ,gender='" + g + "',d_dob='" + d + "',dplace='" + pl + "',dist='" + dis + "',spec='" + s + "',dphone='" + p + "',h_name='" + hn + "',h_place='" + hp + "',h_post='" + hpo + "',h_pin='" + hpi + "',qualification='" + q + "' where lid='" + str(id) + "'")

    return redirect('/docprofile')

@app.route('/docregistration')
def docregistration():

    return render_template("docregistration.html")

@app.route('/docviewschedule')
def docviewscedule():
    s=session['did']
    res=ob.select("select * from opschedule where did='"+str(s)+"'")

    return render_template("docviewschedule.html",a=res)

@app.route('/editopschedule/<op_id>')
def editopschedule(op_id):
    q=ob.selectOne("select * from opschedule where op_id='"+op_id+"'")
    return render_template("editopschedule.html",a=q)

@app.route('/deleteschedule/<op_id>')
def deleteschedule(op_id):
    q=ob.delete("delete from opschedule where op_id='"+op_id+"'")
    return redirect("/docviewschedule")

@app.route('/docopschedule')
def docopschedule():
    return render_template("docopschedule.html")

@app.route('/addopschedule', methods=['POST'])
def addopschedule():
    date=request.form['date']
    ftime=request.form['ftime']
    ttime=request.form['ttime']
    id=session["did"]

    q=ob.insert("insert into opschedule (did,date,f_time,t_time)values('"+str(id)+"','"+date+"','"+ftime+"','"+ttime+"')")
    if q>0:
        return '''<script>alert ("Added Successfully"); window.location="/docopschedule" </script>'''

@app.route('/updateopschedule', methods=['POST'])
def updateopschedule():
    date=request.form['date']
    ftime=request.form['ftime']
    ttime=request.form['ttime']
    id=request.form['hid']
    q=ob.update("update opschedule set date='"+date+"',f_time='"+ftime+"',t_time='"+ttime+"' where op_id='"+id+"'")

    if q>0:
        return '''<script>alert ("Updates Successfully"); window.location="/docviewschedule" </script>'''

@app.route('/usercomplaint')
def usercomplaint():
    return render_template("usercomplaint.html")

@app.route('/userfeedback/<did>')
def userfeedback(did):
    a=ob.selectOne("select * from doctor where did='"+did+"'")
    return render_template("userfeebback.html",a=a)

@app.route('/userregistration')
def userregistration():
    return render_template("user_signup.html")


@app.route('/userviewdoc')
def userviewdoc():
    return render_template("userviewdoc.html")

@app.route('/userviewreply')
def userviewreply():
    return render_template("userviewreply.html")

@app.route('/userviewschedule/<did>')
def userviewschedule(did):
    q=ob.selectOne("select * from doctor where did='"+did+"'")
    res = ob.select("select * from opschedule where did= '"+did+"' and date>=curdate()")
    if len(res)>0:
        return render_template("userviewschedule.html",a=q,data=res)
    else:
        return '''<script>alert ("Doctor not available"); window.location='/userviewdoc_post'</script>'''


@app.route('/userbooking', methods=['POST'])
def userbooking():
    id=session['u_id']
    op_id=request.form['hid']
    res=ob.insert("insert into booking values (null,'"+op_id+"' ,'"+str(id)+"' ,'pending',CURDATE())")
    return '''<script>alert ("Successfully Booked"); window.location='/userviewdoc_post'</script>'''

@app.route('/docviewbooking')
def docviewbooking():
    did=session['did']
    res=ob.select("select user.*,booking.*,opschedule.f_time,opschedule.t_time from user,booking,opschedule where booking.op_id=opschedule.op_id and booking.u_id=user.u_id and opschedule.did='"+str(did)+"' and sts='pending'")
    if len(res) == 0:
        return '''<script>alert ("No Bookings"); window.location='/docprofile'</script>'''
    return render_template("docviewbooking.html",a=res)
@app.route('/userviewbooking')
def userviewbooking():
    uid=session['u_id']
    res=ob.select("select booking.*,opschedule.*,doctor.dname,doctor.h_place,doctor.h_name from booking,doctor,opschedule where booking.u_id='"+str(uid)+"' and booking.op_id=opschedule.op_id and opschedule.did=doctor.did and booking.sts='confirm' and booking.b_date<curdate()")

    return render_template("userviewbooking.html",a=res)

@app.route('/userbookingdetails')
def userbookingdetails():
    uid=session['u_id']
    res=ob.select("select booking.*,opschedule.*,doctor.dname,doctor.h_place,doctor.h_name from booking,doctor,opschedule where booking.u_id='"+str(uid)+"' and booking.op_id=opschedule.op_id and opschedule.did=doctor.did and booking.sts!='pending' and booking.b_date>=curdate()")
    if len(res)==0:
        return '''<script>alert ("No Bookings"); window.location='/userviewprofile'</script>'''
    return render_template("userbookingdetails.html",a=res)

@app.route('/confirmbook' , methods=['POST'])
def confirmbook():

    b=request.form['sts']
    id=request.form['hid']
    if b=='Confirm':
        res=ob.update("update booking set sts='confirm' where b_id='"+id+"'")
        return redirect("/docviewbooking")
    elif b=='Reject':
        res = ob.update("update booking set sts='reject' where b_id='" + id + "'")
        return redirect("/docviewbooking")


@app.route('/viewcomplaint')
def viewcomplaint():
    return render_template("viewcomplaint.html")

@app.route('/viewmoredoc/<lid>')
def viewmoredoc(lid):

    q = ob.selectOne("select * from doctor where lid='"+lid+"'")

    return render_template("viewmoredoc.html" ,a=q)



@app.route('/viewrejecteddoc')
def viewrejecteddoc():

    res = ob.select("select doctor.* from doctor inner join login on login.l_id = doctor.lid and login.u_type = 'block'")
    if len(res)>0:
        return render_template('viewrejecteddoc.html', a = res)
    else:
        return '''<script>alert ("No result found"); window.location='/adminhome'</script>'''



@app.route('/viewschedule')
def viewschedule():
    res=ob.select("select doctor.dname,opschedule.* from opschedule,doctor where opschedule.did=doctor.did")
    return render_template("viewschedule.html",a=res)


@app.route('/viewtrainingset')
def viewtrainingset():
    q=ob.select("select * from trainingset")
    return render_template("viewtrainingset.html" ,a=q)

@app.route('/docviewmorebooking/<b_id>')
def docviewmorebooking(b_id):
    res=ob.selectOne("select booking.*,user.* from booking,user where booking.u_id=user.u_id and booking.b_id='"+b_id+"'")
    return render_template("docviewmorebooking.html",a=res)


@app.route('/userhome')
def userhome():
    return render_template("userhome.html")


@app.route('/dochome')
def dochome():
    return render_template("dochome.html")

@app.route('/check1')
def check1():
    return render_template("check1.html")

@app.route('/check2')
def check2():
    return render_template("check2.html")

@app.route('/check3')
def check3():
    return render_template("check3.html")


@app.route('/user_signup', methods=['POST'])
def user_signup():


    name = request.form['usname']
    age=request.form['dob']
    gender=request.form['r']
    place=request.form['uplace']
    dist=request.form['udist']
    ph=request.form['phone']
    uname=request.form['uname']
    pas=request.form['pass']
    cpas=request.form['cpass']
    file_name="avathar.png"
    if pas==cpas:

        res= ob.selectOne("select * from login where uname='"+uname+"'")

        if res:
            return ''' <script>alert("Email already exist");window.location='/userregistration'</script> '''

        else:
            if  request.files:

                pic = request.files['img']
                timestr = time.strftime("%Y%m%d-%H%M%S")
                file_name = timestr+pic.filename
                pic.save(userpic_path + file_name)


            qr=ob.insert("insert into login (uname,pass,u_type)values('"+uname+"','"+pas+"','user')")

            q=ob.insert("insert into user(lid,img,u_name,age,ph_no,email,gender,u_place,u_dist)values('"+str(qr)+"','"+file_name+"','"+name+"','"+age+"','"+ph+"','"+uname+"','"+gender+"','"+place+"','"+dist+"')")

            return redirect('/')
    else:
        return ''' <script> alert("Password not match");window.location='/userregistration'</script> '''


@app.route('/doctor_signup', methods=['POST'])
def doctor_signup():
    name=request.form['dname']
    gender=request.form['r']
    dob=request.form['dob']
    spec=request.form['spec']
    dplace=request.form['dplace']
    dist=request.form['ddist']
    ph=request.form['phone']
    hname=request.form['hname']
    hplace=request.form['hplace']
    hpost=request.form['hpost']
    hpin=request.form['hpin']
    exp=request.form['exp']
    qlf= request.form.getlist('c')
    email=request.form['uname']
    pas=request.form['pass']
    cpas=request.form['cpass']
    file_name = "avathar.png"

    qu = ""
    for r in qlf:
        qu+= r+","


    if pas==cpas:
        res = ob.selectOne("select * from login where uname='" + email + "'")

        if res:
            return ''' <script>alert("Email already exist");window.location='/docregistration'; </script> '''
        else:
            if request.files:
                pic = request.files['dimg']
                timestr = time.strftime("%Y%m%d-%H%M%S")
                file_name = timestr + pic.filename
                pic.save(doctor_pic + file_name)

            qr = ob.insert("insert into login (uname,pass,u_type)values('" + email + "','" + pas + "','pending')")
            q=ob.insert("insert into doctor(lid,dimg,dname,gender,d_dob,spec,dplace,dist,dphone,email,h_name,h_place,h_post,h_pin,exp,qualification,sts) values('"+str(qr)+"','"+file_name+"','"+name+"','"+gender+"','"+dob+"','"+spec+"','"+dplace+"','"+dist+"','"+ph+"','"+email+"','"+hname+"','"+hplace+"','"+hpost+"','"+hpin+"','"+exp+"','"+qu+"','pending') ")

            return redirect('/')
    else:
        return ''' <script> alert("Password not match");window.location='/docrregistration'</script> '''

@app.route('/addtrainigset_upload', methods=['POST'])
def addtrainigset_upload():
    if request.files:
        pic = request.files['u']
        timestr = time.strftime("%Y%m%d-%H%M%S")
        file_name = timestr + pic.filename
        pic.save(dataset + file_name)
    else:
        return '''<script>alert("Add files"); window.location = '/addtrainigset'</script>'''

    q=ob.insert("insert into trainingset(date,file)values(curdate(),'"+file_name+"')")

    return '''<script>alert("Added Successfully"); window.location = '/addtrinigset'</script>'''

@app.route('/addrating', methods=['POST'])
def addrating():
    did=request.form['did']
    r=request.form['r']
    id=session['lid']
    q=ob.insert("insert into rating(did,lid,date,rate,b_id)values('"+did+"','"+str(id)+"',curdate(),'"+r+"',null)")
    if q>0:
        return redirect('/userviewbooking')



@app.route('/addcomplaint', methods=['POST'])
def addcomplaint():

    sub=request.form['sub']
    txt=request.form['t1']
    id = session["lid"]


    q=ob.insert("insert into complaint(l_id,sub,complaint,c_date,reply)values('"+str(id)+"','"+sub+"','"+txt+"',curdate(),'pending')")
    if q>0:
        return render_template("usercomplaint.html")


@app.route('/addbooking')
def addbooking():
    name=request.form['uname']
    date=request.form['date']
    time=request.form['ftime']


    q=ob.insert("insert into booking(op_id,u_id,sts,b_date)values('0','0',')")
    if q>0:
        return render_template("booking.html")

@app.route('/loginmain', methods=['POST'])
def loginmain():
    name=request.form['uname']
    pas=request.form['password']

    q = ob.selectOne("select * from login where uname='"+name+"' and pass = '"+pas+"'")

    if q:

        session["lid"]=q['l_id']

        if q['u_type']=='doctor':
            res=ob.selectOne("select * from doctor where lid='"+str(session['lid'])+"'")
            session["did"]=res['did']

            return render_template("doctemp.html", a=res)

        elif q['u_type']=='user':
            res = ob.selectOne("select * from user where lid='" + str(session['lid']) + "'")
            session["u_id"] = res['u_id']

            return render_template("usertemp.html", a=res)

        elif q['u_type'] == 'admin':

            return redirect("/adminhome")
        elif q['u_type']=='pending':
            return '''<script>alert ("Your Request is Pending... Please Contact Admin"); window.location='/'</script>'''


    else:
        return '''<script>alert ("Invalid username"); window.location='/'</script>'''

@app.route('/viewregistereddoc')
def viewregistereddoc():

    res = ob.select("select doctor.* from doctor inner join login on login.l_id = doctor.lid and login.u_type = 'doctor'")
    if len(res)>0:
        return render_template('viewaproveddoc.html', data = res)
    else:
        return '''<script>alert ("No result found"); window.location='/adminhome'</script>'''
@app.route('/viewcomplaint_post')
def viewcomplaint_post():

    res = ob.select("select complaint.* , user.u_name,user.ph_no,user.img from complaint inner join user on complaint.l_id=user.lid where complaint.reply='pending'")
    if len(res)>0:
        return render_template('viewcomplaint.html', data = res)
    else:
        return '''<script>alert ("Thare is no Complaint is pending"); window.location='/adminhome'</script>'''

@app.route('/viewadminreply')
def viewadminreply():

    res = ob.select("select complaint.* , user.u_name,user.ph_no,user.img from complaint inner join user on complaint.l_id=user.lid where complaint.reply!='pending'")
    if len(res)>0:
        return render_template('viewreply.html', data = res)
    else:
        return '''<script>alert ("Thare is no Complaint is pending"); window.location='/adminhome'</script>'''

@app.route('/userviewdoc_post')
def userviewdoc_post():
    res = ob.select("select doctor.* from doctor inner join login on login.l_id = doctor.lid and login.u_type = 'doctor' ")
    if len(res)>0:
        return render_template('userviewdoc.html', data = res)
    else:
        return '''<script>alert ("No result found"); window.location='/adminhome'</script>'''

@app.route('/userviewdoc_post1')
def userviewdoc_post1():
    res = ob.select("select doctor.* from doctor inner join login on login.l_id = doctor.lid and login.u_type = 'doctor' ")
    if len(res)>0:
        return render_template('userviewdoc1.html', data = res)
    else:
        return '''<script>alert ("No result found"); window.location='/adminhome'</script>'''


@app.route('/userviewrply1')
def userviewreply1():
    a=session['lid']
    res = ob.select("select * from complaint where l_id='"+str(a)+"' and reply!='pending'")

    if len(res)>0:
        return render_template('userviewreply.html', data = res)
    else:
        return '''<script>alert ("No result found"); window.location='/userviewprofile'</script>'''

@app.route('/userviewprofile', methods=['GET','POST'])
def userhome1_post():
    a=session['lid']
    res = ob.selectOne("select * from user where lid='"+str(a)+"'  ")
    if res:
        return render_template('userhome1.html', a = res)
    else:
        return '''<script>alert ("No result found"); window.location='/usehome'</script>'''


@app.route('/updateuser', methods=['POST'])
def updateuser():
    a=session['lid']

    name = request.form['usname']
    age=request.form['dob']
    gender=request.form['r']
    place=request.form['uplace']
    dist=request.form['udist']
    ph=request.form['phone']


    s=ob.update("update user set u_name = '"+name+"',age='"+age+"',ph_no='"+ph+"',gender='"+gender+"',u_place='"+place+"',u_dist='"+dist+"' where lid='"+str(a)+"'")
    return  redirect('/userviewprofile')
@app.route('/adminreply_post', methods=['POST'])
def adminrplypost():
    r=request.form['b1']
    c=session['cid']
    q=ob.update("update complaint set reply='"+r+"' where id='"+c+"'")
    return redirect('/viewcomplaint_post')

@app.route('/approval_doc', methods=['POST'])
def approval_doc():
    id = request.form['id']
    b=request.form['b1']
    if b=="Approve":
        q=ob.update("update login set u_type ='doctor' where l_id='"+id+"'")
        q1=ob.update("update doctor set sts='Approve' where lid='"+id+"'")
        return redirect('/adminviewdoc')
    elif b=="Reject":
        q = ob.update("update login set u_type ='block' where l_id='" + id + "'")
        q1 = ob.update("update doctor set sts='Reject' where lid='" + id + "'")
        return redirect('/adminviewdoc')
    else:
        return "ok"


@app.route('/viewmoreaprvddoc/<id>')
def viewmoreaprvddoc(id):

   q=ob.selectOne("select * from doctor where lid='"+id+"'")
   return render_template("viewmoreprvddoc.html" , a=q)

@app.route('/decisiontree')
def decisiontree():

   return render_template("check1.html")

@app.route('/userDT')
def userDT():

   return render_template("userDT.html")

@app.route('/decisiontreepst', methods=['POST'])
def decisiontreepst():

    age=float(request.form['f1'])
    sex=float(request.form['f2'])
    cp=float(request.form['f3'])
    tres=float(request.form['f4'])
    chol=float(request.form['f5'])
    fbs=float(request.form['f6'])
    rest=float(request.form['f7'])
    thalch=float(request.form['f8'])
    exang=float(request.form['f9'])
    oldpeak=float(request.form['f10'])
    slope=float(request.form['f11'])
    ca=float(request.form['f12'])
    thal=float(request.form['f13'])

    test_data=[[age,sex,cp,tres,chol,fbs,rest,thalch,exang,oldpeak,slope,ca,thal]]
    dataset = pd.read_csv('C:\\Users\\SHANi\\PycharmProjects\\PHDUML\\static\\dataset\\heart1.csv', sep=',',
                          header=None)
    print(dataset)

    Xt = dataset.values[1:, 0:13]
    Ytt = dataset.values[1:, 13]

    X_train, X_test, Y_train, Y_test = train_test_split(Xt, Ytt, train_size=0.65, test_size=0.20, random_state=0)

    dt = DecisionTreeClassifier(random_state=0)
    dt.fit(X_train, Y_train)
    Y_pred_dt = dt.predict(test_data)


    if Y_pred_dt==0:
        a='Normal'
    else:
        a='Diseased'

    return render_template("check1.html",a=a)

@app.route('/userDTpst', methods=['POST'])
def userDTpst():

    age=float(request.form['f1'])
    sex=float(request.form['f2'])
    cp=float(request.form['f3'])
    tres=float(request.form['f4'])
    chol=float(request.form['f5'])
    fbs=float(request.form['f6'])
    rest=float(request.form['f7'])
    thalch=float(request.form['f8'])
    exang=float(request.form['f9'])
    oldpeak=float(request.form['f10'])
    slope=float(request.form['f11'])
    ca=float(request.form['f12'])
    thal=float(request.form['f13'])

    test_data=[[age,sex,cp,tres,chol,fbs,rest,thalch,exang,oldpeak,slope,ca,thal]]
    dataset = pd.read_csv('C:\\Users\\SHANi\\PycharmProjects\\PHDUML\\static\\dataset\\heart1.csv', sep=',',
                          header=None)
    print(dataset)

    Xt = dataset.values[1:, 0:13]
    Ytt = dataset.values[1:, 13]

    X_train, X_test, Y_train, Y_test = train_test_split(Xt, Ytt, train_size=0.65, test_size=0.20, random_state=0)

    dt = DecisionTreeClassifier(random_state=0)
    dt.fit(X_train, Y_train)
    Y_pred_dt = dt.predict(test_data)


    if Y_pred_dt==0:
        a='Normal'
    else:
        a='Diseased'

    return render_template("userDT.html",a=a)
@app.route('/logistic')
def logistic():

   return render_template("check2.html")

@app.route('/userLR')
def userLR():

   return render_template("userLR.html")

@app.route('/userLRpst', methods=['POST'])
def userLRpst():

    age=float(request.form['f1'])
    sex=float(request.form['f2'])
    cp=float(request.form['f3'])
    tres=float(request.form['f4'])
    chol=float(request.form['f5'])
    fbs=float(request.form['f6'])
    rest=float(request.form['f7'])
    thalch=float(request.form['f8'])
    exang=float(request.form['f9'])
    oldpeak=float(request.form['f10'])
    slope=float(request.form['f11'])
    ca=float(request.form['f12'])
    thal=float(request.form['f13'])

    test_data=[[age,sex,cp,tres,chol,fbs,rest,thalch,exang,oldpeak,slope,ca,thal]]
    dataset = pd.read_csv('C:\\Users\\SHANi\\PycharmProjects\\PHDUML\\static\\dataset\\heart1.csv', sep=',',header=None)

    Xt = dataset.values[1:, 0:13]
    Ytt = dataset.values[1:, 13]

    X_train, X_test, Y_train, Y_test = train_test_split(Xt, Ytt, train_size=0.65, test_size=0.20, random_state=0)


    lr = LogisticRegression(solver='saga')
    lr.fit(X_train, Y_train)
    Y_pred_lr = lr.predict(test_data)

    if Y_pred_lr==0:
        a='Normal'
    else:
        a='Diseased'

    return render_template("userLR.html",a=a)

@app.route('/logisticpst', methods=['POST'])
def logisticpst():

    age=float(request.form['f1'])
    sex=float(request.form['f2'])
    cp=float(request.form['f3'])
    tres=float(request.form['f4'])
    chol=float(request.form['f5'])
    fbs=float(request.form['f6'])
    rest=float(request.form['f7'])
    thalch=float(request.form['f8'])
    exang=float(request.form['f9'])
    oldpeak=float(request.form['f10'])
    slope=float(request.form['f11'])
    ca=float(request.form['f12'])
    thal=float(request.form['f13'])

    test_data=[[age,sex,cp,tres,chol,fbs,rest,thalch,exang,oldpeak,slope,ca,thal]]
    dataset = pd.read_csv('C:\\Users\\SHANi\\PycharmProjects\\PHDUML\\static\\dataset\\heart1.csv', sep=',',header=None)

    Xt = dataset.values[1:, 0:13]
    Ytt = dataset.values[1:, 13]

    X_train, X_test, Y_train, Y_test = train_test_split(Xt, Ytt, train_size=0.65, test_size=0.20, random_state=0)


    lr = LogisticRegression(solver='saga')
    lr.fit(X_train, Y_train)
    Y_pred_lr = lr.predict(test_data)

    if Y_pred_lr==0:
        a='Normal'
    else:
        a='Diseased'

    return render_template("check2.html",a=a)


@app.route('/svm')
def supportvm():
    return render_template("check3.html")

@app.route('/userSVM')
def userSVM():
    return render_template("userSVM.html")


@app.route('/svmpst', methods=['POST'])
def svmpst():
    age = float(request.form['f1'])
    sex = float(request.form['f2'])
    cp = float(request.form['f3'])
    tres = float(request.form['f4'])
    chol = float(request.form['f5'])
    fbs = float(request.form['f6'])
    rest = float(request.form['f7'])
    thalch = float(request.form['f8'])
    exang = float(request.form['f9'])
    oldpeak = float(request.form['f10'])
    slope = float(request.form['f11'])
    ca = float(request.form['f12'])
    thal = float(request.form['f13'])

    test_data = [[age, sex, cp, tres, chol, fbs, rest, thalch, exang, oldpeak, slope, ca, thal]]
    dataset = pd.read_csv('C:\\Users\\SHANi\\PycharmProjects\\PHDUML\\static\\dataset\\heart1.csv', sep=',', header=None)

    Xt = dataset.values[1:, 0:13]
    Ytt = dataset.values[1:, 13]

    X_train, X_test, Y_train, Y_test = train_test_split(Xt, Ytt, train_size=0.65, test_size=0.20, random_state=0)

    sv = svm.SVC(kernel='linear')
    sv.fit(X_train, Y_train)

    Y_pred_svm = sv.predict(test_data)


    if Y_pred_svm == 0:
        a = 'Normal'
    else:
        a = 'Diseased'

    return render_template("check3.html", a=a)

@app.route('/userSVMpst', methods=['POST'])
def userSVMpst():
    age = float(request.form['f1'])
    sex = float(request.form['f2'])
    cp = float(request.form['f3'])
    tres = float(request.form['f4'])
    chol = float(request.form['f5'])
    fbs = float(request.form['f6'])
    rest = float(request.form['f7'])
    thalch = float(request.form['f8'])
    exang = float(request.form['f9'])
    oldpeak = float(request.form['f10'])
    slope = float(request.form['f11'])
    ca = float(request.form['f12'])
    thal = float(request.form['f13'])

    test_data = [[age, sex, cp, tres, chol, fbs, rest, thalch, exang, oldpeak, slope, ca, thal]]
    dataset = pd.read_csv('C:\\Users\\SHANi\\PycharmProjects\\PHDUML\\static\\dataset\\heart1.csv', sep=',', header=None)

    Xt = dataset.values[1:, 0:13]
    Ytt = dataset.values[1:, 13]

    X_train, X_test, Y_train, Y_test = train_test_split(Xt, Ytt, train_size=0.65, test_size=0.20, random_state=0)

    sv = svm.SVC(kernel='linear')
    sv.fit(X_train, Y_train)

    Y_pred_svm = sv.predict(test_data)


    if Y_pred_svm == 0:
        a = 'Normal'
    else:
        a = 'Diseased'

    return render_template("userSVM.html", a=a)

@app.route('/randmforest')
def randmforest():
    return render_template("randomforest.html")

@app.route('/userRF')
def userRF():
    return render_template("userRF.html")


@app.route('/randmforestpst', methods=['POST'])
def randmforestpst():
    age = float(request.form['f1'])
    sex = float(request.form['f2'])
    cp = float(request.form['f3'])
    tres = float(request.form['f4'])
    chol = float(request.form['f5'])
    fbs = float(request.form['f6'])
    rest = float(request.form['f7'])
    thalch = float(request.form['f8'])
    exang = float(request.form['f9'])
    oldpeak = float(request.form['f10'])
    slope = float(request.form['f11'])
    ca = float(request.form['f12'])
    thal = float(request.form['f13'])

    test_data = [[age, sex, cp, tres, chol, fbs, rest, thalch, exang, oldpeak, slope, ca, thal]]
    dataset = pd.read_csv('C:\\Users\\SHANi\\PycharmProjects\\PHDUML\\static\\dataset\\heart1.csv', sep=',', header=None)

    Xt = dataset.values[1:, 0:13]
    Ytt = dataset.values[1:, 13]

    X_train, X_test, Y_train, Y_test = train_test_split(Xt, Ytt, train_size=0.65, test_size=0.20, random_state=0)

    rfc = RandomForestClassifier()
    rfc.fit(X_train, Y_train)
    rfc_predict = rfc.predict(test_data)

    if rfc_predict == 0:
        a = 'Normal'
    else:
        a = 'Diseased'

    return render_template("randomforest.html", a=a)

@app.route('/userRFpst', methods=['POST'])
def userRFpst():
    age = float(request.form['f1'])
    sex = float(request.form['f2'])
    cp = float(request.form['f3'])
    tres = float(request.form['f4'])
    chol = float(request.form['f5'])
    fbs = float(request.form['f6'])
    rest = float(request.form['f7'])
    thalch = float(request.form['f8'])
    exang = float(request.form['f9'])
    oldpeak = float(request.form['f10'])
    slope = float(request.form['f11'])
    ca = float(request.form['f12'])
    thal = float(request.form['f13'])

    test_data = [[age, sex, cp, tres, chol, fbs, rest, thalch, exang, oldpeak, slope, ca, thal]]
    dataset = pd.read_csv('C:\\Users\\SHANi\\PycharmProjects\\PHDUML\\static\\dataset\\heart1.csv', sep=',', header=None)

    Xt = dataset.values[1:, 0:13]
    Ytt = dataset.values[1:, 13]

    X_train, X_test, Y_train, Y_test = train_test_split(Xt, Ytt, train_size=0.65, test_size=0.20, random_state=0)

    rfc = RandomForestClassifier()
    rfc.fit(X_train, Y_train)
    rfc_predict = rfc.predict(test_data)

    if rfc_predict == 0:
        a = 'Normal'
    else:
        a = 'Diseased'

    return render_template("userRF.html", a=a)

@app.route('/naive')
def naive():
    return render_template("naive.html")

@app.route('/userNB')
def userNB():
    return render_template("userNB.html")

@app.route('/naivepst', methods=['POST'])
def naivepst():
    age = float(request.form['f1'])
    sex = float(request.form['f2'])
    cp = float(request.form['f3'])
    tres = float(request.form['f4'])
    chol = float(request.form['f5'])
    fbs = float(request.form['f6'])
    rest = float(request.form['f7'])
    thalch = float(request.form['f8'])
    exang = float(request.form['f9'])
    oldpeak = float(request.form['f10'])
    slope = float(request.form['f11'])
    ca = float(request.form['f12'])
    thal = float(request.form['f13'])

    test_data = [[age, sex, cp, tres, chol, fbs, rest, thalch, exang, oldpeak, slope, ca, thal]]
    dataset = pd.read_csv('C:\\Users\\SHANi\\PycharmProjects\\PHDUML\\static\\dataset\\heart1.csv', sep=',', header=None)

    Xt = dataset.values[1:, 0:13]
    Ytt = dataset.values[1:, 13]

    X_train, X_test, Y_train, Y_test = train_test_split(Xt, Ytt, train_size=0.65, test_size=0.20, random_state=0)
    from sklearn.naive_bayes import GaussianNB

    # Create a Gaussian Classifier
    rfc = GaussianNB()
    rfc.fit(X_train, Y_train)
    rfc_predict = rfc.predict(test_data)

    if rfc_predict == 0:
        a = 'Normal'
    else:
        a = 'Diseased'

    return render_template("naive.html", a=a)

@app.route('/userNBpst', methods=['POST'])
def userNBpst():
    age = float(request.form['f1'])
    sex = float(request.form['f2'])
    cp = float(request.form['f3'])
    tres = float(request.form['f4'])
    chol = float(request.form['f5'])
    fbs = float(request.form['f6'])
    rest = float(request.form['f7'])
    thalch = float(request.form['f8'])
    exang = float(request.form['f9'])
    oldpeak = float(request.form['f10'])
    slope = float(request.form['f11'])
    ca = float(request.form['f12'])
    thal = float(request.form['f13'])

    test_data = [[age, sex, cp, tres, chol, fbs, rest, thalch, exang, oldpeak, slope, ca, thal]]
    dataset = pd.read_csv('C:\\Users\\SHANi\\PycharmProjects\\PHDUML\\static\\dataset\\heart1.csv', sep=',', header=None)

    Xt = dataset.values[1:, 0:13]
    Ytt = dataset.values[1:, 13]

    X_train, X_test, Y_train, Y_test = train_test_split(Xt, Ytt, train_size=0.65, test_size=0.20, random_state=0)
    from sklearn.naive_bayes import GaussianNB

    # Create a Gaussian Classifier
    rfc = GaussianNB()
    rfc.fit(X_train, Y_train)
    rfc_predict = rfc.predict(test_data)

    if rfc_predict == 0:
        a = 'Normal'
    else:
        a = 'Diseased'

    return render_template("userNB.html", a=a)

@app.route('/tensfl')
def tensfl():
    return render_template("tensorflow.html")

@app.route('/userTF')
def userTF():
    return render_template("userTF.html")


@app.route('/tensflpst', methods=['POST'])
def tensflpst():
    import numpy as np
    from sklearn.preprocessing import LabelEncoder, StandardScaler
    import warnings
    warnings.filterwarnings('ignore')
    age = float(request.form['f1'])
    sex = float(request.form['f2'])
    cp = float(request.form['f3'])
    tres = float(request.form['f4'])
    chol = float(request.form['f5'])
    fbs = float(request.form['f6'])
    rest = float(request.form['f7'])
    thalch = float(request.form['f8'])
    exang = float(request.form['f9'])
    oldpeak = float(request.form['f10'])
    slope = float(request.form['f11'])
    ca = float(request.form['f12'])
    thal = float(request.form['f13'])

    test_data = [[age, sex, cp, tres, chol, fbs, rest, thalch, exang, oldpeak, slope, ca, thal]]
    dataset = pd.read_csv('C:\\Users\\SHANi\\PycharmProjects\\PHDUML\\static\\dataset\\heart1.csv', sep=',', header=None)

    Xt = dataset.values[1:, 0:13]
    Ytt = dataset.values[1:, 13]

    X_train, X_test, Y_train, Y_test = train_test_split(Xt, Ytt, train_size=0.65, test_size=0.20, random_state=0)

    from keras import models
    from keras import layers

    model = models.Sequential()
    model.add(layers.Dense(256, activation='relu', input_shape=(X_train.shape[1],)))

    model.add(layers.Dense(128, activation='relu'))

    model.add(layers.Dense(64, activation='relu'))

    model.add(layers.Dense(10, activation='softmax'))

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    history = model.fit(X_train,
                        Y_train,
                        epochs=20,
                        batch_size=128)
    x = np.array(test_data)
    predictions = model.predict_classes(x)


    if predictions == 0:
        a = 'Normal'
    else:
        a = 'Diseased'

    return render_template("tensorflow.html", a=a)

@app.route('/userTFpst', methods=['POST'])
def userTFpst():
    import numpy as np
    from sklearn.preprocessing import LabelEncoder, StandardScaler
    import warnings
    warnings.filterwarnings('ignore')
    age = float(request.form['f1'])
    sex = float(request.form['f2'])
    cp = float(request.form['f3'])
    tres = float(request.form['f4'])
    chol = float(request.form['f5'])
    fbs = float(request.form['f6'])
    rest = float(request.form['f7'])
    thalch = float(request.form['f8'])
    exang = float(request.form['f9'])
    oldpeak = float(request.form['f10'])
    slope = float(request.form['f11'])
    ca = float(request.form['f12'])
    thal = float(request.form['f13'])

    test_data = [[age, sex, cp, tres, chol, fbs, rest, thalch, exang, oldpeak, slope, ca, thal]]
    dataset = pd.read_csv('C:\\Users\\SHANi\\PycharmProjects\\PHDUML\\static\\dataset\\heart1.csv', sep=',', header=None)

    Xt = dataset.values[1:, 0:13]
    Ytt = dataset.values[1:, 13]

    X_train, X_test, Y_train, Y_test = train_test_split(Xt, Ytt, train_size=0.65, test_size=0.20, random_state=0)

    from keras import models
    from keras import layers

    model = models.Sequential()
    model.add(layers.Dense(256, activation='relu', input_shape=(X_train.shape[1],)))

    model.add(layers.Dense(128, activation='relu'))

    model.add(layers.Dense(64, activation='relu'))

    model.add(layers.Dense(10, activation='softmax'))

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    history = model.fit(X_train,
                        Y_train,
                        epochs=20,
                        batch_size=128)
    x = np.array(test_data)
    predictions = model.predict_classes(x)


    if predictions == 0:
        a = 'Normal'
    else:
        a = 'Diseased'

    return render_template("userTF.html", a=a)

@app.route('/dectreeabt')
def dectreeabt():
    dataset = pd.read_csv('C:\\Users\\SHANi\\PycharmProjects\\PHDUML\\static\\dataset\\heart1.csv', sep=',', header=None)
    Xt = dataset.values[1:, 0:13]
    Ytt = dataset.values[1:, 13]
    X_train, X_test, Y_train, Y_test = train_test_split(Xt, Ytt, train_size=0.65, test_size=0.20, random_state=0)

    dt = DecisionTreeClassifier(random_state=0)
    dt.fit(X_train, Y_train)
    Y_pred_dt = dt.predict(X_test)

    s = round(accuracy_score(Y_test, Y_pred_dt) * 100, 2)

    matrix = confusion_matrix(Y_test, Y_pred_dt)

    TP = matrix[0][0]
    TN = matrix[0][1]
    FP = matrix[1][0]
    FN = matrix[1][1]
    t = [s, TP, TN, FP, FN]

    return render_template("zzdectreeabt.html",a=t)

@app.route('/svmabt')
def svmabt():
    dataset = pd.read_csv('C:\\Users\\SHANi\\PycharmProjects\\PHDUML\\static\\dataset\\heart1.csv', sep=',', header=None)
    Xt = dataset.values[1:, 0:13]
    Ytt = dataset.values[1:, 13]
    X_train, X_test, Y_train, Y_test = train_test_split(Xt, Ytt, train_size=0.65, test_size=0.20, random_state=0)

    sv = svm.SVC(kernel='linear')
    sv.fit(X_train, Y_train)
    Y_pred_svm = sv.predict(X_test)

    s = round(accuracy_score(Y_test, Y_pred_svm) * 100, 2)

    matrix = confusion_matrix(Y_test, Y_pred_svm)

    TP = matrix[0][0]
    TN = matrix[0][1]
    FP = matrix[1][0]
    FN = matrix[1][1]
    t = [s, TP, TN, FP, FN]

    return render_template("zzsvmabt.html",a=t)

@app.route('/logregabt')
def logregabt():
    dataset = pd.read_csv('C:\\Users\\SHANi\\PycharmProjects\\PHDUML\\static\\dataset\\heart1.csv', sep=',', header=None)
    Xt = dataset.values[1:, 0:13]
    Ytt = dataset.values[1:, 13]
    X_train, X_test, Y_train, Y_test = train_test_split(Xt, Ytt, train_size=0.65, test_size=0.20, random_state=0)

    lr = LogisticRegression(solver='saga')
    lr.fit(X_train, Y_train)
    Y_pred_lr = lr.predict(X_test)

    s = round(accuracy_score(Y_test, Y_pred_lr) * 100, 2)

    matrix = confusion_matrix(Y_test, Y_pred_lr)

    TP = matrix[0][0]
    TN = matrix[0][1]
    FP = matrix[1][0]
    FN = matrix[1][1]
    t = [s, TP, TN, FP, FN]

    return render_template("zzLogRegabt.html",a=t)

@app.route('/rfabt')
def rfabt():
    dataset = pd.read_csv('C:\\Users\\SHANi\\PycharmProjects\\PHDUML\\static\\dataset\\heart1.csv', sep=',', header=None)
    Xt = dataset.values[1:, 0:13]
    Ytt = dataset.values[1:, 13]
    X_train, X_test, Y_train, Y_test = train_test_split(Xt, Ytt, train_size=0.65, test_size=0.20, random_state=0)

    rfc = RandomForestClassifier()
    rfc.fit(X_train, Y_train)
    rfc_predict = rfc.predict(X_test)

    s = round(accuracy_score( Y_test,rfc_predict) * 100, 2)

    matrix = confusion_matrix(Y_test, rfc_predict)

    TP = matrix[0][0]
    TN = matrix[0][1]
    FP = matrix[1][0]
    FN = matrix[1][1]
    t = [s, TP, TN, FP, FN]

    return render_template("zzrfabt.html",a=t)

@app.route('/nbabt')
def nbabt():
    dataset = pd.read_csv('C:\\Users\\SHANi\\PycharmProjects\\PHDUML\\static\\dataset\\heart1.csv', sep=',',header=None)

    Xt = dataset.values[1:, 0:13]
    Ytt = dataset.values[1:, 13]

    X_train, X_test, Y_train, Y_test = train_test_split(Xt, Ytt, train_size=0.65, test_size=0.20, random_state=0)
    from sklearn.naive_bayes import GaussianNB

    # Create a Gaussian Classifier
    rfc = GaussianNB()
    rfc.fit(X_train, Y_train)
    rfc_predict = rfc.predict(X_test)

    s = round(accuracy_score( Y_test,rfc_predict) * 100, 2)

    matrix = confusion_matrix(Y_test, rfc_predict)

    TP = matrix[0][0]
    TN = matrix[0][1]
    FP = matrix[1][0]
    FN = matrix[1][1]
    t = [s, TP, TN, FP, FN]

    return render_template("zznaiveabt.html",a=t)

@app.route('/tfabt')
def tfabt():
    dataset = pd.read_csv('C:\\Users\\SHANi\\PycharmProjects\\PHDUML\\static\\dataset\\heart1.csv', sep=',',
                          header=None)

    Xt = dataset.values[1:, 0:13]
    Ytt = dataset.values[1:, 13]

    X_train, X_test, Y_train, Y_test = train_test_split(Xt, Ytt, train_size=0.65, test_size=0.20, random_state=0)

    from keras import models
    from keras import layers

    model = models.Sequential()
    model.add(layers.Dense(256, activation='relu', input_shape=(X_train.shape[1],)))

    model.add(layers.Dense(128, activation='relu'))

    model.add(layers.Dense(64, activation='relu'))

    model.add(layers.Dense(10, activation='softmax'))

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    history = model.fit(X_train, Y_train, epochs=20, batch_size=128)
    x = np.array(X_test)
    predictions = model.predict_classes(x)

    s = round(accuracy_score(Y_test, predictions) * 100, 2)

    matrix = confusion_matrix(Y_test, predictions)

    TP = matrix[0][0]
    TN = matrix[0][1]
    FP = matrix[1][0]
    FN = matrix[1][1]
    t = [s, TP, TN, FP, FN]

    return render_template("zzttabt.html",a=t)

# -----------chat with ndoctor-------------------------
@app.route('/chat/<did>')
def chat(did):
    session['q']=did

    return render_template("chat.html", a=did)


@app.route('/chatpst', methods=['POST'])
def chatpst():
    did=session['q']
    c=request.form['c']
    lid=session['lid']

    qry="insert into chat(f_id,t_id,mes,date)values('"+str(lid)+"','"+str(did)+"','"+c+"',curdate())"
    res=ob.insert(qry)
    return render_template("chat.html", a=did)

@app.route('/chatchk', methods=['POST'])
def chatchk():
    did=session['q']
    lid=session['lid']
    toid = request.form['idd']
    qry="select * from chat where (f_id='"+str(lid)+"' and t_id='"+str(toid)+"') or (f_id='"+str(toid)+"' and t_id='"+str(lid)+"') order by id desc"
    res=ob.select(qry)
    if len(res) > 0:
        return jsonify(res)

@app.route('/docchatview')
def docchatview():
    did=session['lid']
    # qry="select chat.*,user.* from chat,user where chat.f_id=user.lid and chat.t_id='"+str(did)+"'"
    qry="select * from (select chat.*,user.* from chat,user where chat.f_id=user.lid and chat.t_id='11' ORDER BY id DESC) as ids group by f_id"
    res=ob.select(qry)

    if len(res)>0:
        return render_template("docchatview.html", a=res)
    else:
        return '''<script>alert ("No Messages"); window.location='/docviewbooking'</script>'''

@app.route('/chatdoc/<lid>')
def chatdoc(lid):
    session['qw']=lid

    return render_template("docchat.html", a=lid)
@app.route('/docchatpst', methods=['POST'])
def docchatpst():
    lid=session['qw']
    c=request.form['c']
    did=session['lid']

    qry="insert into chat(f_id,t_id,mes,date)values('"+str(did)+"','"+str(lid)+"','"+c+"',curdate())"
    res=ob.insert(qry)
    return render_template("docchat.html", a=lid)
@app.route('/docchatchk', methods=['POST'])
def docchatchk():
    did=session['qw']
    lid=session['lid']
    toid = request.form['idd']
    qry="select * from chat where (f_id='"+str(lid)+"' and t_id='"+str(toid)+"') or (f_id='"+str(toid)+"' and t_id='"+str(lid)+"') order by id desc"
    res=ob.select(qry)
    if len(res) > 0:
        return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True,port=4000)
