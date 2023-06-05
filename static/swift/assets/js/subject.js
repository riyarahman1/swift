$(document).ready(function () {

    $("#SubjectsForm").validate({
        rules: {},
        messages: {},
        submitHandler: function (form, event) {
            event.preventDefault();
            var formData = $("#SubjectsForm").serializeArray();
            var url = $("#form_url").val()
            
              function showConfirmationDialog() {
                return Swal.fire({
                    title: "Confirmation",
                    text: "Are you sure you want to proceed?",
                    icon: "question",
                    showCancelButton: true,
                    confirmButtonColor: "#3085d6",
                    cancelButtonColor: "#d33",
                    confirmButtonText: "Yes",
                    cancelButtonText: "Cancel",
                    allowOutsideClick: false,
                    allowEscapeKey: false,
                    toast: true,
                    showConfirmButton: true,
                    timer: 3000,
                });
            }
    
            showConfirmationDialog().then((result) => {
                if (result.isConfirmed) {
                    $.ajax({
                        url: url,
                        headers: {
                            "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val(),
                        },
                        method: "POST",
                        data: formData,
                        beforeSend: function () {
                            $("#subject-submit").attr("disabled", true).val("Saving...");
                        },
                        success: function (response) {
                            if (response.status) {
                                $(".carousel__button").click();
                                FilterSubjects("");
                                $(".msg_desc").text(response.message);
                                $("#flash_message_success").fadeIn().delay(3500).fadeOut();
                                form.reset(); // Reset the form to its initial state
                                $('#myModal').modal('hide'); // Close the modal
                            } else if ("message" in response) {
                                $(".carousel__button").click();
                                $(".msg_desc").text(response.message);
                                $("#flash_message_error").fadeIn().delay(3500).fadeOut();
                            } else {
                                $('#subject-form-div').html(response.template);
                            }
                        },
                        complete: function () {
                            $("#subject-submit").attr("disabled", false).val("Save");
                        },
                    });
                }
            });
        },
    });
});


// Filter,search and reset

function FilterSubjects(page) {
    if (page == '') {
        page = parseInt($('#current_page').val()) || 1;
    }
    var url = $('#load_subject').val();
    var querys = $('#search-input').val();
    var resets = $('#reset-input').val();
    var courses = $('#course-select').val(); // Get selected course values
    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: {
            'page': page,
            'searchs': querys,
            'resets': resets,
            'course': courses // Pass the selected course values

        },
        beforeSend: function () { },
        success: function (response) {
            $('#subject-tbody').html(response.template);
            $('#subject-pagination').html(response.pagination);
        },
    });
}

$(document).ready(function () {
    $('#search-form').submit(function (e) {
        e.preventDefault();
        FilterSubjects('');
    });

    $('#search-input').on('keyup', function () {
        var querys = $(this).val();
        FilterSubjects(querys);
    });

    $('#course-select').change(function () {
        var courses = $(this).val(); // Get selected course values
        FilterSubjects(courses);
    });
    
    $('#reset-button').click(function () {
        $('#search-input').val('');
        $('#course-select').val('');
        $('#reset-input').val('true');
        FilterSubjects('');
    });
});



$(document).on('click', '#create_subject', function (event) {
    event.preventDefault();
    var url = $(this).attr('data-url')
    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: {},
        beforeSend: function () {
            $('#subject-form-div').html('Loading...')
        },
        success: function (response) {
            $('#subject-form-div').html(response.template)
            $('#popup_head').html(response.title)
        },
    });
})
$(document).on('click', '.subject-edit', function (event) {
    event.preventDefault();
    var url = $(this).attr('data-url')
    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: {},
        beforeSend: function () {
            $('#subject-form-div').html('Loading...')
        },
        success: function (response) {
            $('#subject-form-div').html(response.template)
            $('#popup_head').html(response.title)
        },
    });
})

// Function to delete subject
function DeleteSubject(id) {
    var url = '/subject/' + String(id) + '/delete/'
    swal({
        icon: "warning",
        title: "Verify Details",
        text: "Are you sure you want to delete this subject?",
        buttons: true,
        dangerMode: true,
    }).then(function (okey) {
        if (okey) {
            $.ajax({
                url: url,
                headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
                method: "POST",
                data: {},
                beforeSend: function () { },
                success: function (response) {
                    if (response.status) {
                        $(".msg_desc").text(response.message);
                        $("#flash_message_success").attr("style", "display:block;");
                        setTimeout(function () {
                            $("#flash_message_success").attr("style", "display:none;");
                        }, 3500);
                        FilterSubjects('')
                    }
                },
            });
        }
    });
}