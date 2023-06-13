from django import template


register = template.Library()


@register.inclusion_tag("partials/main_menu.html")
def main_menu(request, app_name, list_path_name, create_path_name, search_path_name, menu_name, icon_type, list_content, create_content):
    return {
        "request": request,
        "list_path_name": list_path_name,
        "create_path_name": create_path_name,
        "search_path_name": search_path_name,
        "list_link_name": "{}:{}".format(app_name, list_path_name),
        "create_link_name": "{}:{}".format(app_name, create_path_name),
        "menu_name": menu_name,
        "icon_type": icon_type,
        "list_content": list_content,
        "create_content": create_content
    }