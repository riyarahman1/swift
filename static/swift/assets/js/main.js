//----------------------- sidebar -toggle------------------
jQuery(document).ready(function() {
    $('.toggle-btn').on('click', function() {
        $('.side-bar').toggleClass('collapsed');
        $('.main-panel').toggleClass('body-expand');
    });

});

//----------------------- sub menu------------------

jQuery(document).ready(function() {
    jQuery('.sub-link').on('click', function() {
        var target = jQuery(this).parent().children(".sub-menu");
        jQuery(target).slideToggle(200);
        jQuery('.nav-link').not(this).parent().children('.dropdown-menu-dark').slideUp(200);
        jQuery(this).toggleClass('open-menu');
        jQuery('.nav-link').not(this).removeClass('open-menu');
    });
});