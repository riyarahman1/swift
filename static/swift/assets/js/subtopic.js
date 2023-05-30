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


// Filter,search and reset

function FilterSubtopics(page) {
    if (page === '') {
        page = parseInt($('#current_page').val()) || 1;
    }
    var url = $('#load_subtopic').val();
    var query = $('#search-input').val();
    var reset = $('#reset-input').val();
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
        },
        beforeSend: function () { },
        success: function (response) {
            $('#subtopic-tbody').html(response.template);
            $('#subtopic-pagination').html(response.pagination);
        },
        complete: function () {
            updateTopicDropdown(subjects);
        }
    });
}

function updateTopicDropdown(subjectId) {
    $.ajax({
        url: '/subtopic/searchfilter/',
        type: 'GET',
        data: {
            'subject_id': subjectId
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

    $('#subject-select').change(function () {
        var subjects = $(this).val(); // Get selected subject values
        FilterSubtopics('');
        updateTopicDropdown(subjects);
    });

    $('#topic-select').change(function () {
        var topics = $(this).val(); // Get selected topic values
        FilterSubtopics(topics);
    });

    $('#reset-button').click(function () {
        $('#search-input').val('');
        $('#subject-select').val('');
        $('#topic-select').val('');
        $('#reset-input').val('true');
        FilterSubtopics('');
    });
});



// $(document).on('click', '#create_subtopic', function (event) {
//     event.preventDefault();
//     var url = $(this).attr('data-url');
//     $.ajax({
//         url: url,
//         headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
//         method: "GET",
//         data: {},
//         beforeSend: function () {
//             $('#subtopic-form-div').html('Loading...');
//         },
//         success: function (response) {
//             $('#subtopic-form-div').html(response.template);
//             $('#popup_head').html(response.title);
//         },
//     });
// });

// // Event handler for topic change
// $(document).on('change', '#id_topic', function () {
//     var topicId = $(this).val();

//     // Retrieve the corresponding subjects for the selected topic
//     $.ajax({
//         url: '/subtopic/filter/',
//         type: 'GET',
//         data: {
//             'topic_id': topicId
//         },
//         success: function (response) {
//             var subjectSelect = $('#id_subject');
//             subjectSelect.empty();

//             // Add the retrieved subjects to the subject dropdown
//             $.each(response.subjects, function (index, subject) {
//                 subjectSelect.append($('<option>', {
//                     value: subject.id,
//                     text: subject.name
//                 }));
//             });

//             // Clear the course dropdown
//             var courseSelect = $('#id_course');
//             courseSelect.empty();
//             courseSelect.append($('<option>', {
//                 value: '',
//                 text: '---------'
//             }));

//             // Trigger the subject change event to update the course dropdown
//             subjectSelect.trigger('change');
//         }
//     });
// });

// // Event handler for subject change
// $(document).on('change', '#id_subject', function () {
//     var subjectId = $(this).val();

//     // Retrieve the corresponding courses for the selected subject
//     $.ajax({
//         url: '/subtopic/filter/',
//         type: 'GET',
//         data: {
//             'subject_id': subjectId
//         },
//         success: function (response) {
//             var courseSelect = $('#id_course');
//             courseSelect.empty();

//             // Add the retrieved courses to the course dropdown
//             $.each(response.courses, function (index, course) {
//                 courseSelect.append($('<option>', {
//                     value: course.id,
//                     text: course.name
//                 }));
//             });
//         }
//     });
// });
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

        
            $(document).on('change', '#id_topic', function () {
                var topicId = $(this).val();

               
                $.ajax({
                    url: '/subtopic/filter/',
                    type: 'GET',
                    data: {
                        'topic_id': topicId
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

                        var courseSelect = $('#id_course');
                        courseSelect.empty();
                        courseSelect.append($('<option>', {
                            value: '',
                            text: '---------'
                        }));
                    }
                });
            });

            $(document).on('change', '#id_subject', function () {
                var subjectId = $(this).val();

                
                $.ajax({
                    url: '/subtopic/filter/',
                    type: 'GET',
                    data: {
                        'subject_id': subjectId
                    },
                    success: function (response) {
                        var courseSelect = $('#id_course');
                        courseSelect.empty();

                        // Add the retrieved courses to the course dropdown
                        $.each(response.courses, function (index, course) {
                            courseSelect.append($('<option>', {
                                value: course.id,
                                text: course.name
                            }));
                        });
                    }
                });
            });
        },
    });
});





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


            $('#id_course').change(function () {
                var course_id = $(this).val();
                var subjectsUrl = '/subtopic/filter/';

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
    var url = '/subtopic/' + String(id) + '/delete/'
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
                        FilterSubtopics('')
                    }
                },
            });
        }
    });
}