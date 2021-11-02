import random
import os
import uuid
from django.shortcuts import render
from . import Pool

def IssueInterface(request):
    try:
       result=request.session['EMPLOYEE']
       return render(request,'IssueInterface.html',{'result':result})
    except Exception as e:
        return render(request,'EmployeeLogin.html')

def Issuesubmit(request):
    try:

        employeeid = request.GET['employeeid']
        categoryid = request.GET['categoryid']
        subcategoryid = request.GET['subcategoryid']
        productid = request.GET['productid']
        finalproductid = request.GET['finalproductid']
        demand_employeeid = request.GET['demand_employeeid']
        qtyissue = request.GET['qtyissue']
        issuedate= request.GET['issuedate']
        remark= request.GET['remark']

        q = "insert into issue(employeeid,categoryid,subcategoryid,productid,finalproductid,demand_employeeid,issuedate,qtyissue,remark)values({},{},{},{},{},{},'{}',{},'{}')".format(employeeid,categoryid,subcategoryid,productid,finalproductid ,demand_employeeid,issuedate,qtyissue,remark)
        print(q)
        db, cmd = Pool.CollectionPool()
        cmd.execute(q)
        # update stock
        q = "update finalproducts set  stock=stock-{} where finalproductid={}".format(qtyissue,finalproductid)
        cmd.execute(q)
        db.commit()
        db.close()

        return render(request, 'IssueInterface.html',{'msg':"Issued Successfully"})

    except Exception as e:
        print("Error:",e)
        return render(
            request,'IssueInterface.html',{'msg':"Failed to Issue"})

def DisplayAllIssue(request):
        try:
          # result = request.session['ADMIN']

           db, cmd = Pool.CollectionPool()
          # q= "select * from issue"
           q = "select PUR.* ,(select C.categoryname from categories C where C.categoryid= PUR.categoryid),(select S.subcategoryname from subcategories S where S.subcategoryid = PUR.subcategoryid),(select P.name from products P where P.productid = PUR.productid),(select FP.finalproductname from finalproducts FP where FP.productid = PUR.productid)   from issue PUR"

           cmd.execute(q)
           rows = cmd.fetchall()
           db.close()
           return render(request, 'DisplayAllIssue.html', {'rows': rows})
        except Exception as e:
            print(e)
            return render(request, 'DisplayAllIssue.html', {'rows': []})





def IssueEditDeleteRecord(request):
    btn = request.GET['btn']
    issueid = request.GET['issueid']

    if (btn == 'Edit'):
        employeeid = request.GET['employeeid']
        categoryid = request.GET['categoryid']
        subcategoryid = request.GET['subcategoryid']
        productid = request.GET['productid']
        finalproductid = request.GET['finalproductid']
        demand_employeeid = request.GET['demand_employeeid']

        qtyissue = request.GET['qtyissue']
        issuedate = request.GET['issuedate']
        remark = request.GET['remark']

        try:

            db, cmd = Pool.CollectionPool()

            q = "update  issue set employeeid={} , categoryid = {} ,subcategoryid={},productid={},finalproductid={},  demand_employeeid={},issuedate='{}',qtyissue={},remark='{}'  where issueid={}".format(employeeid,categoryid, subcategoryid,productid,finalproductid,demand_employeeid,issuedate,qtyissue,remark,issueid)
            print(q)

            cmd.execute(q)
            db.commit()

            db.close()
            return DisplayAllIssue(request)
        except Exception as e:
            print("Error:",e)
            return DisplayAllIssue(request)

    elif (btn == 'Delete'):

        try:
            db, cmd = Pool.CollectionPool()
            q = "delete from issue where issueid={}".format(issueid)
            cmd.execute(q)
            db.commit()

            db.close()
            return DisplayAllIssue(request)

        except Exception as e:
            return DisplayAllIssue(request)




