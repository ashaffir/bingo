$(document).ready(function(){
    $("#payment").validate({
       rules: {
        userName: {
          required: true,
          minlength: 3,
          maxlength: 50,
        },
       
        card_number: {
          required : true,
          minlength: 16,
          maxlength: 18
          // email :true,
        },
        exp_month : {
          required : true,
          // maxlength : 50
        },
        exp_year : {
          required : true,
          // maxlength : 50
        },
        cvv : {
          required : true,
          minlength : 3,
          maxlength : 4
        }
      },
      messages: {
         name:{
            required: "Please enter your name",
            minlength: "Name should be at least 3 characters",
            maxlength: "Name should be less than 50 characters"
         },
         card_number: {
            required : "Please enter your card-number",
            minlength: "Invalid",
            maxlength: "Invalid"
         },
        exp_month : {
          required : "Missing",
          // minlength: "subject should be at least 4 characters",
          // maxlength: "subject should be less than 5 characters"
        },
        exp_year : {
          required : "Missing",
          // minlength: "subject should be at least 4 characters",
          // maxlength: "subject should be less than 5 characters"
        },
        cvv : {
          required : "Missing cvv",
          minlength: "cvv should be at least 3 characters",
          maxlength: "cvv should be less than 4 characters"
        }
       }
     });


});
