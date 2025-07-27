from django.db import models
from django.conf import settings


class CommonModels(models.Model):
    created_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created_by"
    )
    updated_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    order = models.CharField(max_length=100, null=True, blank=True)
    display_order = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ["display_order", "order", "-created_at"]

    def __str__(self):
        return f"{self.__class__.__name__} (ID: {self.id})"
