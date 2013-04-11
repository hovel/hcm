$("#account_logout").click(function(e) {
    e.preventDefault();
    $(this).siblings("#logout_form").submit();
});