from django.contrib import admin

from apps.products.models import Category, Option, OptionGroup, Product


@admin.register(Category)
class CagtegoryAdmin(admin.ModelAdmin):
    list_filter = ("cafe",)
    list_display = ("name", "cafe")


@admin.register(OptionGroup)
class OptionGroupAdmin(admin.ModelAdmin):
    list_filter = ("cafe",)
    list_display = ("name", "cafe")

    class OptionInline(admin.TabularInline):
        model = Option
        extra = 0

    inlines = [OptionInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "cafe")
