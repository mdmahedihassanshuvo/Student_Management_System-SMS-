# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import Group
# from core.models import CustomUser
# from member.models import Member


# @receiver(post_save, sender=CustomUser)
# def create_member_profile(sender, instance, created, **kwargs):
#     if created:
#         # Create Member profile
#         Member.objects.create(
#             user=instance,
#             name=instance.full_name
#         )

#         # Assign 'member' group permission
#         try:
#             member_group, created = Group.objects.get_or_create(name='member')
#             instance.groups.add(member_group)
#         except Exception as e:
#             print(f"Error assigning member group: {e}")