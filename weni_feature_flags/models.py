from django.db import models
from django.utils.translation import gettext_lazy as _


class FeatureFlagsDefinitions(models.Model):
    """
    Model to store the feature flags definitions.
    """
    definitions = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Feature Flags Definitions")
        verbose_name_plural = _("Feature Flags Definitions")

    def __str__(self):
        return f"Feature Flags Definitions"