
$(document).ready(function(){

$('#pattern').keyup(function(){

$.getJSON("/displayfinalproductalljson",{pattern:$('#pattern').val()},function(data){

   var htm="<table class='table'><thead><tr><th >Id</th><th >Product Name</th><th>Stock</th><th>Price</th><th>Update</th></tr></thead><tbody>"
 /* var htm="<table class='table'><thead><tr><th>Id</th><th>Product Name</th><th>Stock</th><th>Price</th></tr></thead>"
*/

   $.each(data,function(index,item){

   htm+="<tr><td>"+item.finalproductid+"</td><td>"+item.finalproductname+"</td><td>"+item.stock+"</td><td>"+item.price+"</td></tr>"
   })

   htm+="</tbody></table>"
   /*htm+="</table>"*/
   $('#result').html(htm)
})

})
})


