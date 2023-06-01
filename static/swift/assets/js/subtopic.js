$(document).ready(function () {
    $("#SubtopicsForm").validate({
        rules: {},
        messages: {},
        submitHandler: function (form, event) {
            event.preventDefault();
            var formData = $("#SubtopicsForm").serializeArray();
            var url = $("#form_url").val()
            $.ajax({
                url: url,
                headers: {
                    "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
                },
                method: "POST",
                data: formData,
                beforeSend: function () {
                    $("#subtopic-submit").attr("disabled", "disabled");
                    $("#subtopic-submit").val("Saving...");
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
                            $('#subtopic-form-div').html(response.template)
                        }
                    }
                },
                complete: function () {
                    $("#subtopic-submit").attr("disabled", false);
                    $("#subtopic-submit").val("Save");
                },
            });
        },
    });
});

// -------------------------------------------------------------Filter,search and reset----------------------------------------------


function FilterSubtopics(page) {
    if (page === '') {
        page = parseInt($('#current_page').val()) || 1;
    }
    var url = $('#load_subtopic').val();
    var query = $('#search-input').val();
    var reset = $('#reset-input').val();
    var courses = $('#course-select').val(); // Get selected course values
    var subjects = $('#subject-select').val(); // Get selected subject values
    var topics = $('#topic-select').val(); // Get selected topic values

    if (subjects === '') {
        subjects = null;
    }

    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: {
            'page': page,
            'search': query,
            'reset': reset,
            'subject': subjects,
            'topic': topics,
            'course': courses,
        },
        beforeSend: function () { },
        success: function (response) {
            $('#subtopic-tbody').html(response.template);
            $('#subtopic-pagination').html(response.pagination);
        },
        complete: function () {

        }
    });
}

function updateCourseDropdown() {
    $.ajax({
        url: '/filter_courses/',
        type: 'GET',
        success: function (response) {
            var courseSelect = $('#course-select');
            courseSelect.empty();
            courseSelect.append($('<option>', {
                value: '',
                text: '- All Courses -'
            }));
            $.each(response.courses, function (index, course) {
                courseSelect.append($('<option>', {
                    value: course.id,
                    text: course.name
                }));
            });

            // Trigger change event to update the selected course
            courseSelect.trigger('change');
        }
    });
}
// search dropdown

function updateSubjectDropdown(courseId) {
    $.ajax({
        url: '/filter_subjects/',
        type: 'GET',
        data: {
            'course': courseId
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

            // Trigger change event to update the selected subject
            subjectSelect.trigger('change');
        }
    });
}

// search dropdown
function updateTopicDropdown(subjects) {
    $.ajax({
        url: '/filter_topics/',
        type: 'GET',
        data: {
            'subject': subjects
        },
        success: function (response) {
            var topicSelect = $('#topic-select');
            topicSelect.empty();
            topicSelect.append($('<option>', {
                value: '',
                text: '- All Topics -'
            }));
            $.each(response.topics, function (index, topic) {
                topicSelect.append($('<option>', {
                    value: topic.id,
                    text: topic.name
                }));
            });

            // Trigger change event to update the selected topic
            topicSelect.trigger('change');
        }
    });
}




$(document).ready(function () {
    $('#search-form').submit(function (e) {
        e.preventDefault();
        FilterSubtopics('');
    });

    $('#search-input').on('keyup', function () {
        var query = $(this).val();
        FilterSubtopics(query);
    });

    $('#course-select').change(function () {
        var courseId = $(this).val(); // Get selected course value
        updateSubjectDropdown(courseId);
        FilterSubtopics('');
    });

    $('#subject-select').change(function () {
        var subjects = $(this).val(); // Get selected subject values
        updateTopicDropdown(subjects);
        FilterSubtopics('');
    });

    $('#topic-select').change(function () {
        var topics = $(this).val(); // Get selected topic values
        FilterSubtopics(topics);
    });

    $('#reset-button').click(function () {
        $('#search-input').val('');
        $('#course-select').val('');
        $('#subject-select').val('');
        $('#topic-select').val('');
        $('#reset-input').val('true');
        updateSubjectDropdown(''); // Reset subject dropdown
        updateTopicDropdown('');
        updateCourseDropdown('');
        FilterSubtopics('');
    });
});


// -------------------------------------------------------------create subtopic----------------------------------------------
$(document).on('click', '#create_subtopic', function (event) {
    event.preventDefault();
    var url = $(this).attr('data-url');
    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: {},
        beforeSend: function () {
            $('#subtopic-form-div').html('Loading...');
        },
        success: function (response) {
            $('#subtopic-form-div').html(response.template);
            $('#popup_head').html(response.title);

            // Event handler for course change
            $('#id_course').change(function () {
                var courseId = $(this).val();
                $.ajax({
                    url: '/subtopic/subjectfilter/',
                    type: 'GET',
                    data: {
                        'course': courseId
                    },
                    success: function (response) {
                        var subjectSelect = $('#id_subject');
                        subjectSelect.empty();

                        $.each(response.subjects, function (index, subject) {
                            subjectSelect.append($('<option>', {
                                value: subject.id,
                                text: subject.name
                            }));
                        });

                        var topicSelect = $('#id_topic');
                        topicSelect.empty();
                        topicSelect.append($('<option>', {
                            value: '',
                            text: '---------'
                        }));

                        subjectSelect.trigger('change');
                    }
                });
            });

            // Event handler for subject change
            $(document).off('change', '#id_subject').on('change', '#id_subject', function () {
                var subjectId = $(this).val();
                var courseId = $('#id_course').val();
                $.ajax({
                    url: '/subtopic/topicfilter/',
                    type: 'GET',
                    data: {
                        'subject': subjectId,
                        'course': courseId
                    },
                    success: function (response) {
                        var topicSelect = $('#id_topic');
                        topicSelect.empty();

                        $.each(response.topics, function (index, topic) {
                            topicSelect.append($('<option>', {
                                value: topic.id,
                                text: topic.name
                            }));
                        });
                    }
                });
            });

            // Initialize form validation
            $("#SubtopicsForm").validate({
                rules: {},
                messages: {},
                submitHandler: function (form, event) {
                }
            });
        },
    });
});




// -------------------------------------------------------------edit subtopic----------------------------------------------

$(document).on('click', '.subtopic-edit', function (event) {
    event.preventDefault();
    var url = $(this).attr('data-url');

    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: {},
        beforeSend: function () {
            $('#subtopic-form-div').html('Loading...');
        },
        success: function (response) {
            $('#subtopic-form-div').html(response.template);
            $('#popup_head').html(response.title);

            $(document).off('change', '#id_course').on('change', '#id_course', function () {
                var courseId = $(this).val();
                $.ajax({
                    url: '/subtopic/subjectfilter/',
                    type: 'GET',
                    data: {
                        'course': courseId
                    },
                    success: function (response) {
                        var subjectSelect = $('#id_subject');
                        subjectSelect.empty();

                        $.each(response.subjects, function (index, subject) {
                            subjectSelect.append($('<option>', {
                                value: subject.id,
                                text: subject.name
                            }));
                        });

                        var topicSelect = $('#id_topic');
                        topicSelect.empty();
                        topicSelect.append($('<option>', {
                            value: '',
                            text: '---------'
                        }));

                        subjectSelect.trigger('change');
                    }
                });
            });

            // Event handler for topic change in edit
            $(document).off('change', '#id_subject').on('change', '#id_subject', function () {
                var subjectId = $(this).val();
                var courseId = $('#id_course').val();
                $.ajax({
                    url: '/subtopic/topicfilter/',
                    type: 'GET',
                    data: {
                        'subject': subjectId,
                        'course': courseId
                    },
                    success: function (response) {
                        var topicSelect = $('#id_topic');
                        topicSelect.empty();

                        $.each(response.topics, function (index, topic) {
                            topicSelect.append($('<option>', {
                                value: topic.id,
                                text: topic.name
                            }));
                        });
                    }
                });
            });

            // Trigger change event on subject, topic, and course selects in edit
            $('#id_subject').trigger('change');
            $('#id_topic').trigger('change');
            $('#id_course').trigger('change');
        },
    });
});






// Function to delete topic
function DeleteSubtopic(id) {
    var url = '/subtopic/' + String(id) + '/delete/'
    swal({
        icon: "warning",
        title: "Verify Details",
        text: "Are you sure you want to delete this Subtopic?",
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
                        FilterSubtopics('')
                    }
                },
            });
        }
    });
}