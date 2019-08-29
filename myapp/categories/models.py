from django.db import models


class Category(models.Model):

    name = models.CharField(verbose_name='Name', max_length=50, unique=True)
    parents = models.ForeignKey(
        'self', blank=True, null=True ,related_name='children', on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
