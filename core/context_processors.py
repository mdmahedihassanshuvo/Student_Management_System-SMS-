# LOCAL IMPORTS
from core.services.sidebar_service import SidebarMenuService


def sidebar_menu(request):
    service = SidebarMenuService(request.user)
    sections = service.get_menu_sections()
    return {'menu_sections': sections}