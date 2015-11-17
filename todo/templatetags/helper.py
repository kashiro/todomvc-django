from django import template
register = template.Library()

@register.filter
def filter_todo(todos, filter):
    if filter == 'active':
        return get_incompleted(todos)
    elif filter == 'completed':
        return get_completed(todos)
    else:
        return todos

@register.filter
def get_incompleted(todos):
    return todos.filter(completed=False)

@register.filter
def get_completed(todos):
    return todos.filter(completed=True)
