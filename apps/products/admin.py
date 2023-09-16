from django.contrib import admin

from apps.products.models import Category, Option, OptionGroup, Product


@admin.register(Category)
class CagtegoryAdmin(admin.ModelAdmin):
    list_filter = ("cafe",)
    list_display = ("name", "uuid", "cafe")


@admin.register(OptionGroup)
class OptionGroupAdmin(admin.ModelAdmin):
    list_filter = ("cafe",)
    list_display = ("name", "uuid", "cafe")

    class OptionInline(admin.TabularInline):
        model = Option
        extra = 0

    inlines = [OptionInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "initial_consonant", "cafe")
