from django.db import models

# Product (ID, NameEn, NameAr, UnitPrice, StockQuantity, CategoryID)


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    nameEn = models.CharField(max_length=200)
    nameAr = models.CharField(max_length=200)
    unitPrice = models.DecimalField(max_digits=10, decimal_places=2)
    stockQuantity = models.IntegerField()
    categoryId = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.pk)
