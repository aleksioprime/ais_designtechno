from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from sumassess.models import Unit

# @receiver(m2m_changed, sender=Unit.objective.through)
# def objective_added(instance, action, **kwargs):
#     if action == "post_add" or "post_remove":
#         pass