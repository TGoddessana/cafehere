# Generated by Django 3.2.20 on 2023-09-01 20:38

import datetime
import uuid

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):
    replaces = [
        ("products", "0001_initial"),
        ("products", "0002_auto_20230902_0220"),
        ("products", "0003_auto_20230902_0237"),
        ("products", "0004_rename_producttype_product"),
        ("products", "0005_auto_20230902_0247"),
        ("products", "0006_auto_20230902_0537"),
    ]

    dependencies = [
        ("cafes", "0002_cafe_unique_cafe_name_per_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=30)),
                (
                    "cafe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="categories",
                        to="cafes.cafe",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OptionGroup",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name="ProductType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "uuid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("name", models.CharField(max_length=30)),
                ("description", models.TextField()),
                (
                    "cost",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
                (
                    "price",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.category",
                    ),
                ),
                (
                    "option_groups",
                    models.ManyToManyField(blank=True, to="products.OptionGroup"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "uuid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("expireation_date", models.DateTimeField()),
                (
                    "product_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.producttype",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Option",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=30)),
                (
                    "add_price",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
                (
                    "option_group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.optiongroup",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="producttype",
            constraint=models.UniqueConstraint(
                fields=("name", "category"), name="unique_product_type_per_category"
            ),
        ),
        migrations.AddConstraint(
            model_name="option",
            constraint=models.UniqueConstraint(
                fields=("name", "option_group"), name="unique_option_per_option_group"
            ),
        ),
        migrations.AddConstraint(
            model_name="category",
            constraint=models.UniqueConstraint(
                fields=("name", "cafe"), name="unique_category_per_cafe"
            ),
        ),
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name_plural": "categories"},
        ),
        migrations.AddField(
            model_name="optiongroup",
            name="cafe",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="option_groups",
                to="cafes.cafe",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="producttype",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product_types",
                to="products.category",
            ),
        ),
        migrations.AddField(
            model_name="producttype",
            name="expireation_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 9, 1, 17, 37, 32, 159308, tzinfo=utc)
            ),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name="Product",
        ),
        migrations.RenameModel(
            old_name="ProductType",
            new_name="Product",
        ),
        migrations.RemoveField(
            model_name="product",
            name="created",
        ),
        migrations.RemoveField(
            model_name="product",
            name="modified",
        ),
        migrations.RemoveConstraint(
            model_name="product",
            name="unique_product_type_per_category",
        ),
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="products",
                to="products.category",
            ),
        ),
        migrations.AddConstraint(
            model_name="optiongroup",
            constraint=models.UniqueConstraint(
                fields=("name", "cafe"), name="unique_option_group_per_cafe"
            ),
        ),
        migrations.AddConstraint(
            model_name="product",
            constraint=models.UniqueConstraint(
                fields=("name", "category"), name="unique_product_per_category"
            ),
        ),
    ]