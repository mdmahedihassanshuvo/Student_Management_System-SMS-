# DJANGO IMPORTS
from django.db.models import Prefetch, Q

# LOCAL IMPORTS
from core.models import MenuSection


class SidebarMenuService:
    def __init__(self, user):
        self.user = user

    def get_menu_sections(self):
        """
        Returns active, published menu sections with menu items
        filtered based on the current user's groups.
        """
        user_groups = self.user.groups.all()

        menu_items_qs = self._get_permitted_menu_items(user_groups)

        sections = MenuSection.objects.prefetch_related(
            Prefetch('menu_items', queryset=menu_items_qs, to_attr='permitted_menu_items')  # noqa
        ).filter(
            is_active=True,
            is_draft=False
        ).order_by('order')

        # Now, filter out sections with no permitted_menu_items
        sections = [section for section in sections if section.permitted_menu_items] # noqa

        return sections

    def _get_permitted_menu_items(self, user_groups):
        """
        Returns menu items active & published and:
        - visible to all (if no groups assigned)
        - or assigned to any of the user's groups
        """
        if user_groups.exists():
            return (
                MenuSection._meta.get_field('menu_items').related_model.objects
                .prefetch_related('children', 'groups')
                .filter(
                    is_active=True,
                    is_draft=False
                ).filter(
                    Q(groups__in=user_groups) | Q(groups__isnull=True)
                ).distinct().order_by('order')
            )
        else:
            # If no groups, only get public menu items
            return (
                MenuSection._meta.get_field('menu_items').related_model.objects
                .prefetch_related('children', 'groups')
                .filter(
                    is_active=True,
                    is_draft=False,
                    groups__isnull=True
                ).order_by('order')
            )