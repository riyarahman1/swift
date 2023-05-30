$(document).ready(function () {
    $("#TopicsForm").validate({
        rules: {},
        messages: {},
        submitHandler: function (form, event) {
            event.preventDefault();
            var formData = $("#TopicsForm").serializeArray();
            var url = $("#form_url").val()
            $.ajax({
                url: url,
                headers: {
                    "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
                },
                method: "POST",
                data: formData,
                beforeSend: function () {
                    $("#topic-submit").attr("disabled", "disabled");
                    $("#topic-submit").val("Saving...");
                },
                success: function (response) {
                    if (response.status) {
                        $(".carousel__button").click()
                        FilterTopics('')
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
                            $('#topic-form-div').html(response.template)
                        }
                    }
                },
                complete: function () {
                    $("#topic-submit").attr("disabled", false);
                    $("#topic-submit").val("Save");
                },
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
    $.ajax({
        url: '/topic/searchfilter/',
        type: 'GET',
        data: {
            'course_id': courseId
        },
        success: function (response) {
            var subjectSelect = $('#subject-select');
            subjectSelect.empty();
            subjectSelect.append($('<option>', {
                value: '',
                text: '- All Subjects -'
            }));
            $.each(response.subjects, function (index, subject) {
                subjectSelect.append($('<option>', {
                    value: subject.id,
                    text: subject.name
                }));
            });
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
        var courseId = $(this).val(); // Get selected course option value
        updateSubjectDropdown(courseId);
        FilterTopics('');
    });

    $('#reset-button').click(function () {
        $('#search-input').val('');
        $('#subject-select').val('');
        $('#course-select').val('');
        $('#reset-input').val('true');
        FilterTopics('');
    });
});



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
                    url: '/topic/filter/',
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


            $('#id_course').change(function () {
                var course_id = $(this).val();
                var subjectsUrl = '/topic/filter/';

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
                        FilterTopics('')
                    }
                },
            });
        }
    });
}