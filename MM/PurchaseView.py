import random
import os
import uuid
from django.shortcuts import render
from . import Pool

def PurchaseInterface(request):
    try:
        result=request.session['EMPLOYEE']
        return render(request,'PurchaseInterface.html',{'result':result})
    except Exception as e:
        return render(request,'EmployeeLogin.html')

def Purchasesubmit(request):
    try:

        employeeid = request.GET['employeeid']
        categoryid = request.GET['categoryid']
        subcategoryid = request.GET['subcategoryid']
        productid = request.GET['productid']
        finalproductid = request.GET['finalproductid']
        stock = request.GET['stock']
        dob= request.GET['purchasedate']
        supplierid= request.GET['supplierid']
        amount= request.GET['amount']

        q = "insert into purchase(employeeid,categoryid,subcategoryid,productid,finalproductid,stock,dateofpurchase,supplierid,amount)values({},{},{},{},{},{},'{}',{},{})".format(employeeid,categoryid,subcategoryid,productid,finalproductid ,stock,dob,supplierid,amount)
        db, cmd = Pool.CollectionPool()
        cmd.execute(q)
        #update stock
        q = "update finalproducts set price=((price+{})/2), stock=stock+{} where finalproductid={}".format(amount, stock,finalproductid)
        cmd.execute(q)


        db.commit()
        db.close()

        return render(request, 'PurchaseInterface.html',{'msg':"Record Successfully Submitted"})

    except Exception as e:
        print("Error:",e)
        return render(request,'PurchaseInterface.html',{'msg':"Record Not Submitted"})

def DisplayAllPurchase(request):
        try:
           result = request.session['ADMIN']

           db, cmd = Pool.CollectionPool()
           q = "select PUR.* ,(select C.categoryname from categories C where C.categoryid= PUR.categoryid),(select S.subcategoryname from subcategories S where S.subcategoryid = PUR.subcategoryid),(select P.name from products P where P.productid = PUR.productid),(select FP.finalproductname from finalproducts FP where FP.productid = PUR.productid)   from purchase PUR"
           cmd.execute(q)
           rows = cmd.fetchall()
           db.close()
           return render(request, 'DisplayAllPurchase.html', {'rows': rows})
        except Exception as e:
            print(e)
            return render(request, 'EmployeeLogin.html', {'rows': []})





def PurchaseEditDeleteRecord(request):
    btn = request.GET['btn']
    transactionid = request.GET['transactionid']

    if (btn == 'Edit'):
        employeeid = request.GET['employeeid']
        categoryid = request.GET['categoryid']
        subcategoryid = request.GET['subcategoryid']
        productid = request.GET['productid']
        finalproductid = request.GET['finalproductid']
        stock = request.GET['stock']
        dob = request.GET['dateofpurchase']


        try:

            db, cmd = Pool.CollectionPool()

            q = "update  purchase set employeeid={} , categoryid = {} ,subcategoryid={},productid={},finalproductid={},stock='{}',dateofpurchase='{}'  where transactionid={}".format(employeeid,categoryid, subcategoryid,productid,finalproductid,stock,dob,transactionid)
            print(q)

            cmd.execute(q)
            db.commit()

            db.close()
            return DisplayAllPurchase(request)
        except Exception as e:
            print("Error:",e)
            return DisplayAllPurchase(request)

    elif (btn == 'Delete'):

        try:
            db, cmd = Pool.CollectionPool()
            q = "delete from purchase where transactionid={}".format(transactionid)
            cmd.execute(q)
            db.commit()

            db.close()
            return DisplayAllPurchase(request)

        except Exception as e:
            return DisplayAllPurchase(request)




