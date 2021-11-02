$(document).ready(function(){


$.getJSON("/getcategoriesjson",{ajax:true},function(data){
   $.each(data,function(index,item){
   $('#categoryid').append($('<option>').text(item[1]).val(item[0]))

   })
})



$('#categoryid').change(function(){

$.getJSON("/getsubcategoriesjson",{ajax:true,categoryid:$('#categoryid').val()},function(data){
   $('#subcategoryid').empty()
   $('#subcategoryid').append($('<option>').text('-Select Sub-Category-'))
   $.each(data,function(index,item){
   $('#subcategoryid').append($('<option>').text(item[2]).val(item[1]))

   })
})

})
$('#subcategoryid').change(function(){

$.getJSON("/getproductjson",{ajax:true,categoryid:$('#categoryid').val(),subcategoryid:$('#subcategoryid').val() },function(data){

   $('#productid').empty()
   $('#productid').append($('<option>').text('-Select Product-'))
   $.each(data,function(index,item){
   $('#productid').append($('<option>').text(item[3]).val(item[2]))

   })
})

})





})


