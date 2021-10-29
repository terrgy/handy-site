from django.template.defaulttags import register


@register.inclusion_tag('blocks/user_link.html', takes_context=True)
def user_link(context, user):
    return {'user': user, 'auth_user': context['user']}
