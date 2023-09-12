from typing import Any

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import AdminProfile, Cart, CartItem, CustomerProfile, User

admin.site.unregister(Group)


class CustomerProxy(User):
    class Meta:
        verbose_name_plural = "CustomerUser"
        proxy = True


class AdminProxy(User):
    class Meta:
        verbose_name_plural = "Admin Users"
        proxy = True


class AdminInline(admin.StackedInline):
    model = AdminProfile
    can_delete = False
    verbose_name_plural = "Admin Profile"
    fk_name = "user"
    max_num = 1
    min_num = 1


class CustomerInline(admin.StackedInline):
    model = CustomerProfile
    can_delete = False
    verbose_name_plural = "Customer Profile"
    fk_name = "user"
    max_num = 1
    min_num = 1


@admin.register(CustomerProxy)
class Customers(admin.ModelAdmin):
    inlines = [CustomerInline]
    verbose_name = "Customer"
    list_display = (
        "email",
        "fullName",
        "getCustomerUserPhone",
        "getCustomerUserAddress",
    )
    fields = ("email", "password", "fullName")
    fieldsets = ()

    def save_model(self, request, obj, form, change):
        obj.set_password(obj.password)
        super().save_model(request, obj, form, change)
        Cart.objects.create(customer=obj).save()

    def getCustomerUserPhone(self, obj):
        return obj.customerProfile.phone

    getCustomerUserPhone.short_description = "Phone"

    def getCustomerUserAddress(self, obj):
        return obj.customerProfile.address

    getCustomerUserPhone.short_description = "Phone"

    def get_queryset(self, request):
        qs = super(Customers, self).get_queryset(request)
        return qs.filter(is_superuser=False)


@admin.register(AdminProxy)
class Admins(admin.ModelAdmin):
    inlines = [AdminInline]
    fields = ("email", "password", "fullName")
    verbose_name = "Admins"
    fieldsets = ()
    list_display = (
        "email",
        "fullName",
        "getAdminProfileJobTitle",
        "getAdminProfileHireDate",
    )

    def save_model(self, request, obj, form, change):
        obj.is_superuser = True
        obj.is_staff = True
        obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

    def getAdminProfileJobTitle(self, obj):
        return obj.adminProfile.jobTitle

    getAdminProfileJobTitle.short_description = "Job Title"

    def getAdminProfileHireDate(self, obj):
        return obj.adminProfile.hireDate

    getAdminProfileHireDate.short_description = "Hire Date"

    def get_queryset(self, request):
        qs = super(Admins, self).get_queryset(request)
        return qs.filter(is_superuser=True)


admin.site.register(CartItem)
