$(document).on('click', '.action-btn', function (event) {
    event.preventDefault()
    let url = $(this).attr('href')
    action_button_ajax_request(function () {
    }, url)
})

let check_updater

function check_handler() {
    $.ajax({
        url: check_updater_url,
        type: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        dataType: 'json',
        success: function (json_obj) {
            if ('messages' in json_obj) {
                add_messages(json_obj['messages'])
            }

            if (json_obj['status'] != 'ok') {
                return;
            }
            if (json_obj['check']) {
                document.location.href = json_obj['check_redirect']
            }
        },
        error: function () {
            add_messages(create_message('error', 'Error getting data from the server'))
        }
    })
}

function start_check_update() {
    check_updater = setInterval(check_handler, 10000)
}

function end_check_update() {
    clearInterval(check_updater)
}


$(function () {
    start_check_update()
})
