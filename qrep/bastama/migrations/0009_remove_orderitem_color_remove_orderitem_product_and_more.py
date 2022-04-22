# Generated by Django 4.0.3 on 2022-04-21 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bastama', '0008_size_size_code_alter_color_color_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='color',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='product',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='size',
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bastama.color')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bastama.product')),
                ('size', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bastama.size')),
            ],
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product_attr',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bastama.productattribute'),
            preserve_default=False,
        ),
    ]