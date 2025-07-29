from django.contrib import admin
from student.models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'get_full_name', 'get_email')
    search_fields = ('user__full_name', 'user__email', 'student_id')
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
