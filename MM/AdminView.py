from django.shortcuts import render
import uuid
import random
import os
from django.shortcuts import render
from django.http import JsonResponse

from . import PoolDict,Pool
import uuid

def AdminLogout(request):
    del request.session['ADMIN']
    return render(request, "AdminInterface.html")


def AdminInterface(request):
    try:
        result=request.session['ADMIN']
        print(result)
        return render(request, "AdminDashboard.html", {'result': result})

    except:

         return render(request,'AdminInterface.html')

def AdminDashboard(request):
    try:
        result=request.session['ADMIN']
        print(result)
        return render(request,'AdminDashboard.html',{'result':result})
    except:

        return render(request, 'AdminInterface.html')

def CheckAdminLogin(request):
    try:
        result = request.session['ADMIN']
        return render(request, "AdminDashboard.html", {'result': result})
    except  Exception as e:
        pass
    try:
        emailid = request.POST['emailid']
        password = request.POST['password']
        db, cmd = PoolDict.CollectionPool()
        q = "select * from admins where emailid='{}' and password='{}'".format(emailid, password)

        cmd.execute(q)
        result = cmd.fetchone()

        if (result):
            request.session['ADMIN'] = result
            return render(request, "AdminDashboard.html", {'result': result})
        else:
            return render(request, "AdminInterface.html", {'result': result, 'msg': 'Invalid Userid or Password'})

        db.close()
    except Exception as e:
          print("Error :", e)
          return render(request, "AdminInterface.html", {'result': {}, 'msg': 'Server Error'})



def AdminUpdateProfilePicture(request):
    try:
        result = request.session['ADMIN']

        adminid=request.POST['adminid']
        oldpicture=request.POST['oldpicture']
        picture = request.FILES['picture']
        filename = str(uuid.uuid4())+picture.name[picture.name.rfind('.'):]
        q = "update admins set picture='{}' where adminid={}".format(filename,adminid)
        print(q)
        db,cmd = Pool.CollectionPool()
        cmd.execute(q)
        db.commit()
        F = open("E:/MM/assets/"+filename,"wb")

        for chunk in picture.chunks():
            F.write(chunk)
        F.close()
        db.close()
        os.remove('E:/MM/assets/'+oldpicture)
        return AdminDashboard(request)
    except Exception as e:
        print(e)
        return AdminDashboard(request)


