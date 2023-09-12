from django.contrib import admin

from .models import Category, Product

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ("nameEn", "nameAr", "unitPrice", "stockQuantity", "categoryId")
    list_display = (
        "nameEn",
        "nameAr",
        "unitPrice",
        "stockQuantity",
        "get_category",
    )

    def get_category(self, obj):
        return obj.categoryId.name

    get_category.short_description = "Category"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ("name",)
    list_display = ("name",)
