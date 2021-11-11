"""MM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.views.static import serve
from django.conf.urls import url
from . import EmployeeView,StateCityView,CategoryView,SubCategoryView,ProductView,FinalProductView,PurchaseView,SupplierView,AdminView,IssueView

urlpatterns = [
    path('admin/', admin.site.urls),

    #Employee
    path('employeelogin/', EmployeeView.EmployeeLogin),
    path('checkemployeelogin', EmployeeView.CheckEmployeeLogin),
    path('employeedashboard', EmployeeView.EmployeeDashboard),
    path('employeeinterface/',EmployeeView.EmployeeInterface),
    #security required
    path('employeesubmit', EmployeeView.EmployeeSubmit),

    path('displayall/',EmployeeView.DisplayAllEmployee),
    path('displayemployeebyid/',EmployeeView.DisplayById),
    path('editdeleterecord/',EmployeeView.EditDeleteRecord),
    path('editemployeepicture/',EmployeeView.EditEmployeePicture),
    path('saveeditpicture',EmployeeView.SaveEditPicture),
    path('updateprofilepicture',EmployeeView.UpdateProfilePicture),
    path('employeelogin/',EmployeeView.EmployeeLogin),
    path('employeelogout/',EmployeeView.EmployeeLogout),
    #sercurity required
    path('getemployeejson',EmployeeView.GetEmployeeJSON),

  #Category
    path('categoryinterface/',CategoryView.CategoryInterface),
    #security required
    path('categoriessubmit',CategoryView.Categoriessubmit),

    path('displayallcategories/', CategoryView.DisplayAllCategories),
    path('displaycategorybyid/', CategoryView.DisplayById),
    path('categoryeditdeleterecord/',CategoryView.CategoryEditDeleteRecord),
    path('editcategorypicture/',CategoryView.EditCategoryPicture),
    path('categorysaveeditpicture',CategoryView.CategorySaveEditPicture),
    #security required
    path('getcategoriesjson',CategoryView.GetCategorieJSON),

    # Sub Category
     path('subcategoryinterface/', SubCategoryView.SubCategoryInterface),
     path('subcategoriessubmit', SubCategoryView.SubCategoriessubmit),
     path('displayallsubcategories/', SubCategoryView.DisplayAllSubCategories),
     path('displaysubcategorybyid/', SubCategoryView.DisplayById),
     path('subcategoryeditdeleterecord/',SubCategoryView.SubCategoryEditDeleteRecord),
     path('editsubcategorypicture/',SubCategoryView.EditSubCategoryPicture),
     path('subcategorysaveeditpicture',SubCategoryView.SubCategorySaveEditPicture),
     path('getcategoriesjson',SubCategoryView.GetCategoriesJSON),
     path('getsubcategoriesjson',SubCategoryView.GetSubCategoriesJSON),

  #products
        path('productinterface/', ProductView.ProductInterface),
        path('productsubmit', ProductView.Productsubmit),
        path('displayallproducts/', ProductView.DisplayAllProducts),
        path('displayallproductsforemployee/', ProductView.DisplayAllProductsForEmployee),
        path('displayproductbyid/', ProductView.DisplayById),
        path('producteditdeleterecord/',ProductView.ProductEditDeleteRecord),
        path('editproductpicture/',ProductView.EditProductPicture),
        path('productsaveeditpicture',ProductView.ProductSaveEditPicture),
        path('getproductjson', ProductView.GetProductJSON),

    #final products
        path('finalproductinterface/', FinalProductView.FinalProductInterface),
        path('finalproductsubmit', FinalProductView.FinalProductsubmit),
        path('displayallfinalproducts/', FinalProductView.DisplayAllFinalProducts),
        path('displayallfinalproductsforemployee/', FinalProductView.DisplayAllFinalProductsForEmployee),
        path('finalproducteditdeleterecord/',FinalProductView.FinalProductEditDeleteRecord),
        path('finalproductsaveeditpicture',FinalProductView.FinalProductSaveEditPicture),
        path('getfinalproductjson/', FinalProductView.GetFinalProductJSON),
        path('displayfinalproductbyidjson/', FinalProductView.DisplayFinalProductByIdJSON),
        path('displayfinalproductalljson/', FinalProductView.DisplayFinalProductAllJSON),
        path('displayupdatedstock/', FinalProductView.DisplayUpdatedStock),

  #Fetching
    path('fetchallstates/',StateCityView.FetchAllStates),
    path('fetchallcities/', StateCityView.FetchAllCities),

    #Purchaseing
    path('purchaseinterface/', PurchaseView.PurchaseInterface),
    path('purchasesubmit/', PurchaseView.Purchasesubmit),
    path('displayallpurchase/', PurchaseView.DisplayAllPurchase),
    path('purchaseeditdeleterecord/', PurchaseView.PurchaseEditDeleteRecord),

    #supplier
    path('supplierinterface/', SupplierView.SupplierInterface),
    path('suppliersubmit/', SupplierView.Suppliersubmit),
    path('displayallsupplier/', SupplierView.DisplayAllSupplier),
    path('suppliereditdeleterecord/', SupplierView.SupplierEditDeleteRecord),
    path('getsupplierjson',SupplierView.GetSupplierJSON),

    #Admin
    path('admininterface/', AdminView.AdminInterface),
    path('adminlogout/', AdminView.AdminLogout),
    path('checkadminlogin', AdminView.CheckAdminLogin),
    path('admindashboard/', AdminView.AdminDashboard),
    path('adminupdateprofilepicture', AdminView.AdminUpdateProfilePicture),

    #Issue
    path('issueinterface/', IssueView.IssueInterface),
    path('issuesubmit/', IssueView.Issuesubmit),
    path('displayallissue/', IssueView.DisplayAllIssue),
    path('issueeditdeleterecord/', IssueView.IssueEditDeleteRecord),

]
