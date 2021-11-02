import os
import random
from django.http import JsonResponse

import uuid
from django.shortcuts import render
from . import Pool

def SubCategoryInterface(request):
    try:
        result=request.session['ADMIN']
        return render(request,'SubCategoryInterface.html',{'result':result})
    except Exception as e:
        return render(request,'AdminInterface.html')

def SubCategoriessubmit(request):
    try:
        categoryid = request.POST['categoryid']
        subcategoryname = request.POST['subcategoryname']
        description = request.POST['description']
        icon = request.FILES['subcategoryicon']
        filename = str(uuid.uuid4()) + icon.name[icon.name.rfind('.'):]
        q = "insert into subcategories(categoryid, subcategoryname, description,icon)values({},'{}','{}','{}')".format(categoryid,subcategoryname ,description,filename)
        db, cmd = Pool.CollectionPool()
        cmd.execute(q)
        db.commit()
        F = open("E:/MM/assets/" + filename, "wb")

        for chunk in icon.chunks():
            F.write(chunk)
        F.close()
        db.close()

        return render(request, 'SubCategoryInterface.html',{'msg':"Record Successfully Submitted"})

    except Exception as e:
        print("Error:",e)
        return render(request, 'SubCategoryInterface.html',{'msg':"Record Not Submitted"})

def DisplayAllSubCategories(request):
        try:
            result = request.session['ADMIN']

            db, cmd = Pool.CollectionPool()
            q = "select * from subcategories "
            cmd.execute(q)
            rows = cmd.fetchall()
            db.close()
            return render(request, 'DisplayAllSubCategories.html', {'rows': rows,'result':result})
        except Exception as e:
            print(e)
            return render(request, 'AdminInterface.html', {'rows': []})

def DisplayById(request):
    subcategoryid = request.GET['subcategoryid']
    try:
        db, cmd = Pool.CollectionPool()
        q = "select S.*,(select C.categoryname from categories C where C.categoryid=S.categoryid)  from subcategories S where subcategoryid={} ".format(subcategoryid)
        print(q)

        cmd.execute(q)
        row = cmd.fetchone()
        db.close()
        return render(request, 'DisplaySubCategoryById.html', {'row': row})
    except Exception as e:
        return render(request, 'DisplaySubCategoryById.html', {'row': []})


def SubCategoryEditDeleteRecord(request):
        btn = request.GET['btn']
        subcategoryid = request.GET['subcategoryid']
        if (btn == 'Edit'):
            categoryid = request.GET['categoryid']
            subcategoryname = request.GET['subcategoryname']
            description = request.GET['description']

            try:

                db, cmd = Pool.CollectionPool()
                q = "update  subcategories set categoryid={}, subcategoryname = '{}',description='{}' where subcategoryid={}".format(categoryid,subcategoryname,description, subcategoryid)

                cmd.execute(q)
                db.commit()

                db.close()
                return DisplayAllSubCategories(request)
            except Exception as e:
                print("Hello...")
                return DisplayAllSubCategories(request)

        elif (btn == 'Delete'):

            try:
                db, cmd = Pool.CollectionPool()
                q = "delete from subcategories where subcategoryid={}".format(subcategoryid)
                cmd.execute(q)
                db.commit()

                db.close()
                return DisplayAllSubCategories(request)

            except Exception as e:
                return DisplayAllSubCategories(request)


def EditSubCategoryPicture(request):
    try:
        subcategoryid = request.GET['subcategoryid']
        subcategoryname = request.GET['subcategoryname']
        picture = request.GET['picture']
        row = [subcategoryid,subcategoryname,picture]
        return render(request, 'EditSubCategoryPicture.html', {'row': row})
    except Exception as e:
        return render(request, 'EditSubCategoryPicture.html', {'row': row})

def SubCategorySaveEditPicture(request):
    try:
        subcategoryid=request.POST['subcategoryid']
        oldpicture=request.POST['oldpicture']
        picture = request.FILES['picture']
        filename = str(uuid.uuid4())+picture.name[picture.name.rfind('.'):]
        q = "update subcategories set icon='{}' where subcategoryid={} ".format(filename,subcategoryid)
        db,cmd = Pool.CollectionPool()
        cmd.execute(q)
        db.commit()
        F = open("E:/MM/assets/"+filename,"wb")

        for chunk in picture.chunks():
            F.write(chunk)
        F.close()
        db.close()
        os.remove('E:/MM/assets/'+oldpicture)
        return DisplayAllSubCategories(request)
    except Exception as e:
        print(e)
        return DisplayAllSubCategories(request)

def GetCategoriesJSON(request):
        try:
            db, cmd = Pool.CollectionPool()
            q = "select * from categories "
            cmd.execute(q)
            rows = cmd.fetchall()
            db.close()
            return JsonResponse(rows, safe=False)

        except Exception as e:
            return JsonResponse([], safe=False)


def GetSubCategoriesJSON(request):
    try:
        db, cmd = Pool.CollectionPool()
        categoryid = request.GET['categoryid']
        q = "select * from subcategories where categoryid={}".format(categoryid)
        print(q)
        cmd.execute(q)
        rows = cmd.fetchall()
        db.close()
        return JsonResponse(rows, safe=False)

    except Exception as e:
        return JsonResponse([], safe=False)