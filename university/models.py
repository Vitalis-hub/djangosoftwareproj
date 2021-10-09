from django.db import models
from django.utils.translation import gettext_lazy as _


class Campus(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=400)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    PARK = 'park'
    DORM = 'dorm'
    CAFE = 'cafe'
    LECTURE_HAL = 'lecture_hall'
    MUSEUM = 'museum'

    CATEGORY_CHOICES = (
        (PARK, _('Park')),
        (DORM, _('Dorm')),
        (CAFE, _('Cafeteria')),
        (LECTURE_HAL, _('Lecture Hall')),
        (MUSEUM, _('Museum')),
    )

    name = models.CharField(max_length=150)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    address = models.CharField(max_length=400)
    description = models.CharField(max_length=600)
    image = models.ImageField(blank=True, null=True)
    category = models.CharField(
        max_length=32,
        choices=CATEGORY_CHOICES,
    )

    @property
    def default_entrance(self):
        entrances = Entrance.objects.filter(location=self)
        auto_entrances = entrances.filter(automatic_door=True)
        if auto_entrances.exists():
            return auto_entrances.first()
        elif entrances.exists():
            return entrances.first()
        return None

    @property
    def category_value(self):
        for t in self.CATEGORY_CHOICES:
            if self.category == t[0]:
                return t[1]

    @property
    def category_value(self):
        for t in self.CATEGORY_CHOICES:
            if self.category == t[0]:
                return t[1]

    def __str__(self):
        return f'{self.campus.name}: {self.name}'


class Entrance(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    address = models.CharField(max_length=400)
    orientation = models.CharField(max_length=150)
    image = models.ImageField(blank=True, null=True)
    automatic_door = models.BooleanField()
    default = models.BooleanField()
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    description = models.CharField(max_length=600, blank=True, null=True)

    def __str__(self):
        return f'{self.location.campus.name}: {self.location.name} ({self.orientation})'

    @property
    def direction_address(self):
        return f'{self.latitude},{self.longitude}' if self.longitude and self.longitude else self.address
