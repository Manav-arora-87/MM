import random
import os
from . import SendSms,EmailService
from django.shortcuts import render
from django.http import JsonResponse

from . import PoolDict,Pool
import uuid
from django.views.decorators.clickjacking import xframe_options_exempt

def EmployeeDashboard(request):
    try:
        result = request.session['EMPLOYEE']

        return render(request,'EmployeeDashboard.html',{'result':result})
    except Exception as e:
        return render(request,'Employeelogin.html')


def EmployeeLogout(request):
    del request.session['EMPLOYEE']
    return render(request, "EmployeeLogin.html")


@xframe_options_exempt
def EmployeeInterface(request):
    try:
        result = request.session['ADMIN']
        #result=request.session['EMPLOYEE']
        return render(request, 'EmployeeInterface.html',{'result':result})

    except Exception as e:
        return render(request,'AdminInterface.html')

@xframe_options_exempt
def EmployeeLogin(request):
        return render(request, 'EmployeeLogin.html')


def CheckEmployeeLogin(request):

       try:
            result=request.session['EMPLOYEE']
            return render(request, "EmployeeDashboard.html", {'result': result})
       except  Exception as e:
           pass
       try:
         emailid = request.POST['emailid']
         password = request.POST['password']
         db,cmd = PoolDict.CollectionPool()
         q = "select * from employee where email='{}' and password='{}'".format(emailid,password)
         cmd.execute(q)
         result = cmd.fetchone()
         print(q)
         if(result):
            request.session['EMPLOYEE']=result
            return render(request, "EmployeeDashboard.html", {'result': result})
         else:
            return render(request, "EmployeeLogin.html", {'result': result,'msg':'Invalid Userid or Password'})

         db.close()
       except Exception as e:
          print("Error :",e)
          return render(request,"EmployeeLogin.html",{'result':{} ,'msg':'Server Error'})


@xframe_options_exempt
def EmployeeSubmit(request):
     try:
        result = request.session['ADMIN']

        firstname=request.POST['firstname']
        lastname = request.POST['lastname']
        birthdate = request.POST['birthdate']
        gender = request.POST['gender']
        paddress = request.POST['paddress']
        state = request.POST['state']
        city = request.POST['city']
        caddress = request.POST['caddress']
        emailaddress = request.POST['emailaddress']
        mobilenumber = request.POST['mobilenumber']
        designation = request.POST['designation']
        picture = request.FILES['picture']
        filename = str(uuid.uuid4())+picture.name[picture.name.rfind('.'):]
        password = "".join(random.sample(['!', '@', '#', '$', '%', 'e', 'a', 'k', 'n', '4', '5'], k=7))
        q = "insert into employee(firstname, lastname, gender, dob, paddress, stateid, cityid, caddress, email, mobileno, designation, picture, password)values('{}','{}','{}','{}','{}',{},{},'{}','{}','{}','{}','{}','{}')".format( firstname, lastname, gender, birthdate, paddress, state, city, caddress, emailaddress, mobilenumber, designation, filename, password)
        db,cmd = Pool.CollectionPool()
        cmd.execute(q)
        db.commit()
        F = open("E:/MM/assets/"+filename,"wb")

        for chunk in picture.chunks():
            F.write(chunk)
        F.close()
        db.close()
        r = SendSms.SendMessage("Hi {} Your Password is {}".format(firstname, password), mobilenumber)
        print("========================")
        print(r.json())
        print("========================")
        EmailService.SendMail(emailaddress,"Hi {} Your Password is {}".format(firstname, password))
       # EmailService.SendHTMLMail(emailaddress,"Hi {} Your Password is {}".format(firstname, password))
        return render(request,'EmployeeInterface.html',{'msg':'Record Successfully Submitted'})
     except Exception as e:
        print(e)
        return render(request, 'EmployeeInterface.html',{'msg':'Record Not Submitted'})


@xframe_options_exempt
def DisplayAllEmployee(request):
        try:
            #result = request.session['EMPLOYEE']
            result = request.session['ADMIN']
            print(result)
            db,cmd = Pool.CollectionPool()
            q = "select E.* ,(select C.cityname from cities C where C.cityid = E.cityid),(select S.statename from states S where S.stateid = E.stateid) from employee E "
            cmd.execute(q)
            rows = cmd.fetchall()
            db.close()
            return render(request, 'DisplayAll.html',{'rows':rows,'result':result})
        except Exception as e:
            return render(request, 'AdminInterface.html',{'rows':[]})




@xframe_options_exempt
def DisplayById(request):
        empid= request.GET['empid']
        try:
            db,cmd = Pool.CollectionPool()
            q = "select E.* ,(select C.cityname from cities C where C.cityid = E.cityid),(select S.statename from states S where S.stateid = E.stateid) from employee E where employeeid={} ".format(empid)
            cmd.execute(q)
            row = cmd.fetchone()
            db.close()
            return render(request, 'DisplayEmployeeById.html',{'row':row})
        except Exception as e:
            return render(request, 'DisplayEmployeeById.html',{'row':[]})


@xframe_options_exempt
def EditDeleteRecord(request):
        btn= request.GET['btn']
        if(btn=='Edit'):

         empid= request.GET['empid']
         firstname = request.GET['firstname']
         lastname = request.GET['lastname']
         birthdate = request.GET['birthdate']
         gender = request.GET['gender']
         paddress = request.GET['paddress']
         state = request.GET['state']
         city = request.GET['city']
         caddress = request.GET['caddress']
         emailaddress = request.GET['emailaddress']
         mobilenumber = request.GET['mobilenumber']
         designation = request.GET['designation']

         try:
            db,cmd = Pool.CollectionPool()
            q = "update  employee set firstname='{}', lastname='{}', gender='{}', dob='{}', paddress='{}', stateid={}, cityid={}, caddress='{}', email='{}', mobileno='{}', designation='{}' where employeeid={}".format(firstname, lastname, gender, birthdate, paddress, state, city, caddress, emailaddress, mobilenumber,designation,empid)
            cmd.execute(q)
            db.commit()

            db.close()
            return DisplayAllEmployee(request)
         except Exception as e:
             return DisplayAllEmployee(request)

        elif(btn=='Delete'):
            empid = request.GET['empid']

            try:
                db, cmd = Pool.CollectionPool()
                q = "delete from employee where employeeid={}".format(empid)
                cmd.execute(q)
                db.commit()

                db.close()
                return DisplayAllEmployee(request)



            except Exception as e:
                return DisplayAllEmployee(request)



@xframe_options_exempt
def EditEmployeePicture(request):
    try:
        empid = request.GET['empid']
        firstname = request.GET['firstname']
        lastname = request.GET['lastname']
        picture = request.GET['picture']
        row=[empid,firstname,lastname,picture]
        return render(request, 'EditEmployeePicture.html', {'row': row})
    except Exception as e:
        return render(request, 'EditEmployeePicture.html', {'row': row})


@xframe_options_exempt
def SaveEditPicture(request):
    try:
        empid=request.POST['empid']
        oldpicture=request.POST['oldpicture']
        picture = request.FILES['picture']
        filename = str(uuid.uuid4())+picture.name[picture.name.rfind('.'):]
        q = "update employee set picture='{}' where employeeid={}      ".format(filename,empid)
        db,cmd = Pool.CollectionPool()
        cmd.execute(q)
        db.commit()
        F = open("E:/MM/assets/"+filename,"wb")

        for chunk in picture.chunks():
            F.write(chunk)
        F.close()
        db.close()
        os.remove('E:/MM/assets/'+oldpicture)
        return DisplayAllEmployee(request)
    except Exception as e:
        print(e)
        return DisplayAllEmployee(request)

def UpdateProfilePicture(request):
    try:
        result = request.session['EMPLOYEE']
        print(result)

        empid=request.POST['empid']
        oldpicture=request.POST['oldpicture']
        picture = request.FILES['picture']
        filename = str(uuid.uuid4())+picture.name[picture.name.rfind('.'):]
        q = "update employee set picture='{}' where employeeid={}      ".format(filename,empid)
        db,cmd = Pool.CollectionPool()
        cmd.execute(q)
        db.commit()
        F = open("E:/MM/assets/"+filename,"wb")

        for chunk in picture.chunks():
            F.write(chunk)
        F.close()
        db.close()
        os.remove('E:/MM/assets/'+oldpicture)

        result['picture']=filename
        return EmployeeDashboard(request)
    except Exception as e:
        print(e)
        return EmployeeDashboard(request)




def GetEmployeeJSON(request):
        try:
            result = request.session['ADMIN']
            db, cmd = Pool.CollectionPool()
            q = "select * from employee "
            cmd.execute(q)
            rows = cmd.fetchall()
            db.close()
            return JsonResponse(rows, safe=False)

        except Exception as e:
            return JsonResponse([], safe=False)