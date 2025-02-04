from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.timezone import now


class Todo(models.Model):
    """
        Needed fields
        - user (fk to User Model - Use AUTH_USER_MODEL from django.conf.settings)
        - name (max_length=1000)
        - done (boolean with default been false)
        - date_created (with default of creation time)
        - date_completed (set it when done is marked true)

        Add string representation for this model with todos name.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    done = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=now)
    date_completed = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.done and self.date_completed is None:
            self.date_completed = now()
        elif not self.done:
            self.date_completed = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    