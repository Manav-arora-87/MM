$(document).ready(function(){

$.getJSON("/fetchallstates",{ajax:true},function(data){
   $.each(data,function(index,item){
   /*$('#state').empty()*/
   $('#state').append($('<option>').text(item[1]).val(item[0]))

   })
})
$('#state').change(function(){

$.getJSON("/fetchallcities",{ajax:true,stateid:$('#state').val()},function(data){
   $('#city').empty()
   $('#city').append($('<option>').text('-City-'))
   $.each(data,function(index,item){
   $('#city').append($('<option>').text(item[2]).val(item[1]))

   })
})

})

    $('#picture').change(function(){
    /*alert(picture.files[0])*/
    var file = picture.files[0]
    pic.src = URL.createObjectURL(file)

    })

    $('#categoryicon').change(function(){
    /*alert(categoryicon.files[0])*/
    var file = categoryicon.files[0]
    categoryiconpic.src = URL.createObjectURL(file)

    })

    $('#subcategoryicon').change(function(){
    /*alert(subcategoryicon.files[0])*/
    var file = subcategoryicon.files[0]
    subcategoryiconpic.src = URL.createObjectURL(file)

    })


    $('#productpicture').change(function(){

    var file = productpicture.files[0]
    productpic.src = URL.createObjectURL(file)

    })


    $('#finalpicture').change(function(){
    /*alert(finalpicture.files[0])*/
    var file = finalpicture.files[0]
    productpic.src = URL.createObjectURL(file)

    })


})