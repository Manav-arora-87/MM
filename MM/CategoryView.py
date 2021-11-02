from django.http import JsonResponse
import random
import uuid
import os
from django.shortcuts import render
from . import Pool

def CategoryInterface(request):
    try:
        result=request.session['ADMIN']
        return render(request,'CategoryInterface.html',{'result':result})
    except Exception as e:
        return render(request,'AdminInterface.html')

def Categoriessubmit(request):
    try:

        categoryname = request.POST['categoryname']
        icon = request.FILES['categoryicon']
        filename = str(uuid.uuid4()) + icon.name[icon.name.rfind('.'):]
        q = "insert into categories(categoryname, icon)values('{}','{}')".format(categoryname ,filename)
        db, cmd = Pool.CollectionPool()
        cmd.execute(q)
        db.commit()
        F = open("E:/MM/assets/" + filename, "wb")

        for chunk in icon.chunks():
            F.write(chunk)
        F.close()
        db.close()

        return render(request, 'CategoryInterface.html',{'msg':"Record Successfully Submitted"})

    except Exception as e:
        print(e)
        return render(request, 'CategoryInterface.html',{'msg':"Record Not Submitted"})

def DisplayAllCategories(request):
        try:
            result = request.session['ADMIN']

            db, cmd = Pool.CollectionPool()
            q = "select * from categories "
            cmd.execute(q)
            rows = cmd.fetchall()
            db.close()
            return render(request, 'DisplayAllCategories.html',{'result':result,'rows':rows})
        except Exception as e:
            return render(request, 'AdminInterface.html', {'rows': []})


def DisplayById(request):
    categoryid = request.GET['categoryid']
    try:
        db, cmd = Pool.CollectionPool()
        q = "select *  from categories where categoryid={} ".format(categoryid)
        cmd.execute(q)
        row = cmd.fetchone()
        db.close()
        return render(request, 'DisplayCategoryId.html', {'row': row})
    except Exception as e:
        return render(request, 'DisplayCategoryId.html', {'row': []})


def CategoryEditDeleteRecord(request):
        btn = request.GET['btn']
        categoryid = request.GET['categoryid']
        if (btn == 'Edit'):
            categoryname = request.GET['categoryname']

            try:

                db, cmd = Pool.CollectionPool()
                q = "update  categories set categoryname = '{}' where categoryid={}".format(categoryname, categoryid)
                print(q)
                cmd.execute(q)
                db.commit()

                db.close()
                return DisplayAllCategories(request)
            except Exception as e:

                return DisplayAllCategories(request)

        elif (btn == 'Delete'):

            try:
                db, cmd = Pool.CollectionPool()
                q = "delete from categories where categoryid={}".format(categoryid)
                cmd.execute(q)
                db.commit()

                db.close()
                return DisplayAllCategories(request)

            except Exception as e:
                return DisplayAllCategories(request)

def EditCategoryPicture(request):
    try:
        categoryid = request.GET['categoryid']
        categoryname = request.GET['categoryname']
        picture = request.GET['picture']
        row = [categoryid,categoryname,picture]
        return render(request, 'EditCategoryPicture.html', {'row': row})
    except Exception as e:
        return render(request, 'EditCategoryPicture.html', {'row': row})

def CategorySaveEditPicture(request):
    try:
        categoryid=request.POST['categoryid']
        oldpicture=request.POST['oldpicture']
        picture = request.FILES['picture']
        filename = str(uuid.uuid4())+picture.name[picture.name.rfind('.'):]
        q = "update categories set icon='{}' where categoryid={} ".format(filename,categoryid)
        db,cmd = Pool.CollectionPool()
        cmd.execute(q)
        db.commit()
        F = open("E:/MM/assets/"+filename,"wb")

        for chunk in picture.chunks():
            F.write(chunk)
        F.close()
        db.close()
        os.remove('E:/MM/assets/'+oldpicture)
        return DisplayAllCategories(request)
    except Exception as e:
        print(e)
        return DisplayAllCategories(request)

def GetCategorieJSON(request):
        try:
            db, cmd = Pool.CollectionPool()
            q = "select * from categories "
            cmd.execute(q)
            rows = cmd.fetchall()
            db.close()
            return JsonResponse(rows,safe=False)

        except Exception as e:
            return JsonResponse([],safe=False)