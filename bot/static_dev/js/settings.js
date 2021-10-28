$(document).on('submit', '.edit-form', function (event) {
  event.preventDefault()
  let form_obj = $(this)
  form_ajax_request(edit_success_form, form_obj)
})

function edit_success_form() {
}
