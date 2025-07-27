from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import CommonModels, CustomUser

PROGRAM_CHOICES = [
    ("CSE_BSC", "B.Sc Engg in CSE"),
    ("EEE_BSC", "B.Sc Engg in EEE"),
    ("CIVIL_BSC", "B.Sc Engg in Civil"),
    ("ENG_BA", "BA in English"),
    ("BBA", "Bachelor of Business Administration"),
]

PROGRAM_NUMERIC_CODE = {
    "CSE_BSC": "101",
    "EEE_BSC": "102",
    "CIVIL_BSC": "103",
    "ENG_BA": "104",
    "BBA": "105",
}


class Student(CommonModels):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="students",
    )
    student_id = models.CharField(
        max_length=50, unique=True, blank=True, null=True
    )
    date_of_birth = models.DateField(null=True, blank=True)
    program = models.CharField(
        max_length=50, choices=PROGRAM_CHOICES, null=True, blank=True
    )
    intake = models.CharField(max_length=50, null=True, blank=True)
    blood_group = models.CharField(
        max_length=3,
        choices=[
            ("A+", "A+"), ("A-", "A-"),
            ("B+", "B+"), ("B-", "B-"),
            ("AB+", "AB+"), ("AB-", "AB-"),
            ("O+", "O+"), ("O-", "O-")
        ],
        null=True,
        blank=True
    )

    def __str__(self):
        return self.student_id or "No ID"


@receiver(post_save, sender=Student)
def generate_student_id(sender, instance, created, **kwargs):
    if created and not instance.student_id and instance.program:
        year = timezone.now().year
        program_code = PROGRAM_NUMERIC_CODE.get(instance.program, "000")

        prefix = f"{year}{program_code}"
        last_student = Student.objects.filter(
            student_id__startswith=prefix
        ).order_by('-student_id').first()

        if last_student:
            last_serial_str = last_student.student_id[len(prefix):]
            if last_serial_str.isdigit():
                last_serial = int(last_serial_str)
            else:
                last_serial = 0
        else:
            last_serial = 0

        new_serial = last_serial + 1
        serial_str = str(new_serial).zfill(4)

        instance.student_id = f"{prefix}{serial_str}"
        instance.save(update_fields=['student_id'])
