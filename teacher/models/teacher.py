from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from core.models import CommonModels, CustomUser


DEPARTMENT_CHOICES = [
    ("CSE", _("Computer Science & Engineering")),
    ("EEE", _("Electrical & Electronic Engineering")),
    ("CIVIL", _("Civil Engineering")),
    ("ENG", _("English")),
    ("BBA", _("Business Administration")),
]

DESIGNATION_CHOICES = [
    ("PROF", _("Professor")),
    ("ASSOC_PROF", _("Associate Professor")),
    ("ASST_PROF", _("Assistant Professor")),
    ("LECT", _("Lecturer")),
    ("TUTOR", _("Tutor")),
]

BLOOD_GROUP_CHOICES = [
    ("A+", _("A+")), ("A-", _("A-")),
    ("B+", _("B+")), ("B-", _("B-")),
    ("AB+", _("AB+")), ("AB-", _("AB-")),
    ("O+", _("O+")), ("O-", _("O-")),
]

DEPARTMENT_CODE = {
    "CSE": "101",
    "EEE": "102",
    "CIVIL": "103",
    "ENG": "104",
    "BBA": "105",
}


class Teacher(CommonModels):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="teachers",
    )
    teacher_id = models.CharField(
        max_length=50, unique=True, blank=True, null=True
    )
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    designation = models.CharField(max_length=50, choices=DESIGNATION_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    blood_group = models.CharField(
        max_length=3, choices=BLOOD_GROUP_CHOICES, null=True, blank=True
    )
    contact_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.teacher_id or 'No ID'}"


@receiver(post_save, sender=Teacher)
def generate_teacher_id(sender, instance, created, **kwargs):
    if created and not instance.teacher_id and instance.department:
        year = timezone.now().year
        dept_code = DEPARTMENT_CODE.get(instance.department, "000")
        prefix = f"{year}{dept_code}"

        last_teacher = Teacher.objects.filter(
            teacher_id__startswith=prefix
        ).order_by('-teacher_id').first()

        if last_teacher:
            last_serial_str = last_teacher.teacher_id[len(prefix):]
            last_serial = int(
                last_serial_str
            ) if last_serial_str.isdigit() else 0
        else:
            last_serial = 0

        new_serial = last_serial + 1
        serial_str = str(new_serial).zfill(4)
        instance.teacher_id = f"{prefix}{serial_str}"
        instance.save(update_fields=["teacher_id"])
