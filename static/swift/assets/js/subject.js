$(document).ready(function () {

    $("#SubjectsForm").validate({
        rules: {},
        messages: {},
        submitHandler: function (form, event) {
            event.preventDefault();
            var formData = $("#SubjectsForm").serializeArray();   // Serialize the form data into an array
            var url = $("#form_url").val()   // To get the URL of the form, use "form_url"
            $.ajax({
                url: url,
                headers: {
                    "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
                },
                method: "POST",
                data: formData,
                beforeSend: function () {
                    $("#subject-submit").attr("disabled", "disabled");  // Disable submit button
                    $("#subject-submit").val("Saving...");  // Change text submit button
                },
                success: function (response) {
                    if (response.status) {
                        $(".carousel__button").click()
                        FilterSubjects('')
                        $(".msg_desc").text(response.message)
                        $("#flash_message_success").attr("style", "display:block;")
                        setTimeout(function () {
                            $("#flash_message_success").attr("style", "display:none;")
                        }, 3500)
                    } else {
                        if ('message' in response) {
                            $(".carousel__button").click()
                            $(".msg_desc").text(response.message)
                            $("#flash_message_error").attr("style", "display:block;")
                            setTimeout(function () {
                                $("#flash_message_error").attr("style", "display:none;")
                            }, 3500)
                        } else {
                            $('#subject-form-div').html(response.template)  // Replaced with an AJAX template.
                        }
                    }
                },
                complete: function () {
                    $("#subject-submit").attr("disabled", false);
                    $("#subject-submit").val("Save");
                },
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
    var query = $('#search-input').val();
    var reset = $('#reset-input').val();
    var courses = $('#course-select').val(); // Get selected course values
    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: {
            'page': page,
            'search': query,
            'reset': reset,
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
        var query = $(this).val();
        FilterSubjects(query);
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
        text: "Are you sure you want to delete this record?",
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

