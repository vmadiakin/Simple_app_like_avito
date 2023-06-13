from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models
from categories.models import Category
from users.models import User


class Ad(models.Model):
    name = models.CharField(null=False, max_length=255, validators=[MinLengthValidator(10)])
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    description = models.TextField(null=True)
    is_published = models.BooleanField(default=False, editable=False)
    image = models.ImageField(upload_to='images/', max_length=5000, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
