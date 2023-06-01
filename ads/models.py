from django.db import models
from categories.models import Category
from users.models import User


class Ad(models.Model):
    name = models.CharField(verbose_name='Объявление', max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/', max_length=5000, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
