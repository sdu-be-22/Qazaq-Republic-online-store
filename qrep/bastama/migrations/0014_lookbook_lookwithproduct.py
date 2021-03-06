# Generated by Django 4.0.3 on 2022-05-06 04:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bastama', '0013_alter_productattribute_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='LookBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('look_image', models.ImageField(blank=True, upload_to='lookbook/%Y/%m/%d')),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='LookWithProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lookbook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bastama.lookbook')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bastama.product')),
            ],
        ),
    ]
