import pandas as pd
from fpdf import FPDF 
from datetime import datetime
from flask import redirect, url_for, render_template

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import getpass
import numpy as np

def clean():
    import os, re, os.path
    mypath = "myfolder"

    for root, dirs, files in os.walk(mypath):
        for file in files:
            os.remove(os.path.join(root, file))

    return render_template("mysuccess.html")

def mail(df, e, p):
   
    from_, password = e, p

    to = df['Email'].to_list()
    name = df['Name'].to_list()
    success = False

    try:
        server = smtplib.SMTP('smtp.outlook.com', 587)
        server.starttls()
        server.login(from_, password)
        success = True
    except :

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(from_, password)
            success = True
        except:

            try:
                server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
                server.starttls()
                server.login(from_, password)
                success = True
            except:
                
                try:
                    server = smtplib.SMTP('smtp.rediffmailpro.com', 587)
                    server.starttls()
                    server.login(from_, password)
                    success = True
                except:
                    
                    try:
                        server = smtplib.SMTP('smtp.rediffmail.com', 25)
                        server.starttls()
                        server.login(from_, password)
                        success = True
                    except:
                        success = False
                        return render_template("myfail.html")


    if (success == True):

        for i, j in zip(to, name) :

            data = MIMEMultipart()
            data['To'] = i
            data['From'] = from_
            data['Subject'] = "IA"

            body = "Your Report"

            data.attach(MIMEText(body, 'plain'))

            p = "myfolder/{}.pdf".format(j)
            filename = p

            attachment = open(filename, "rb")

            p = MIMEBase('application', 'octet-stream')

            p.set_payload((attachment).read())

            encoders.encode_base64(p)

            p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

            data.attach(p)
            

            text = data.as_string()
            server.sendmail(from_, i, text)
            attachment.close()

        server.quit()

    else:
        return ("Enter valid email and password")

    return clean()

def process(df, emai, paswrd):

    li = df.columns

    now = datetime.now()
    dt_time = now.strftime("%d/%m/%Y %H:%M:%S")

    for i in df.values:
    
        name, email, roll, m1, m2, m3, m4, m5 = i
        
        l = []
        
        for j in [m1, m2, m3, m4, m5]:
            if j < 16:
                remark = "You need {} marks in IA2 to pass".format(16-j)
                l.append(remark)
            else:
                remark = "You have passed in IA1 and IA2"
                l.append(remark)
        
        name = "{} : {}".format(li[0], name)
        email = "{} : {}".format(li[1], email)
        roll = "{} : {}".format(li[2], roll)
        m_1 = "{} : {}  ({})".format(li[3], m1, l[0])
        m_2 = "{} : {}  ({})".format(li[4], m2, l[1])
        m_3 = "{} : {}  ({})".format(li[5], m3, l[2])
        m_4 = "{} : {}  ({})".format(li[6], m4, l[3])
        m_5 = "{} : {}  ({})".format(li[7], m5, l[4])
        
        pdf = FPDF() 
        
        pdf.add_page() 
        pdf.set_font("Arial", size = 20) 
        
        pdf.cell(200, 10, txt = "VIDYALANKAR INSTITUTE OF TECHNOLOGY, MUMBAI",  ln = 1, align = 'C')
        pdf.set_font("Arial", size = 18) 

        pdf.cell(200, 10, txt = "INFORMATION TECHNOLOGY DEPARTMENT",  ln = 2, align = 'C')
        
        pdf.set_font("Arial", size = 15) 
        pdf.cell(200, 10, txt = " ",  ln = 3, align = 'L') 
        pdf.cell(200, 10, txt = "Date : {}".format(dt_time),  ln = 4, align = 'R')
        pdf.cell(200, 10, txt = " ",  ln = 5, align = 'L') 
        
        pdf.cell(200, 10, txt = name,  ln = 6, align = 'L') 
        pdf.cell(200, 10, txt = email, ln = 7, align = 'L') 
        pdf.cell(200, 10, txt = roll, ln = 8, align = 'L')
        
        pdf.cell(200, 10, txt = "++++++++++++ IA1 ++++++++++++", ln = 9, align = 'L')
        
        pdf.cell(200, 10, txt = m_1, ln = 10, align = 'L') 
        pdf.cell(200, 10, txt = m_2, ln = 11, align = 'L') 
        pdf.cell(200, 10, txt = m_3, ln = 12, align = 'L') 
        pdf.cell(200, 10, txt = m_4, ln = 13, align = 'L') 
        pdf.cell(200, 10, txt = m_5, ln = 14, align = 'L') 
        pdf.cell(200, 10, txt = "Total : {} of 100".format(m1+m2+m3+m4+m5), ln = 15, align = 'L') 
        
        p = "myfolder/{}.pdf".format(i[0])
        pdf.output(p)

    return mail(df, emai, paswrd)

def readfile(l, e, p):

    try:
        df = pd.read_excel(l)
    except:
        try:
            df = pd.read_csv(l)
        except:
            return render_template("myfail.html")

    
    return process(df, e, p)

def arrangement(l1, l2, email, password):
    
    try:
        df = pd.read_excel(l2)
    except:
        try:
            df = pd.read_csv(l2)
        except:
            return "Failed : Check your format"

    from_, password = email, password

    to = df['Email'].to_list()
    success = False

    try:
        server = smtplib.SMTP('smtp.outlook.com', 587)
        server.starttls()
        server.login(from_, password)
        success = True
    except :

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(from_, password)
            success = True
        except:

            try:
                server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
                server.starttls()
                server.login(from_, password)
                success = True
            except:
                
                try:
                    server = smtplib.SMTP('smtp.rediffmailpro.com', 587)
                    server.starttls()
                    server.login(from_, password)
                    success = True
                except:
                    
                    try:
                        server = smtplib.SMTP('smtp.rediffmail.com', 25)
                        server.starttls()
                        server.login(from_, password)
                        success = True
                    except:
                        success = False
                        return render_template("myfail.html")
                        
    if (success == True):

        for i in to:

            data = MIMEMultipart()
            data['To'] = i
            data['From'] = from_
            data['Subject'] = "IA Seating Arrangement"

            body = "Be sure to be 30 minutes before the exam. All the best!"

            data.attach(MIMEText(body, 'plain'))

            filename = l1

            attachment = open(filename, "rb")

            p = MIMEBase('application', 'octet-stream')

            p.set_payload((attachment).read())

            encoders.encode_base64(p)

            p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

            data.attach(p)

            text = data.as_string()
            server.sendmail(from_, i, text)
            attachment.close()
        server.quit()

    else:
        return ("Enter valid email and password")

    return clean()

def process1(df, emai, paswrd):

    now = datetime.now()
    li = df.columns

    dt_time = now.strftime("%d/%m/%Y %H:%M:%S")

    for i in df.values:
        
        name, email, roll, m1, m2, m3, m4, m5, m6, m7, m8, m9, m10 = i
        
        l = []
        for j in [m6, m7, m8, m9, m10]:
            if j < 16:
                remark = "You should to have {} marks in IA1 to pass".format(16-j)
                l.append(remark)
            else:
                remark = "You have passed in IA2"
                l.append(remark)
        a = np.array([m1, m2, m3, m4, m5])
        b = np.array([m6, m7, m8, m9, m10])
        
        c = (a+b)/2
        m = []
        for j in c:
            if j >= 7:
                remarks = "You have passed in IA"
                m.append(remarks)
            else:
                remarks = "You have not passed in IA"
                m.append(remarks)
                
        name = "{} : {}".format(li[0], name)
        email = "{} : {}".format(li[1], email)
        roll = "{} : {}".format(li[2], roll)
        m_1 = "{} : {} ".format(li[3], m1)
        m_2 = "{} : {} ".format(li[4], m2)
        m_3 = "{} : {} ".format(li[5], m3)
        m_4 = "{} : {} ".format(li[6], m4)
        m_5 = "{} : {} ".format(li[7], m5)
        m_6 = "{} : {}  ({})".format(li[8], m6, m[0])
        m_7 = "{} : {}  ({})".format(li[9], m7, m[1])
        m_8 = "{} : {}  ({})".format(li[10], m8, m[2])
        m_9 = "{} : {}  ({})".format(li[11], m9, m[3])
        m_10 = "{} : {}  ({})".format(li[12], m10, m[4])
        
        pdf = FPDF() 
        
        pdf.add_page() 
        pdf.set_font("Arial", size = 20) 
        
        pdf.cell(200, 10, txt = "VIDYALANKAR INSTITUTE OF TECHNOLOGY, MUMBAI",  ln = 1, align = 'C')
        pdf.set_font("Arial", size = 18) 

        pdf.cell(200, 10, txt = "INFORMATION TECHNOLOGY DEPARTMENT",  ln = 2, align = 'C')
        
        pdf.set_font("Arial", size = 15) 
        pdf.cell(200, 10, txt = " ",  ln = 3, align = 'L') 
        pdf.cell(200, 10, txt = "Date : {}".format(dt_time),  ln = 4, align = 'R')
        pdf.cell(200, 10, txt = " ",  ln = 5, align = 'L') 
        
        pdf.cell(200, 10, txt = name,  ln = 6, align = 'L') 
        pdf.cell(200, 10, txt = email, ln = 7, align = 'L') 
        pdf.cell(200, 10, txt = roll, ln = 8, align = 'L')
        
        pdf.cell(200, 10, txt = "++++++++++++ IA1 ++++++++++++", ln = 9, align = 'L')
        
        pdf.cell(200, 10, txt = m_1, ln = 10, align = 'L') 
        pdf.cell(200, 10, txt = m_2, ln = 11, align = 'L') 
        pdf.cell(200, 10, txt = m_3, ln = 12, align = 'L') 
        pdf.cell(200, 10, txt = m_4, ln = 13, align = 'L') 
        pdf.cell(200, 10, txt = m_5, ln = 14, align = 'L') 
        pdf.cell(200, 10, txt = "Total : {} of 100".format(m1+m2+m3+m4+m5), ln = 15, align = 'L') 
        
        pdf.cell(200, 10, txt = "++++++++++++ IA2 ++++++++++++ ", ln = 16, align = 'L')
        
        pdf.cell(200, 10, txt = m_6, ln = 17, align = 'L') 
        pdf.cell(200, 10, txt = m_7, ln = 18, align = 'L') 
        pdf.cell(200, 10, txt = m_8, ln = 19, align = 'L') 
        pdf.cell(200, 10, txt = m_9, ln = 20, align = 'L') 
        pdf.cell(200, 10, txt = m_10, ln = 21, align = 'L') 
        pdf.cell(200, 10, txt = "Total : {} of 100".format(m6+m7+m8+m9+m10), ln = 22, align = 'L') 
        
        pdf.cell(200, 10, txt = "++++++++++++ IA1 + IA2 ++++++++++++ ", ln = 23, align = 'L')
        IAavg = (m1+m2+m3+m4+m5+m6+m7+m8+m9+m10)/2
        
        if IAavg >= 90:
            r = ("Outstanding")
        elif IAavg >= 80:
            r = ("Excellent")
        elif IAavg >= 70:
            r = ("Good")
        elif IAavg >= 60:
            r = ("Try Harder")
        elif IAavg >= 50:
            r = ("You can do better")
        else:
            r = ("You need to study more")
        
        pdf.cell(200, 10, txt = "Total IA avg : {} of 100".format(IAavg), ln = 24, align = 'L') 
        pdf.cell(200, 10, txt = "Total Remark : {}".format(r), ln = 25, align = 'L') 

        
        p = "myfolder/{}.pdf".format(i[0])
        pdf.output(p)

    return mail(df, emai, paswrd)


def readfile1(l, email, password):

    try:
        df = pd.read_excel(l)
    except:
        try:
            df = pd.read_csv(l)
        except:
            return render_template("myfail.html")
    
    return process1(df, email, password)