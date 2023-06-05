$(document).ready(function () {

    $("#CourseForm").validate({
        rules: {},
        messages: {},
        submitHandler: function (form, event) {
            event.preventDefault();
            var formData = $("#CourseForm").serializeArray();
            var url = $("#form_url").val();
    
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
                            $("#course-submit").attr("disabled", true).val("Saving...");
                        },
                        success: function (response) {
                            if (response.status) {
                                $(".carousel__button").click();
                                FilterCourse("");
                                $(".msg_desc").text(response.message);
                                $("#flash_message_success").fadeIn().delay(3500).fadeOut();
                                form.reset(); // Reset the form to its initial state
                                $('#myModal').modal('hide'); // Close the modal
                            } else if ("message" in response) {
                                $(".carousel__button").click();
                                $(".msg_desc").text(response.message);
                                $("#flash_message_error").fadeIn().delay(3500).fadeOut();
                            } else {
                                $('#course-form-div').html(response.template);
                            }
                        },
                        complete: function () {
                            $("#course-submit").attr("disabled", false).val("Save");
                        },
                    });
                }
            });
        },
    });
    
});

// Filter,search and reset
function FilterCourse(page) {
    if (page == '') {
        page = parseInt($('#current_page').val()) || 1;
    }
    var url = $('#load_course').val();
    var query = $('#search-input').val();
    var reset = $('#reset-input').val();
    var curriculums = $('#curriculum-select').val(); // Get selected curriculum values
    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: {
            'page': page,
            'search': query,
            'reset': reset,
            'curriculum': curriculums // Pass the selected curriculum values
        },
        beforeSend: function () { },
        success: function (response) {
            $('#course-tbody').html(response.template);
            $('#course-pagination').html(response.pagination);
        },
    });
}

$(document).ready(function () {
    $('#search-form').submit(function (e) {
        e.preventDefault();
        FilterCourse('');
    });

    $('#search-input').on('keyup', function () {
        var query = $(this).val();
        FilterCourse(query);
    });

    $('#curriculum-select').change(function () {
        var curriculums = $(this).val(); // Get selected curriculum values
        FilterCourse(curriculums);
    });

    $('#reset-button').click(function () {
        $('#search-input').val('');
        $('#curriculum-select').val('');
        $('#reset-input').val('true');
        FilterCourse('');
    });
});





$(document).on('click', '#create_course', function (event) {
    event.preventDefault();
    var url = $(this).attr('data-url')
    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: {},
        beforeSend: function () {
            $('#course-form-div').html('Loading...')
        },
        success: function (response) {
            $('#course-form-div').html(response.template)      // Replaced with an AJAX template.
            $('#popup_head').html(response.title)    //title from the response
        },
    });
})
$(document).on('click', '.course-edit', function (event) {
    event.preventDefault();
    var url = $(this).attr('data-url');
    $.ajax({
        url: url,
        method: "GET",
        data: {},
        beforeSend: function () {
            $('#course-form-div').html('Loading...');
        },
        success: function (response) {
            $('#course-form-div').html(response.template);
            $('#popup_head').html(response.title);
        },
    });
});

// Function to delete course
function DeleteCourse(id) {
    var url = '/course/' + String(id) + '/delete/'
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
                        FilterCourse('')
                    }
                },
            });
        }
    });
}



