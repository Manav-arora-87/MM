import random
from django.http import JsonResponse
import os
import uuid
from django.shortcuts import render
from . import Pool,PoolDict

def FinalProductInterface(request):
    try:
        result=request.session['ADMIN']
        return render(request,'FinalProductInterface.html',{'result':result})
    except Exception as e:
        return render(request,'AdminInterface.html')

def DisplayFinalProductByIdJSON(request):
        finalproductid=request.GET['finalproductid']
        try:


            db, cmd = PoolDict.CollectionPool()
            q = "select FP.*,(select C.categoryname from categories C where C.categoryid= FP.categoryid),(select S.subcategoryname from subcategories S where S.subcategoryid = FP.subcategoryid),(select P.name from products P where P.productid = FP.productid)   from finalproducts FP where finalproductid={}".format(finalproductid)
            cmd.execute(q)
            row = cmd.fetchone()
            db.close()
            return JsonResponse(row, safe=False)

        except Exception as e:
            print(e)
            return JsonResponse([], safe=False)

def DisplayUpdatedStock(request):
    return render(request, 'ListFinalProductsEmployee.html')


def DisplayFinalProductAllJSON(request):
    pattern = request.GET['pattern']
    try:

        db, cmd = PoolDict.CollectionPool()
        q = "select FP.*,(select C.categoryname from categories C where C.categoryid= FP.categoryid),(select S.subcategoryname from subcategories S where S.subcategoryid = FP.subcategoryid),(select P.name from products P where P.productid = FP.productid)   from finalproducts FP where finalproductname like '%{}%' ".format(pattern)
        cmd.execute(q)
        rows = cmd.fetchall()
        db.close()
        return JsonResponse(rows, safe=False)

    except Exception as e:
        print(e)
        return JsonResponse([], safe=False)


def FinalProductsubmit(request):
    try:
        categoryid = request.POST['categoryid']
        subcategoryid = request.POST['subcategoryid']
        productid = request.POST['productid']
        finalproductname = request.POST['finalproductname']
        size = request.POST['size']
        sizeunit = request.POST['sizeunit']
        weight = request.POST['weight']
        weightunit = request.POST['weightunit']
        price = request.POST['price']
        color = request.POST['color']
        stock = request.POST['stock']
        icon = request.FILES['finalpicture']
        filename = str(uuid.uuid4()) + icon.name[icon.name.rfind('.'):]
        q = "insert into finalproducts(categoryid,subcategoryid,productid,finalproductname,size,sizeunit,weight,weightunit,color,price,stock,picture)values({},{},{},'{}','{}','{}','{}','{}','{}',{},{},'{}')".format(categoryid,subcategoryid,productid,finalproductname ,size,sizeunit,weight,weightunit,color,price,stock,filename)
        db, cmd = Pool.CollectionPool()
        cmd.execute(q)
        db.commit()
        F = open("E:/MM/assets/" + filename, "wb")

        for chunk in icon.chunks():
            F.write(chunk)
        F.close()
        db.close()

        return render(request, 'FinalProductInterface.html',{'msg':"Record Successfully Submitted"})

    except Exception as e:
        print("Error:",e)
        return render(request,'FinalProductInterface.html',{'msg':"Record Not Submitted"})

def DisplayAllFinalProducts(request):
        try:
           result = request.session['ADMIN']

           db, cmd = Pool.CollectionPool()
           q = "select FP.*,(select C.categoryname from categories C where C.categoryid= FP.categoryid),(select S.subcategoryname from subcategories S where S.subcategoryid = FP.subcategoryid),(select P.name from products P where P.productid = FP.productid)   from finalproducts FP"
           cmd.execute(q)
           rows = cmd.fetchall()
           db.close()
           return render(request, 'DisplayAllFinalProducts.html', {'rows': rows,'result':result})
        except Exception as e:
            print(e)
            return render(request, 'AdminInterface.html', {'rows': []})

def DisplayAllFinalProductsForEmployee(request):
        try:
           result = request.session['EMPLOYEE']

           db, cmd = Pool.CollectionPool()
           q = "select FP.*,(select C.categoryname from categories C where C.categoryid= FP.categoryid),(select S.subcategoryname from subcategories S where S.subcategoryid = FP.subcategoryid),(select P.name from products P where P.productid = FP.productid)   from finalproducts FP"
           cmd.execute(q)
           rows = cmd.fetchall()
           db.close()
           return render(request, 'DisplayAllFinalProductsForEmployee.html', {'rows': rows,'result':result})
        except Exception as e:
            print(e)
            return render(request, 'EmployeeLogin.html', {'rows': []})




def FinalProductEditDeleteRecord(request):
    btn = request.GET['btn']
    finalproductid = request.GET['finalproductid']
    print(finalproductid)
    if (btn == 'Edit'):
        categoryid = request.GET['categoryid']
        subcategoryid = request.GET['subcategoryid']
        productid = request.GET['productid']
        finalproductname = request.GET['finalproductname']
        color = request.GET['color']
        size = request.GET['size']
        sizeunit = request.GET['sizeunit']
        weight = request.GET['weight']
        weightunit = request.GET['weightunit']
        price = request.GET['price']
        stock = request.GET['stock']


        try:

            db, cmd = Pool.CollectionPool()

            q = "update  finalproducts set categoryid = {} ,subcategoryid={},productid={},finalproductname='{}',size='{}',sizeunit='{}',weight='{}',weightunit='{}',color='{}', price={},stock={}    where finalproductid={}".format(categoryid, subcategoryid,productid,finalproductname,size,sizeunit,weight,weightunit,color,price,stock,finalproductid)
            print(q)
            print(finalproductid)
            cmd.execute(q)
            db.commit()

            db.close()
            return DisplayAllFinalProducts(request)
        except Exception as e:
            print("Error:",e)
            return DisplayAllFinalProducts(request)

    elif (btn == 'Delete'):

        try:
            db, cmd = Pool.CollectionPool()
            q = "delete from finalproducts where finalproductid={}".format(finalproductid)
            cmd.execute(q)
            db.commit()

            db.close()
            return DisplayAllFinalProducts(request)

        except Exception as e:
            return DisplayAllFinalProducts(request)

def FinalProductSaveEditPicture(request):
    try:
        finalproduct=request.POST['finalproduct']
        oldpicture=request.POST['oldpicture']
        picture = request.FILES['picture']
        filename = str(uuid.uuid4())+picture.name[picture.name.rfind('.'):]
        q = "update finalproducts set picture='{}' where finalproductid={} ".format(filename,finalproduct)
        db,cmd = Pool.CollectionPool()
        cmd.execute(q)
        db.commit()
        F = open("E:/MM/assets/"+filename,"wb")

        for chunk in picture.chunks():
            F.write(chunk)
        F.close()
        db.close()
        os.remove('E:/MM/assets/'+oldpicture)
        return DisplayAllFinalProducts(request)
    except Exception as e:
        print(e)
        return DisplayAllFinalProducts(request)


def GetFinalProductJSON(request):
    try:
        db, cmd = Pool.CollectionPool()
        categoryid = request.GET['categoryid']
        subcategoryid = request.GET['subcategoryid']
        productid = request.GET['productid']

        q = "select * from finalproducts where categoryid={} and subcategoryid={} and productid={}".format(categoryid,subcategoryid,productid)
        print(q)
        cmd.execute(q)
        rows = cmd.fetchall()
        db.close()
        return JsonResponse(rows, safe=False)

    except Exception as e:
        return JsonResponse([], safe=False)

