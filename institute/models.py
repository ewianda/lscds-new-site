from django.db import models


class University(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class Degree(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class Faculty(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


