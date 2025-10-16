from builtins import property
from itertools import product

from flask import Flask, render_template, flash, request, session
from flask import render_template, redirect, url_for, request
import mysql.connector
import datetime
import time

app = Flask(__name__)
app.config['DEBUG']
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/AdminLogin")
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route("/UserLogin")
def UserLogin():
    return render_template('UserLogin.html')


@app.route("/NewUser")
def NewUser():
    return render_template('NewUser.html')


@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2vehicleQrcodedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb ")
    data = cur.fetchall()

    return render_template('AdminHome.html', data=data)


@app.route("/ComplaintInfo")
def ComplaintInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2vehicleQrcodedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM complainttb   ")
    data = cur.fetchall()

    return render_template('ComplaintInfo.html', data=data)


@app.route("/AdminReport")
def AdminReport():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2vehicleQrcodedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM entrytb  ")
    data = cur.fetchall()
    return render_template('AdminReport.html', data=data)


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    error = None
    if request.method == 'POST':

        if request.form['Name'] == 'admin' and request.form['Password'] == 'admin':
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2vehicleQrcodedb')

            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb ")
            data = cur.fetchall()

            return render_template('AdminHome.html', data=data)

        else:
            data = "UserName or Password Incorrect!"

            return render_template('goback.html', data=data)


@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        name = request.form['t1']

        mobile = request.form['t2']
        email = request.form['t3']
        vno = request.form['t6']
        username = request.form['t4']
        Password = request.form['t5']
        vtype = request.form['vtype']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2vehicleQrcodedb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' or  VehicleNo='" + vno + "'")
        data = cursor.fetchone()
        if data:
            data = "Already Register  VehicleNo Or UserName!"
            return render_template('goback.html', data=data)

        else:

            import qrcode
            img = qrcode.make(str(vno))
            import random
            pn = random.randint(1111, 9999)
            img.save("static/Qrcode/" + str(pn) + ".png")
            Qrcode = str(pn) + ".png"

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2vehicleQrcodedb')
            cursor = conn.cursor()
            cursor.execute(
                "insert into regtb values('','" + name + "','" + mobile + "','" + email + "','" + vno + "','" + username + "','" + Password + "','" +
                vtype + "','" + Qrcode + "')")
            conn.commit()
            conn.close()
            data = "Record Saved!"

            outFileName = 'static/Qrcode/' + Qrcode

            import smtplib
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            from email.mime.base import MIMEBase
            from email import encoders

            fromaddr = "projectmailm@gmail.com"
            toaddr = email

            # instance of MIMEMultipart
            msg = MIMEMultipart()

            # storing the senders email address
            msg['From'] = fromaddr

            # storing the receivers email address
            msg['To'] = toaddr

            # storing the subject
            msg['Subject'] = "Qr Code"

            # string to store the body of the mail
            body = "Vehicle Document"

            # attach the body with the msg instance
            msg.attach(MIMEText(body, 'plain'))

            # open the file to be sent
            filename = Qrcode
            attachment = open(outFileName, "rb")

            # instance of MIMEBase and named as p
            p = MIMEBase('application', 'octet-stream')

            # To change the payload into encoded form
            p.set_payload((attachment).read())

            # encode into base64
            encoders.encode_base64(p)

            p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

            # attach the instance 'p' to instance 'msg'
            msg.attach(p)

            # creates SMTP session
            s = smtplib.SMTP('smtp.gmail.com', 587)

            # start TLS for security
            s.starttls()

            # Authentication
            s.login(fromaddr, "qmgn xecl bkqv musr")

            # Converts the Multipart msg into a string
            text = msg.as_string()

            # sending the mail
            s.sendmail(fromaddr, toaddr, text)

            # terminating the session
            s.quit()
            return render_template('goback.html', data=data)


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        username = request.form['Name']
        password = request.form['Password']
        # session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2vehicleQrcodedb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            alert = 'Username or Password is wrong'
            return render_template('goback.html', data=alert)



        else:
            session['vno'] = data[4]
            session['uname'] = data[5]
            session['mob'] = data[2]

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2vehicleQrcodedb')
            # cursor = conn.cursor()
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where username='" + username + "' and Password='" + password + "'")
            data = cur.fetchall()

            return render_template('UserHome.html', data=data)


@app.route("/UserHome")
def UserHome():
    username = session['uname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2vehicleQrcodedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb  where username='" + username + "' ")
    data = cur.fetchall()
    return render_template('UserHome.html', data=data)


@app.route("/NewInsurance")
def NewInsurance():
    username = session['uname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2vehicleQrcodedb')
    cur = conn.cursor()
    cur.execute("SELECT VehicleNo FROM regtb  where username='" + username + "' ")
    data = cur.fetchall()
    return render_template('NewInsurance.html', data=data)


@app.route("/newinsure", methods=['GET', 'POST'])
def newinsure():
    if request.method == 'POST':
        t1 = request.form['t1']

        t2 = request.form['t2']
        t3 = request.form['t3']
        t4 = request.form['t4']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2vehicleQrcodedb')
        cursor = conn.cursor()
        cursor.execute(
            "insert into insuratb values('','" + t1 + "','" + session[
                'mob'] + "','" + t2 + "','" + t3 + "','" + t4 + "')")
        conn.commit()
        conn.close()

    data = "Record Saved!"

    return render_template('goback.html', data=data)


@app.route("/InsuranceInfo")
def InsuranceInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2vehicleQrcodedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM insuratb  where Mobile='" + session[
        'mob'] + "' ")
    data = cur.fetchall()
    return render_template('InsuranceInfo.html', data=data)


@app.route("/Complaint")
def Complaint():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2vehicleQrcodedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM complainttb  where Mobile='" + session[
        'mob'] + "' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2vehicleQrcodedb')
    cur = conn.cursor()
    cur.execute("SELECT VehicleNo FROM regtb  where username='" + session[
        'uname'] + "' ")
    data1 = cur.fetchall()
    return render_template('NewComplaint.html', data=data, data1=data1)


@app.route("/newcom", methods=['GET', 'POST'])
def newcom():
    if request.method == 'POST':
        username = session['uname']
        mobi = session['mob']
        t1 = request.form['t1']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2vehicleQrcodedb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM  regtb  where  VehicleNo	='" + t1 + "'")
        data = cursor.fetchone()

        if data:
            VehicleType = data[7]

        t2 = request.form['t2']
        import datetime
        date = datetime.datetime.now().strftime('%Y-%m-%d')

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2vehicleQrcodedb')
        cursor = conn.cursor()
        cursor.execute(
            "insert into complainttb values('','" + username + "','" + mobi + "','" + t1 + "','" + t2 + "','" + date + "','waiting','" + VehicleType + "')")
        conn.commit()
        conn.close()

    data = "Record Saved!"
    return render_template('goback.html', data=data)


@app.route("/Fine")
def Fine():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2vehicleQrcodedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  entrytb  where VehicleNo='" + session['vno'] + "' and Status='NotPaid' ")
    data = cur.fetchall()

    return render_template('Fine.html', data=data)


@app.route("/pay")
def pay():
    id = request.args.get('id')
    session['cid'] = id
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2vehicleQrcodedb')
    cursor = conn.cursor()
    cursor.execute("SELECT  FineAmount  FROM  entrytb where  id	='" + id + "'")
    data = cursor.fetchone()

    if data:
        Amt = data[0]

        return render_template('payment.html', amt=Amt)


@app.route("/payamount", methods=['GET', 'POST'])
def payamount():
    if request.method == 'POST':
        id = session['cid']
        conn = mysql.connector.connect(user='root', password='', host='localhost',
                                       database='2vehicleQrcodedb')
        cursor = conn.cursor()
        cursor.execute("update  entrytb set Status='Paid'   where id='" + str(id) + "' ")
        conn.commit()
        conn.close()
    data = "Payment successful!"
    return render_template('goback.html', data=data)


@app.route("/Verification")
def Verification():
    import cv2
    print('hai')
    cam = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    while True:
        _, img = cam.read()
        data, bbox, _ = detector.detectAndDecode(img)
        if data:

            session['pid'] = data

            print(data)

            conn = mysql.connector.connect(user='root', password='', host='localhost',
                                           database='2vehicleQrcodedb')
            cursor = conn.cursor()
            cursor.execute(
                "select * from insuratb where VehicleNo='" + str(data) + "' and  ExpiryDate < '" + date + "' ")
            data = cursor.fetchone()
            if data is None:
                print("VehilceNo Not Found")

            else:
                mob = data[2]
                conn = mysql.connector.connect(user='root', password='', host='localhost',
                                               database='1numberhelmetdb')
                cursor = conn.cursor()
                cursor.execute(
                    "select * from entrytb where Date='" + str(date) + "' and VehicleNo='" + str(data) + "'")
                data = cursor.fetchone()
                if data is None:
                    conn = mysql.connector.connect(user='root', password='', host='localhost',
                                                   database='2vehicleQrcodedb')
                    cursor = conn.cursor()
                    cursor.execute(
                        "insert into entrytb values('','" + str(data) + "','" + str(
                            date) + "','" + str(
                            timeStamp) + "','500','NotPaid')")
                    conn.commit()
                    conn.close()
                    print("Fine Amount Info Saved")

                    sendmsg(mob, " Fine Amount For Insurance Date expiry  RS.500")

                    vnoo = data
                    cam.release()
                    cv2.destroyAllWindows()

                    conn = mysql.connector.connect(user='root', password='', host='localhost',
                                                   database='2vehicleQrcodedb')
                    # cursor = conn.cursor()
                    cur = conn.cursor()
                    cur.execute("SELECT * FROM entrytb ")
                    data = cur.fetchall()
                    return render_template('AdminReport.html', data=data)


        else:
            cam.release()
            cv2.destroyAllWindows()

            flash('Qr code Not valid')
            return render_template('AdminReport.html')

        cv2.imshow("img", img)
        if cv2.waitKey(1) == ord("Q"):
            break
    cam.release()
    cv2.destroyAllWindows()


@app.route("/QrCodeVerify")
def QrCodeVerify():
    import cv2
    cam = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    while True:
        _, img = cam.read()
        data, bbox, _ = detector.detectAndDecode(img)
        if data:

            session['pid'] = data

            print(data)

            ts = time.time()
            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

            conn = mysql.connector.connect(user='root', password='', host='localhost',
                                           database='2vehicleQrcodedb')
            cursor = conn.cursor()
            cursor.execute(
                "select * from insuratb where VehicleNo='" + str(data) + "' and  ExpiryDate < '" + date + "' ")
            data1 = cursor.fetchone()
            if data1 is None:

                cam.release()
                cv2.destroyAllWindows()

                flash('Qr code Not valid')

                return render_template('AdminReport.html')
            else:

                mob = data1[2]
                print(mob)
                conn = mysql.connector.connect(user='root', password='', host='localhost',
                                               database='2vehicleQrcodedb')
                cursor = conn.cursor()
                cursor.execute(
                    "select * from entrytb where Date='" + str(date) + "' and VehicleNo='" + str(data) + "'")
                data2 = cursor.fetchone()
                if data2 is None:
                    conn = mysql.connector.connect(user='root', password='', host='localhost',
                                                   database='2vehicleQrcodedb')
                    cursor = conn.cursor()
                    cursor.execute(
                        "insert into entrytb values('','" + str(data) + "','" + str(
                            date) + "','" + str(
                            timeStamp) + "','500','NotPaid')")
                    conn.commit()
                    conn.close()
                    print("Fine Amount Info Saved")

                    sendmsg(mob, "Fine Amount For Insurance Date expiry RS.500")

                    vnoo = data
                    cam.release()
                    cv2.destroyAllWindows()

                    conn = mysql.connector.connect(user='root', password='', host='localhost',
                                                   database='2vehicleQrcodedb')
                    # cursor = conn.cursor()
                    cur = conn.cursor()
                    cur.execute("SELECT * FROM entrytb ")
                    data = cur.fetchall()
                    return render_template('AdminReport.html', data=data)


        cv2.imshow("img", img)
        if cv2.waitKey(1) == ord("Q"):
            break

    cam.release()
    cv2.destroyAllWindows()




def sendmsg(targetno,message):
    import requests
    requests.post(
        "http://sms.creativepoint.in/api/push.json?apikey=6555c521622c1&route=transsms&sender=FSSMSS&mobileno=" + targetno + "&text=Dear customer your msg is " + message + "  Sent By FSMSG FSSMSS")



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
