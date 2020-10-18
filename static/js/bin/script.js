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
  $('.datepicker').datepicker();
  $('select').formSelect();
  });
