$(function () {


    /* ===============================================================
         LIGHTBOX
      =============================================================== */
    lightbox.option({
        'resizeDuration': 200,
        'wrapAround': true
    });


    /* ===============================================================
         PRODUCT SLIDER
      =============================================================== */
    $('.product-slider').owlCarousel({
        items: 1,
        thumbs: true,
        thumbImage: false,
        thumbsPrerendered: true,
        thumbContainerClass: 'owl-thumbs',
        thumbItemClass: 'owl-thumb-item'
    });


    /* ===============================================================
         PRODUCT QUNATITY
      =============================================================== */
      $('.dec-btn').click(function () {
          var siblings = $(this).siblings('input');
          if (parseInt(siblings.val(), 10) >= 1) {
              siblings.val(parseInt(siblings.val(), 10) - 1);
          }
      });

      $('.inc-btn').click(function () {
          var siblings = $(this).siblings('input');
          siblings.val(parseInt(siblings.val(), 10) + 1);
      });


      /* ===============================================================
           BOOTSTRAP SELECT
        =============================================================== */
      $('.selectpicker').on('change', function () {
          $(this).closest('.dropdown').find('.filter-option-inner-inner').addClass('selected');
      });


      /* ===============================================================
           TOGGLE ALTERNATIVE BILLING ADDRESS
        =============================================================== */
      $('#alternateAddressCheckbox').on('change', function () {
         var checkboxId = '#' + $(this).attr('id').replace('Checkbox', '');
         $(checkboxId).toggleClass('d-none');
      });


      /* ===============================================================
           DISABLE UNWORKED ANCHORS
        =============================================================== */
      $('a[href="#"]').on('click', function (e) {
         e.preventDefault();
      });

});


/* ===============================================================
     COUNTRY SELECT BOX FILLING
  =============================================================== */
$.getJSON('js/countries.json', function (data) {
    $.each(data, function (key, value) {
        var selectOption = "<option value='" + value.name + "' data-dial-code='" + value.dial_code + "'>" + value.name + "</option>";
        $("select.country").append(selectOption);
    });
})

function validateForm() {
    let x = document.forms['billing']['firstName'].value;
    if (x == "") {
        alert("Enter a valid first name");
        return false;
    }
    let x1 = document.forms['billing']['lastName'].value;
    if (x1 == "") {
        alert("Enter a valid last name");
        return false;
    }
    let x2 = document.forms['billing']['email'].value;
    if (x2 == "") {
        alert("Enter a valid email address");
        return false;
    }
    let x3 = document.forms['billing']['phone'].value;
    if (x3 == "") {
        alert("Enter a valid phone number");
        return false;
    }
    let x4 = document.forms['billing']['country'].value;
    if (x4 == "") {
        alert("Enter a valid country");
        return false;
    }
    let x5 = document.forms['billing']['address'].value;
    if (x5 == "") {
        alert("Enter a valid address");
        return false;
    }
    let x6 = document.forms['billing']['city'].value;
    if (x6 == "") {
        alert("Enter a valid city");
        return false;
    }
    let x7 = document.forms['billing']['state'].value;
    if (x7 == "") {
        alert("Enter a valid state");
        return false;
    }
}
