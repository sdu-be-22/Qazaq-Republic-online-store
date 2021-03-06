# Generated by Django 4.0.3 on 2022-05-04 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bastama', '0011_productattribute_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productattribute',
            name='size',
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bastama.size'),
        ),
    ]
