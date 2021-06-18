function form_ajax_request(success_func, form, target = undefined, extra_data = '', url = undefined) {
  let data = form.serialize()
  if (extra_data !== '') {
    data += '&' + extra_data
  }
  if (url === undefined) {
    url = form.attr('action')
  }
  $.ajax({
    url: url,
    type: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken')
    },
    data: data,
    dataType: 'json',
    success: function (json_obj) {
      process_standard_fields(json_obj)
      if (target === undefined) {
        success_func(json_obj)
      } else {
        success_func(json_obj, target)
      }
    },
    error: function () {
      add_messages(create_message('error', 'Error getting data from the server'))
    }
  })
}

function action_button_ajax_request(success_func, url, target = null, data = null) {
  $.ajax({
    url: url,
    type: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken')
    },
    data: data,
    dataType: 'json',
    success: function (json_obj) {
      process_standard_fields(json_obj)
      if (target) {
        success_func(json_obj, target)
      } else {
        success_func(json_obj)
      }
    },
    error: function () {
      add_messages(create_message('error', 'Error getting data from the server'))
    }
  })
}

function process_standard_fields(json_obj) {
  if ('messages' in json_obj) {
    add_messages(json_obj['messages'])
  }
  if ('redirect' in json_obj) {
    document.location.href = json_obj['redirect']
  }
  if ('reload' in json_obj) {
    document.location.reload()
  }
}
