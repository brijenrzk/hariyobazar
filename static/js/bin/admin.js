
  $(document).ready(function(){
    $('#dropDown').click(function(){
      $('.drop-down').toggleClass('drop-down--active');
    });

    $('.sidenav').sidenav();

    $('select').formSelect();
    $('.modal').modal();
  });

  $('.datepicker').datepicker({
    defaultDate : new Date(2002,01,01),
    maxDate:  new Date(2002,01,31)
  })

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


  (function(window, document, undefined) {

    var factory = function($, DataTable) {
      "use strict";
  
      $('.search-toggle').click(function() {
        if ($('.hiddensearch').css('display') == 'none')
          $('.hiddensearch').slideDown();
        else
          $('.hiddensearch').slideUp();
      });
  
      /* Set the defaults for DataTables initialisation */
      $.extend(true, DataTable.defaults, {
        dom: "<'hiddensearch'f'>" +
          "tr" +
          "<'table-footer'lip'>",
        renderer: 'material'
      });
  
      /* Default class modification */
      $.extend(DataTable.ext.classes, {
        sWrapper: "dataTables_wrapper",
        sFilterInput: "form-control input-sm",
        sLengthSelect: "form-control input-sm"
      });
  
      /* Bootstrap paging button renderer */
      DataTable.ext.renderer.pageButton.material = function(settings, host, idx, buttons, page, pages) {
        var api = new DataTable.Api(settings);
        var classes = settings.oClasses;
        var lang = settings.oLanguage.oPaginate;
        var btnDisplay, btnClass, counter = 0;
  
        var attach = function(container, buttons) {
          var i, ien, node, button;
          var clickHandler = function(e) {
            e.preventDefault();
            if (!$(e.currentTarget).hasClass('disabled')) {
              api.page(e.data.action).draw(false);
            }
          };
  
          for (i = 0, ien = buttons.length; i < ien; i++) {
            button = buttons[i];
  
            if ($.isArray(button)) {
              attach(container, button);
            } else {
              btnDisplay = '';
              btnClass = '';
  
              switch (button) {
  
                case 'first':
                  btnDisplay = lang.sFirst;
                  btnClass = button + (page > 0 ?
                    '' : ' disabled');
                  break;
  
                case 'previous':
                  btnDisplay = '<i class="material-icons">chevron_left</i>';
                  btnClass = button + (page > 0 ?
                    '' : ' disabled');
                  break;
  
                case 'next':
                  btnDisplay = '<i class="material-icons">chevron_right</i>';
                  btnClass = button + (page < pages - 1 ?
                    '' : ' disabled');
                  break;
  
                case 'last':
                  btnDisplay = lang.sLast;
                  btnClass = button + (page < pages - 1 ?
                    '' : ' disabled');
                  break;
  
              }
  
              if (btnDisplay) {
                node = $('<li>', {
                    'class': classes.sPageButton + ' ' + btnClass,
                    'id': idx === 0 && typeof button === 'string' ?
                      settings.sTableId + '_' + button : null
                  })
                  .append($('<a>', {
                      'href': '#',
                      'aria-controls': settings.sTableId,
                      'data-dt-idx': counter,
                      'tabindex': settings.iTabIndex
                    })
                    .html(btnDisplay)
                  )
                  .appendTo(container);
  
                settings.oApi._fnBindAction(
                  node, {
                    action: button
                  }, clickHandler
                );
  
                counter++;
              }
            }
          }
        };
  
        // IE9 throws an 'unknown error' if document.activeElement is used
        // inside an iframe or frame. 
        var activeEl;
  
        try {
          // Because this approach is destroying and recreating the paging
          // elements, focus is lost on the select button which is bad for
          // accessibility. So we want to restore focus once the draw has
          // completed
          activeEl = $(document.activeElement).data('dt-idx');
        } catch (e) {}
  
        attach(
          $(host).empty().html('<ul class="material-pagination"/>').children('ul'),
          buttons
        );
  
        if (activeEl) {
          $(host).find('[data-dt-idx=' + activeEl + ']').focus();
        }
      };
  
      /*
       * TableTools Bootstrap compatibility
       * Required TableTools 2.1+
       */
      if (DataTable.TableTools) {
        // Set the classes that TableTools uses to something suitable for Bootstrap
        $.extend(true, DataTable.TableTools.classes, {
          "container": "DTTT btn-group",
          "buttons": {
            "normal": "btn btn-default",
            "disabled": "disabled"
          },
          "collection": {
            "container": "DTTT_dropdown dropdown-menu",
            "buttons": {
              "normal": "",
              "disabled": "disabled"
            }
          },
          "print": {
            "info": "DTTT_print_info"
          },
          "select": {
            "row": "active"
          }
        });
  
        // Have the collection use a material compatible drop down
        $.extend(true, DataTable.TableTools.DEFAULTS.oTags, {
          "collection": {
            "container": "ul",
            "button": "li",
            "liner": "a"
          }
        });
      }
  
    }; // /factory
  
    // Define as an AMD module if possible
    if (typeof define === 'function' && define.amd) {
      define(['jquery', 'datatables'], factory);
    } else if (typeof exports === 'object') {
      // Node/CommonJS
      factory(require('jquery'), require('datatables'));
    } else if (jQuery) {
      // Otherwise simply initialise as normal, stopping multiple evaluation
      factory(jQuery, jQuery.fn.dataTable);
    }
  
  })(window, document);
  
  $(document).ready(function() {
    $('#datatable').dataTable({
      "oLanguage": {
        "sStripClasses": "",
        "sSearch": "",
        "sSearchPlaceholder": "Enter Keywords Here",
        "sInfo": "_START_ -_END_ of _TOTAL_",
        "sLengthMenu": '<span>Rows per page:</span><select class="browser-default">' +
          '<option value="10">10</option>' +
          '<option value="20">20</option>' +
          '<option value="30">30</option>' +
          '<option value="40">40</option>' +
          '<option value="50">50</option>' +
          '<option value="-1">All</option>' +
          '</select></div>'
      },
      bAutoWidth: false
    });
  });


    // js code for image


  //I added event handler for the file upload control to access the files properties.
document.addEventListener("DOMContentLoaded", init, false);

//To save an array of attachments
var AttachmentArray = [];

//counter for attachment array
var arrCounter = 0;

//to make sure the error message for number of files will be shown only one time.
var filesCounterAlertStatus = false;

//un ordered list to keep attachments thumbnails
var ul = document.createElement("ul");
ul.className = "thumb-Images";
ul.id = "imgList";

function init() {
  //add javascript handlers for the file upload event
  document
    .querySelector("#files")
    .addEventListener("change", handleFileSelect, false);
}

//the handler for file upload event
function handleFileSelect(e) {
  //to make sure the user select file/files
  if (!e.target.files) return;

  //To obtaine a File reference
  var files = e.target.files;

  // Loop through the FileList and then to render image files as thumbnails.
  for (var i = 0, f; (f = files[i]); i++) {
    //instantiate a FileReader object to read its contents into memory
    var fileReader = new FileReader();

    // Closure to capture the file information and apply validation.
    fileReader.onload = (function(readerEvt) {
      return function(e) {
        //Apply the validation rules for attachments upload
        ApplyFileValidationRules(readerEvt);

        //Render attachments thumbnails.
        RenderThumbnail(e, readerEvt);

        //Fill the array of attachment
        FillAttachmentArray(e, readerEvt);
      };
    })(f);

    // Read in the image file as a data URL.
    // readAsDataURL: The result property will contain the file/blob's data encoded as a data URL.
    // More info about Data URI scheme https://en.wikipedia.org/wiki/Data_URI_scheme
    fileReader.readAsDataURL(f);
  }
  document
    .getElementById("id_product_photo")
    .addEventListener("change", handleFileSelect, false);
}

//To remove attachment once user click on x button
jQuery(function($) {
  $("div").on("click", ".img-wrap .close", function() {
    var id = $(this)
      .closest(".img-wrap")
      .find("img")
      .data("id");

    //to remove the deleted item from array
    var elementPos = AttachmentArray.map(function(x) {
      return x.FileName;
    }).indexOf(id);
    if (elementPos !== -1) {
      AttachmentArray.splice(elementPos, 1);
    }

    //to remove image tag
    $(this)
      .parent()
      .find("img")
      .not()
      .remove();

    //to remove div tag that contain the image
    $(this)
      .parent()
      .find("div")
      .not()
      .remove();

    //to remove div tag that contain caption name
    $(this)
      .parent()
      .parent()
      .find("div")
      .not()
      .remove();

    //to remove li tag
    var lis = document.querySelectorAll("#imgList li");
    for (var i = 0; (li = lis[i]); i++) {
      if (li.innerHTML == "") {
        li.parentNode.removeChild(li);
      }
    }
  });
});

//Apply the validation rules for attachments upload
function ApplyFileValidationRules(readerEvt) {
  //To check file type according to upload conditions
  if (CheckFileType(readerEvt.type) == false) {
    alert(
      "The file (" +
        readerEvt.name +
        ") does not match the upload conditions, You can only upload jpg/png/gif files"
    );
    e.preventDefault();
    return;
  }

  //To check file Size according to upload conditions
  if (CheckFileSize(readerEvt.size) == false) {
    alert(
      "The file (" +
        readerEvt.name +
        ") does not match the upload conditions, The maximum file size for uploads should not exceed 300 KB"
    );
    e.preventDefault();
    return;
  }

  //To check files count according to upload conditions
  if (CheckFilesCount(AttachmentArray) == false) {
    if (!filesCounterAlertStatus) {
      filesCounterAlertStatus = true;
      alert(
        "You have added more than 10 files. According to upload conditions you can upload 10 files maximum"
      );
    }
    e.preventDefault();
    return;
  }
}

//To check file type according to upload conditions
function CheckFileType(fileType) {
  if (fileType == "image/jpeg") {
    return true;
  } else if (fileType == "image/png") {
    return true;
  } else if (fileType == "image/gif") {
    return true;
  } else {
    return false;
  }
  return true;
}

//To check file Size according to upload conditions
function CheckFileSize(fileSize) {
  if (fileSize < 3000000) {
    return true;
  } else {
    return false;
  }
  return true;
}

//To check files count according to upload conditions
function CheckFilesCount(AttachmentArray) {
  //Since AttachmentArray.length return the next available index in the array,
  //I have used the loop to get the real length
  var len = 0;
  for (var i = 0; i < AttachmentArray.length; i++) {
    if (AttachmentArray[i] !== undefined) {
      len++;
    }
  }
  //To check the length does not exceed 10 files maximum
  if (len > 3) {
    return false;
  } else {
    return true;
  }
}

//Render attachments thumbnails.
function RenderThumbnail(e, readerEvt) {
  var li = document.createElement("li");
  ul.appendChild(li);
  li.innerHTML = [
    '<div class="img-wrap"> <span class="close">&times;</span>' +
      '<img class="thumb" src="',
    e.target.result,
    '" title="',
    escape(readerEvt.name),
    '" data-id="',
    readerEvt.name,
    '"/>' + "</div>"
  ].join("");

  var div = document.createElement("div");
  div.className = "FileNameCaptionStyle";
  li.appendChild(div);
  div.innerHTML = [readerEvt.name].join("");
  document.getElementById("Filelist").insertBefore(ul, null);
}

//Fill the array of attachment
function FillAttachmentArray(e, readerEvt) {
  AttachmentArray[arrCounter] = {
    AttachmentType: 1,
    ObjectType: 1,
    FileName: readerEvt.name,
    FileDescription: "Attachment",
    NoteText: "",
    MimeType: readerEvt.type,
    Content: e.target.result.split("base64,")[1],
    FileSizeInBytes: readerEvt.size
  };
  arrCounter = arrCounter + 1;
}



  // end for js image