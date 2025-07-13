from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    source = models.URLField()
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title