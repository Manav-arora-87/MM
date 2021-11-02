$(document).ready(function(){
var d=new Date()
var cd=(d.getFullYear())+"-"+(d.getMonth()+1)+"-"+(d.getDate())
$('#issuedate').val(cd)
$('#purchasedate').val(cd)


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
$('#productid').change(function(){

$.getJSON("/getfinalproductjson",{ajax:true,categoryid:$('#categoryid').val(),subcategoryid:$('#subcategoryid').val(),productid:$('#productid').val() },function(data){

   $('#finalproductid').empty()
   $('#finalproductid').append($('<option>').text('-Select Final Product-'))
   $.each(data,function(index,item){
   $('#finalproductid').append($('<option>').text(item[4]).val(item[3]))

   })
})




})



$.getJSON("/getsupplierjson",{ajax:true},function(data){
   $.each(data,function(index,item){
   $('#supplierid').append($('<option>').text(item[1]).val(item[0]))

   })
})

$.getJSON("/getemployeejson",{ajax:true},function(data){
   $.each(data,function(index,item){
   $('#demand_employeeid').append($('<option>').text(item[1]+" "+item[2]).val(item[0]))

   })
})




$('#finalproductid').change(function(){

$.getJSON("/displayfinalproductbyidjson",{ajax:true,finalproductid:$('#finalproductid').val()},function(data){

   $('#currentstock').html(data.stock)

})

$('#qtyissue').keyup(function(){

if(parseInt($('#currentstock').html())>=parseInt($('#qtyissue').val()))
{

$('#btnsubmit').attr('disabled',false)
}
else
{

$('#btnsubmit').attr('disabled',true)

}

})


})




})


