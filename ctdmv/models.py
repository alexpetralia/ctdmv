import re

from django_pandas.managers import DataFrameManager
from django.db import models

class WaitEntry(models.Model):
    """An individual wait time entry for a given branch"""
    branch = models.ForeignKey("Branch", on_delete=models.CASCADE)
    service = models.ForeignKey("Service", on_delete=models.CASCADE)
    wait_time_str = models.CharField(max_length=60, null=False, blank=False)
    wait_time_mins = models.IntegerField(null=False, blank=False)
    num_waiting = models.IntegerField(null=False, blank=False)
    creation_date_utc = models.DateTimeField(auto_now_add=True)

    objects = DataFrameManager()

    class Meta:
        unique_together = ('creation_date_utc', 'branch', 'service')
        ordering = ('-creation_date_utc', 'branch', 'service')

    @classmethod
    def extract_mins(cls, str_: str) -> int:
        """Converts string wait time to integer"""
        groups = re.search('(\d+) hour?. (\d+) minute?.', str_)
        if not groups:
            return 0
        return int(groups[1]) * 60 + int(groups[2])

    @classmethod
    def factory(cls, branch, service, wait_time_str, num_waiting):
        """Factory method to build related objects"""
        branch, _ = Branch.objects.get_or_create(name=branch)
        service, _ = Service.objects.get_or_create(name=service)
        wait_time_mins =  cls.extract_mins(wait_time_str)

        entry, _ = cls.objects.get_or_create(
            branch=branch,
            service=service,
            wait_time_str=wait_time_str,
            wait_time_mins=wait_time_mins,
            num_waiting=num_waiting,
        )
        return entry

    def __str__(self):
        return f"Wait time of {self.wait_time_str} for {self.service.name} \
                at {self.branch.name}, {self.creation_date_utc}"

class Branch(models.Model):
    name = models.CharField(max_length=60, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=60, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name
