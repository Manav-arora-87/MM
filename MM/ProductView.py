from django.http import JsonResponse
import os
import uuid
from django.shortcuts import render
from . import Pool

def ProductInterface(request):
    try:
        result=request.session['ADMIN']
        return render(request,'ProductInterface.html',{'result':result})
    except Exception as e:
        return render(request,'AdminInterface.html')

def Productsubmit(request):
    try:
        categoryid = request.POST['categoryid']
        subcategoryid = request.POST['subcategoryid']
        productname = request.POST['productname']
        description = request.POST['description']
        gst = request.POST['gst']
        icon = request.FILES['productpicture']
        filename = str(uuid.uuid4()) + icon.name[icon.name.rfind('.'):]
        q = "insert into products(categoryid,subcategoryid,name, description,gst,picture)values({},{},'{}','{}','{}','{}')".format(categoryid,subcategoryid,productname ,description,gst,filename)
        db, cmd = Pool.CollectionPool()
        cmd.execute(q)
        db.commit()
        F = open("E:/MM/assets/" + filename, "wb")

        for chunk in icon.chunks():
            F.write(chunk)
        F.close()
        db.close()

        return render(request, 'ProductInterface.html',{'msg':"Record Successfully Submitted"})

    except Exception as e:
        print("Error:",e)
        return render(request,'ProductInterface.html',{'msg':"Record Not Submitted"})

def DisplayAllProducts(request):
        try:
            result = request.session['ADMIN']

            db, cmd = Pool.CollectionPool()
            q = "select * from products "
            cmd.execute(q)
            rows = cmd.fetchall()
            db.close()
            return render(request, 'DisplayAllProducts.html', {'rows': rows,'result':result})
        except Exception as e:
            print(e)
            return render(request, 'AdminInterface.html', {'rows': []})

def DisplayAllProductsForEmployee(request):
        try:
            result = request.session['EMPLOYEE']

            db, cmd = Pool.CollectionPool()
            q = "select * from products "
            cmd.execute(q)
            rows = cmd.fetchall()
            db.close()
            return render(request, 'DisplayAllProductsForEmployee.html', {'rows': rows,'result':result})
        except Exception as e:
            print(e)
            return render(request, 'EmployeeLogin.html', {'rows': []})


def DisplayById(request):
    productid = request.GET['productid']
    try:
        db, cmd = Pool.CollectionPool()
        q = "select P.*,(select C.categoryname from categories C where C.categoryid= P.categoryid),(select S.subcategoryname from subcategories S where S.subcategoryid = P.subcategoryid)   from products P where productid={} ".format(productid)
        print(q)
        cmd.execute(q)
        row = cmd.fetchone()
        db.close()
        return render(request, 'DisplayProductById.html', {'row': row})
    except Exception as e:
        return render(request, 'DisplayProductById.html', {'row': []})


def ProductEditDeleteRecord(request):
    btn = request.GET['btn']
    productid = request.GET['productid']
    if (btn == 'Edit'):
        categoryid = request.GET['categoryid']
        subcategoryid = request.GET['subcategoryid']
        name = request.GET['productname']
        description = request.GET['description']
        gst = request.GET['gst']

        try:

            db, cmd = Pool.CollectionPool()
            q = "update  products set categoryid = {} ,subcategoryid={}, name='{}',description='{}',gst={}    where productid={}".format(categoryid, subcategoryid,name,description,gst,productid)
            print(q)
            cmd.execute(q)
            db.commit()

            db.close()
            return DisplayAllProducts(request)
        except Exception as e:

            return DisplayAllProducts(request)

    elif (btn == 'Delete'):

        try:
            db, cmd = Pool.CollectionPool()
            q = "delete from products where productid={}".format(productid)
            cmd.execute(q)
            db.commit()

            db.close()
            return DisplayAllProducts(request)

        except Exception as e:
            return DisplayAllProducts(request)

def EditProductPicture(request):
    try:
        productid = request.GET['productid']
        productname = request.GET['productname']
        picture = request.GET['picture']
        row = [productid,productname,picture]
        return render(request, 'EditProductPicture.html', {'row': row})
    except Exception as e:
        return render(request, 'EditProductPicture.html', {'row': row})

def ProductSaveEditPicture(request):
    try:
        productid=request.POST['productid']
        oldpicture=request.POST['oldpicture']
        picture = request.FILES['picture']
        filename = str(uuid.uuid4())+picture.name[picture.name.rfind('.'):]
        q = "update products set picture='{}' where productid={} ".format(filename,productid)
        db,cmd = Pool.CollectionPool()
        cmd.execute(q)
        db.commit()
        F = open("E:/MM/assets/"+filename,"wb")

        for chunk in picture.chunks():
            F.write(chunk)
        F.close()
        db.close()
        os.remove('E:/MM/assets/'+oldpicture)
        return DisplayAllProducts(request)
    except Exception as e:
        print(e)
        return DisplayAllProducts(request)

def GetProductJSON(request):
    try:
        db, cmd = Pool.CollectionPool()
        categoryid = request.GET['categoryid']
        subcategoryid = request.GET['subcategoryid']

        q = "select * from products where categoryid={} and subcategoryid={}".format(categoryid,subcategoryid)
        print(q)
        cmd.execute(q)
        rows = cmd.fetchall()
        db.close()
        return JsonResponse(rows, safe=False)

    except Exception as e:
        return JsonResponse([], safe=False)
