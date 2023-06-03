from django import template


register = template.Library()


@register.inclusion_tag("partials/link.html")
def link(request, app_name, path_name, content):
    return {
        "request": request,
        "path_name": path_name,
        "link_name": "{}:{}".format(app_name, path_name),
        "content": content
    }