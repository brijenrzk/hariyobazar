$(document).ready(function(){
    $('#dropDown').click(function(){
      $('.drop-down').toggleClass('drop-down--active');
    });
    // $(document).on("click", function(event){
    //   var $trigger = $(".drop-down");
    //   if($trigger !== event.target && !$trigger.has(event.target).length && $('.drop-down').on()){
    //     $('.drop-down').toggle();
    //   }            
  // });

  $('.carousel.carousel-slider').carousel({
    fullWidth: true

});
autoplay();
function autoplay() {
    $('.carousel').carousel('next');
    setTimeout(autoplay, 4500);
}

  $('select').formSelect();
  });

  $('.datepicker').datepicker({
    defaultDate : new Date(2002,01,01),
    maxDate:  new Date(2002,01,31)
  })
    

   function Toggle() { 
    var temp = document.getElementById("typepass"); 
    var switchEye = document.getElementById("eye"); 
    if (temp.type === "password") { 
        temp.type = "text"; 
        {switchEye.innerHTML = 'visibility_off';}
    } 
    else { 
        temp.type = "password"; 
        {switchEye.innerHTML = 'visibility';}
    } 
} 

function Toggle2() { 
  var temp = document.getElementById("id_password1"); 
  var switchEye = document.getElementById("eye2"); 
  if (temp.type === "password") { 
      temp.type = "text"; 
      {switchEye.innerHTML = 'visibility_off';}
  } 
  else { 
      temp.type = "password"; 
      {switchEye.innerHTML = 'visibility';}
  } 
} 

function Toggle3() { 
  var temp = document.getElementById("id_password2"); 
  var switchEye = document.getElementById("eye3"); 
  if (temp.type === "password") { 
      temp.type = "text"; 
      {switchEye.innerHTML = 'visibility_off';}
  } 
  else { 
      temp.type = "password"; 
      {switchEye.innerHTML = 'visibility';}
  } 
} 
function Toggle4() { 
  var temp = document.getElementById("id_old_password"); 
  var switchEye = document.getElementById("eye"); 
  if (temp.type === "password") { 
      temp.type = "text"; 
      {switchEye.innerHTML = 'visibility_off';}
  } 
  else { 
      temp.type = "password"; 
      {switchEye.innerHTML = 'visibility';}
  } 
}
function Toggle5() { 
  var temp = document.getElementById("id_new_password1"); 
  var switchEye = document.getElementById("eye2"); 
  if (temp.type === "password") { 
      temp.type = "text"; 
      {switchEye.innerHTML = 'visibility_off';}
  } 
  else { 
      temp.type = "password"; 
      {switchEye.innerHTML = 'visibility';}
  } 
}
function Toggle6() { 
  var temp = document.getElementById("id_new_password2"); 
  var switchEye = document.getElementById("eye3"); 
  if (temp.type === "password") { 
      temp.type = "text"; 
      {switchEye.innerHTML = 'visibility_off';}
  } 
  else { 
      temp.type = "password"; 
      {switchEye.innerHTML = 'visibility';}
  } 
}
$(function() {

  $(".form__password-active").focusin(function() {
      $(".form__password_warning").show();
  }).focusout(function () {
      $(".form__password_warning").hide();
  });
});

//drop down

const $drowdownArrow = document.querySelector('.rot');
const $checkbox = document.getElementById('openDropdown');
const $dropdownMenu = document.querySelector('.dropdown-menu');

$checkbox.addEventListener('change', () => {
  $drowdownArrow.classList.toggle('rotate-dropdown-arrow');
});

$dropdownMenu.addEventListener('click', (e) => {
  $checkbox.checked = false;
  // setting checked to false won't trigger 'change'
  // event, manually dispatch an event to rotate
  // dropdown arrow icon
  $checkbox.dispatchEvent(new Event('change'));
});


//end of dropdown