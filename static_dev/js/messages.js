MESSAGE_TAGS = {
  'debug': 'alert-info',
  'info': 'alert-info',
  'success': 'alert-success',
  'warning': 'alert-warning',
  'error': 'alert-danger',
}

function create_message(type, text) {
  let btn = document.createElement('button')
  btn.setAttribute('type', 'button')
  btn.setAttribute('data-bs-dismiss', 'alert')
  btn.setAttribute('aria-label', 'Close')
  btn.className = 'btn-close'
  let div = document.createElement('div')
  div.setAttribute('role', 'alert')
  div.className = 'alert alert-dismissible fade show ' + MESSAGE_TAGS[type]
  div.append(text)
  div.append(btn)
  return div
}

$(function () {
  set_messages_close_timeout()
})

function add_messages(messages) {
  $('#messages_block').html(messages)
  set_messages_close_timeout()
}

function set_messages_close_timeout() {
  $('#messages_block .alert').each(function () {
    setTimeout(() => hide_message(this), 5000)
  })
}

function hide_message(message) {
  (new bootstrap.Alert(message)).close()
}
