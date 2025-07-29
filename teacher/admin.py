from django.contrib import admin
from teacher.models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher_id', 'get_full_name', 'get_email')
    search_fields = ('user__full_name', 'user__email', 'teacher_id')
    list_filter = ('created_at', 'user__email')
    ordering = ('-created_at',)

    def get_full_name(self, obj):
        return obj.user.full_name
    get_full_name.short_description = 'Full Name'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

    def has_add_permission(self, request):
        return False
