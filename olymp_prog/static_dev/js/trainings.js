$(document).on('click', '.action-btn', function (event) {
    event.preventDefault()
    let url = $(this).attr('href')
    action_button_ajax_request(function () {
    }, url)
})

$(document).on('click', '.toggle-tags-selection-window-btn', function (event) {
    let tags_select_block = find_tags_select_parent_block(this)
    tags_select_block.find('input[name=tag-name]').val('')
    tags_select_block.find('.tags-selection-window').toggle()
})

$(document).on('click', '.not-selected-tag .tag', function (event) {
    select_tag($(this).parent()[0])
})

$(document).on('click', '.selected-tag .tag', function (event) {
    unselect_tag($(this).parent()[0])
})

$(document).on('click', '.add-new-tag-btn', function (event) {
    let btn = $(this)
    let url = btn.attr('data-href')
    let tag_name = btn.siblings('input[name=tag-name]').val()
    if (!tag_name) {
        add_messages(create_message('error', 'Tag name can\'t be empty'))
        return
    }
    action_button_ajax_request(tags_add_success, url, this, {'tag-name': tag_name})
})

$(document).on('click', '.tag-trash-btn', function (event) {
    let btn = $(this)
    let url = delete_tag_url
    let value = btn.parents('.not-selected-tag').attr('data-value')
    action_button_ajax_request(tags_delete_success, url, this, {'tag-value': value})
})

function find_tags_select_parent_block(element) {
    return $(element).parents('.tags-select')
}

function select_tag(tag) {
    let tags_select_block = find_tags_select_parent_block(tag)
    let selected_tags_block = tags_select_block.find('.selected-tags')
    let select_input_block = tags_select_block.find('.tags-select-input select')

    tag = $(tag)
    tag.removeClass('not-selected-tag')
    tag.addClass('selected-tag')

    let tag_value = tag.attr('data-value')
    select_input_block.children(`option[value=${tag_value}]`).prop('selected', true)

    selected_tags_block.append(tag)
}

function unselect_tag(tag) {
    let tags_select_block = find_tags_select_parent_block(tag)
    let not_selected_tags_block = tags_select_block.find('.not-selected-tags')
    let select_input_block = tags_select_block.find('.tags-select-input select')

    tag = $(tag)
    tag.removeClass('selected-tag')
    tag.addClass('not-selected-tag')

    let tag_value = tag.attr('data-value')
    select_input_block.children(`option[value=${tag_value}]`).prop('selected', false)

    not_selected_tags_block.append(tag)
}

function create_tag(name, value) {
    let div = $(document.createElement('div'))
    let span = $(document.createElement('span'))
    let img = $(document.createElement('img'))

    span.text(name)
    span.attr('class', 'badge rounded-pill bg-primary tag me-1')

    img.attr('src', trash_icon_url)
    img.attr('class', 'tag-trash-btn')
    img.attr('width', '10')
    img.attr('alt', 'trash icon')

    div.attr('class', 'not-selected-tag')
    div.attr('data-value', value)
    div.append(span)
    div.append(img)

    return div
}

function create_tag_option(name, value) {
    let option = $(document.createElement('option'))
    option.text(name)
    option.attr('value', value)
    return option
}

function tags_add_success(json_obj, target) {
    if (json_obj['status'] != 'ok') {
        return
    }
    let new_tag = create_tag(json_obj['new_tag']['name'], json_obj['new_tag']['value'])
    let new_tag_option = create_tag_option(json_obj['new_tag']['name'], json_obj['new_tag']['value'])
    new_tag_option.prop('selected', true)
    let tags_select_block = find_tags_select_parent_block(target)
    tags_select_block.find('.not-selected-tags').append(new_tag)
    tags_select_block.find('.tags-select-input select').append(new_tag_option)
    tags_select_block.find('input[name=tag-name]').val('')
}

function tags_delete_success(json_obj, target) {
    if (json_obj['status'] != 'ok') {
        return
    }
    let tags_select_block = find_tags_select_parent_block(target)
    tags_select_block.find(`.not-selected-tags .not-selected-tag[data-value=${json_obj['tag_value']}]`).remove()
    tags_select_block.find(`.selected-tags .selected-tag[data-value=${json_obj['tag_value']}]`).remove()
    tags_select_block.find(`tags-select-input select option[value=${json_obj['tag_value']}]`).remove()
}
