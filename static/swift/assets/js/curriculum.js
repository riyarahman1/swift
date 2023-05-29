$(document).ready(function() {
    $("#CurriculumForm").validate({
        rules: {},
        messages: {},
        submitHandler: function(form, event) {
            event.preventDefault();
            var formData = $("#CurriculumForm").serializeArray();
            var url = $("#form_url").val()
            $.ajax({
                url: url,
                headers: {
                    "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
                },
                method: "POST",
                data: formData,
                beforeSend: function() {
                    $("#curriculum-submit").attr("disabled", "disabled");
                    $("#curriculum-submit").val("Saving...");
                },
                success: function(response) {
                    if (response.status) {                        
                        $(".carousel__button").click()
                        FilterCurriculum('')
                        $(".msg_desc").text(response.message)
                        $("#flash_message_success").attr("style", "display:block;")
                        setTimeout(function() {
                            $("#flash_message_success").attr("style", "display:none;")
                        }, 3500)
                    } else {
                        if ('message' in response ){
                            $(".carousel__button").click()
                            $(".msg_desc").text(response.message)
                            $("#flash_message_error").attr("style", "display:block;")
                            setTimeout(function() {
                                $("#flash_message_error").attr("style", "display:none;")
                            }, 3500)                                                       
                        } else {                        
                            $('#curriculum-form-div').html(response.template)     
                        } 
                    }                
                },
                complete: function() {
                    $("#curriculum-submit").attr("disabled", false);
                    $("#curriculum-submit").val("Save");
                },
            });
        },
    });
});

function FilterCurriculum(page) {
    if (page == '') {
        page = $('#current_page').val()
    }
    var url = $('#load_curriculum').val()
    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: { 'page': page },
        beforeSend: function() {},
        success: function(response) {
            $('#curriculum-tbody').html(response.template)
            $('#curriculum-pagination').html(response.pagination)
        },
    });
}

$(document).on('click', '#create_curriculum', function(event) {
    event.preventDefault();
    var url = $(this).attr('data-url')
    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: {},
        beforeSend: function() {
            $('#curriculum-form-div').html('Loading...')
        },
        success: function(response) {            
            $('#curriculum-form-div').html(response.template)
            $('#popup_head').html(response.title)
        },
    });
})
$(document).on('click', '.curriculum-edit', function(event) {
    event.preventDefault();
    var url = $(this).attr('data-url')
    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: {},
        beforeSend: function() {
            $('#curriculum-form-div').html('Loading...')
        },
        success: function(response) {
            $('#curriculum-form-div').html(response.template)
            $('#popup_head').html(response.title)
        },
    });
})

// Function to delete curriculum
function DeleteCurriculum(id) {
    var url = '/curriculum/' + String(id) + '/delete/'
    swal({
        icon: "warning",
        title: "Verify Details",
        text: "Are you sure you want to delete this record?",
        buttons: true,
        dangerMode: true,
    }).then(function(okey) {
        if (okey) {
            $.ajax({
                url: url,
                headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
                method: "POST",
                data: {},
                beforeSend: function() {},
                success: function(response) {
                    if (response.status) {
                        $(".msg_desc").text(response.message);
                        $("#flash_message_success").attr("style", "display:block;");
                        setTimeout(function() {
                            $("#flash_message_success").attr("style", "display:none;");
                        }, 3500);
                        FilterCurriculum('')
                    }
                },
            });
        }
    });
}