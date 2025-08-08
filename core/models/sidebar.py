# DJANGO IMPORTS
from django.db import models
from django.contrib.auth.models import Group
from django.urls import reverse, NoReverseMatch
from django.utils.translation import gettext_lazy as _

# LOCAL IMPORTS
from .common import CommonModels


class MenuSection(CommonModels):
    title = models.CharField(_('Section Title'), max_length=100)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class MenuItem(CommonModels):
    section = models.ForeignKey(
        MenuSection,
        on_delete=models.CASCADE,
        related_name='menu_items',
        null=True,
        blank=True
    )
    title = models.CharField(_('Title'), max_length=100)
    icon_class = models.CharField(
        _('FontAwesome Icon Class'),
        max_length=50,
        help_text="Example: 'fas fa-user'"
    )
    url_name = models.CharField(
        _('Django URL name'),
        max_length=100,
        help_text="Django reverse() compatible url name"
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        null=True,
        blank=True
    )
    groups = models.ManyToManyField(
        Group,
        related_name='menu_items',
        blank=True,
        help_text="If empty — visible to all users"
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if '/' in self.url_name:
            return self.url_name
        try:
            return reverse(self.url_name)
        except NoReverseMatch:
            return '#'