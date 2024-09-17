import uuid
from django.db import models
from django.utils import timezone


class UuidMixin(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    class Meta:
        abstract = True


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class NameMixin(models.Model):
    name = models.CharField(max_length=255, blank=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class DescriptionMixin(models.Model):
    description = models.TextField(blank=True, default="")

    class Meta:
        abstract = True


class BaseMixin(UuidMixin, TimestampMixin):
    class Meta:
        abstract = True


class StatusManager(models.Manager):
    def active(self):
        return self.filter(status=StatusMixin.Status.ACTIVE)

    def inactive(self):
        return self.filter(status=StatusMixin.Status.INACTIVE)


class StatusMixin(models.Model):
    class Status:
        INACTIVE = 0
        ACTIVE = 1

        choices = ((ACTIVE, "active"), (INACTIVE, "inactive"))

    status = models.PositiveIntegerField(choices=Status.choices, default=Status.ACTIVE)

    @property
    def is_active(self) -> bool:
        return self.status == self.Status.ACTIVE

    def activate(self, save=True, *args, **kwargs) -> int:
        if not self.is_active:
            self.status = self.Status.ACTIVE
            if save:
                self.save(update_fields=["status"])
        return self.status

    def deactivate(self, save=True, *args, **kwargs) -> int:
        if not self.is_active:
            return self.status

        self.status = self.Status.INACTIVE
        if save:
            self.save(update_fields=["status"])
        return self.status

    class Meta:
        abstract = True


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def deleted(self):
        return super().get_queryset().filter(is_deleted=True)


class SoftDeleteMixin(models.Model):

    is_deleted = models.BooleanField(default=False)

    def delete(self, force_delete=False, **kwargs):

        if force_delete:
            return super().delete(**kwargs)
        if not self.is_deleted:
            self.is_deleted = True
            self.save(update_fields=["is_deleted"])
        return self.is_deleted

    def restore(self):

        if self.is_deleted:
            self.is_deleted = False
            self.save(update_fields=["is_deleted"])
        return self.is_deleted

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True
