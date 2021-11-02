import random
import os
import uuid
from django.shortcuts import render
from django.http import JsonResponse

from . import Pool

def SupplierInterface(request):
    try:
        result=request.session['ADMIN']
        return render(request,'SupplierInterface.html',{'result':result})
    except Exception as e:
        return render(request,'AdminInterface.html')

def Suppliersubmit(request):
    try:

        name = request.GET['suppliername']
        number = request.GET['suppliernumber']
        mail = request.GET['suppliermail']
        address = request.GET['supplieraddress']
        state = request.GET['supplierstate']
        city = request.GET['suppliercity']

        q = "insert into supplier(suppliername,mobileno,emailid,address,state,city)values('{}','{}','{}','{}','{}','{}')".format(name,number,mail,address,state ,city)
        db, cmd = Pool.CollectionPool()
        cmd.execute(q)
        db.commit()
        db.close()

        return render(request, 'SupplierInterface.html',{'msg':"Record Successfully Submitted"})

    except Exception as e:
        print("Error:",e)
        return render(request,'SupplierInterface.html',{'msg':"Record Not Submitted"})

def DisplayAllSupplier(request):
        try:
           result = request.session['ADMIN']

           db, cmd = Pool.CollectionPool()
           q = "select *  from supplier"
           cmd.execute(q)
           rows = cmd.fetchall()
           db.close()
           return render(request, 'DisplayAllSupplier.html', {'rows': rows,'result':result})
        except Exception as e:
            print(e)
            return render(request, 'AdminInterface.html', {'rows': []})





def SupplierEditDeleteRecord(request):
    btn = request.GET['btn']
    supplierid = request.GET['supplierid']

    if (btn == 'Edit'):
        name = request.GET['suppliername']
        number = request.GET['suppliernumber']
        mail = request.GET['suppliermail']
        address = request.GET['supplieraddress']
        state = request.GET['supplierstate']
        city = request.GET['suppliercity']



        try:

            db, cmd = Pool.CollectionPool()

            q = "update  supplier set suppliername='{}' , mobileno = '{}' ,emailid='{}',address='{}',state='{}',city='{}'  where supplierid={}".format(name,number, mail,address,state,city,supplierid)
            print(q)

            cmd.execute(q)
            db.commit()

            db.close()
            return DisplayAllSupplier(request)
        except Exception as e:
            print("Error:",e)
            return DisplayAllSupplier(request)

    elif (btn == 'Delete'):

        try:
            db, cmd = Pool.CollectionPool()
            q = "delete from supplier where supplierid={}".format(supplierid)
            cmd.execute(q)
            db.commit()

            db.close()
            return DisplayAllSupplier(request)

        except Exception as e:
            return DisplayAllSupplier(request)

def GetSupplierJSON(request):
        try:
            db, cmd = Pool.CollectionPool()
            q = "select * from supplier "
            cmd.execute(q)
            rows = cmd.fetchall()
            db.close()
            return JsonResponse(rows, safe=False)

        except Exception as e:
            return JsonResponse([], safe=False)


