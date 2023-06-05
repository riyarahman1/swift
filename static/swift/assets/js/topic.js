$(document).ready(function () {
    $("#TopicsForm").validate({
        rules: {},
        messages: {},
        submitHandler: function (form, event) {
            event.preventDefault();
            var formData = $("#TopicsForm").serializeArray();
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
                    allowOutsideClick: false,   // Prevent closing on outside click
                    allowEscapeKey: false,      // Prevent closing on Escape key press
                    toast: true,                // Display as toast notification
                    // position: "top-end",        // Position the toast notification at the top-end
                    showConfirmButton: true,   // Hide the confirm button in toast mode
                    timer: 3000,                // Auto-close the toast after 3 seconds
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
                            $("#topic-submit").attr("disabled", true).val("Saving...");
                        },
                        success: function (response) {
                            if (response.status) {
                                $(".carousel__button").click();
                                FilterTopics("");
                                $(".msg_desc").text(response.message);
                                $("#flash_message_success").fadeIn().delay(3500).fadeOut();
                                form.reset(); // Reset the form to its initial state
                                $('#myModal').modal('hide'); // Close the modal
                            } else if ("message" in response) {
                                $(".carousel__button").click();
                                $(".msg_desc").text(response.message);
                                $("#flash_message_error").fadeIn().delay(3500).fadeOut();
                            } else {
                                $('#topic-form-div').html(response.template);
                            }
                        },
                        complete: function () {
                            $("#topic-submit").attr("disabled", false).val("Save");
                       },
                    });
                }
            });
        },
    });
    
});

// Filter,search and reset

function FilterTopics(page) {
    if (page == '') {
        page = parseInt($('#current_page').val()) || 1;
    }
    var url = $('#load_topic').val();
    var query = $('#search-input').val();
    var reset = $('#reset-input').val();
    var subjects = $('#subject-select').val();
    var courses = $('#course-select').val();

    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: {
            'page': page,
            'search': query,
            'reset': reset,
            'subject': subjects,
            'course': courses,
        },
        beforeSend: function () { },
        success: function (response) {
            $('#topic-tbody').html(response.template);
            $('#topic-pagination').html(response.pagination);
        },
    });
}

function updateSubjectDropdown(courseId) {
    var data = {
        'course_id': courseId ? courseId : null
    };
    $.ajax({
        url: '/topic/searchfilter/',
        type: 'GET',
        data: data,
        success: function (response) {
            var subjectSelect = $('#subject-select');
            subjectSelect.empty();
            subjectSelect.append($('<option>', {
                value: '',
                text: '- All Subjects -'
            }));
            if (response.subjects) {
                $.each(response.subjects, function (index, subject) {
                    subjectSelect.append($('<option>', {
                        value: subject.id,
                        text: subject.name
                    }));
                });
            }

            // Set the previously selected subject value
            var selectedSubject = $('#subject-select').data('selected-value');
            if (selectedSubject) {
                subjectSelect.val(selectedSubject);
            }
        }
    });
}




$(document).ready(function () {
    $('#search-form').submit(function (e) {
        e.preventDefault();
        FilterTopics('');
    });

    $('#search-input').on('input', function () {
        FilterTopics('');
    });
    $('#subject-select').change(function () {
        var subjects = $(this).val(); // Get selected subject values
        FilterTopics(subjects);
    });

    $('#course-select').change(function () {
        var courseId = $(this).val();
        var selectedSubject = $('#subject-select').val(); // Store the selected subject value
        updateSubjectDropdown(courseId); // Pass the courseId
        FilterTopics('');
    });
    
    
    $('#reset-button').click(function () {
        $('#search-input').val('');
        $('#subject-select').val('');
        $('#course-select').val('');
        $('#reset-input').val('true');
        updateSubjectDropdown(null); 
        FilterTopics('');
        return false; 
    });
    

});
// -------------------------------------------------------------create topic----------------------------------------------


$(document).on('click', '#create_topic', function (event) {
    event.preventDefault();
    var url = $(this).attr('data-url');
    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: {},
        beforeSend: function () {
            $('#topic-form-div').html('Loading...');
        },
        success: function (response) {
            $('#topic-form-div').html(response.template);
            $('#popup_head').html(response.title);


            $('#id_course').change(function () {
                var course_id = $(this).val();  // Get the selected course option value

                //  filtered subject options
                $.ajax({
                    url: '/topic/searchfilter/',
                    type: 'GET',
                    data: {
                        'course_id': course_id
                    },
                    success: function (response) {

                        $('#id_subject').empty();
                        $.each(response.subjects, function (index, subject) {
                            $('#id_subject').append($('<option>', {
                                value: subject.id,
                                text: subject.name
                            }));
                        });
                    }
                });
            });
        },
    });
});



$(document).on('click', '.topic-edit', function (event) {
    event.preventDefault();
    var url = $(this).attr('data-url');

    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: {},
        beforeSend: function () {
            $('#topic-form-div').html('Loading...');
        },
        success: function (response) {
            $('#topic-form-div').html(response.template);
            $('#popup_head').html(response.title);

            // Set the value for the id_course select element
            var courseSelect = $('#id_course');
            courseSelect.val(response.course_id);

            $('#id_course').change(function () {
                var course_id = $(this).val();
                var subjectsUrl = '/topic/searchfilter/';

                $.ajax({
                    url: subjectsUrl,
                    method: "GET",
                    data: {
                        course_id: course_id
                    },
                    beforeSend: function () {

                    },
                    success: function (response) {
                        var subjectSelect = $('#id_subject');
                        subjectSelect.empty();

                        $.each(response.subjects, function (index, subject) {
                            var option = $('<option>').val(subject.id).text(subject.name);
                            subjectSelect.append(option);
                        });
                    },
                    error: function (xhr, textStatus, error) {

                    }
                });
            });
        },
        error: function (xhr, textStatus, error) {

        }
    });
});



// Function to delete topic
function DeleteTopic(id) {
    var url = '/topic/' + String(id) + '/delete/'
    swal({
        icon: "warning",
        title: "Verify Details",
        text: "Are you sure you want to delete this Topic?",
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
                        FilterTopics('')
                    }
                },
            });
        }
    });
}