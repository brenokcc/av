# Generated by Django 4.1 on 2023-06-05 11:35

from django.db import migrations
import django.db.models.deletion
import sloth.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('av', '0003_cor_fabricante_marca'),
    ]

    operations = [
        migrations.AddField(
            model_name='validacao',
            name='chassi',
            field=sloth.db.models.CharField(max_length=255, null=True, verbose_name='Chassi'),
        ),
        migrations.AddField(
            model_name='validacao',
            name='cor',
            field=sloth.db.models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='av.cor', verbose_name='Cor'),
        ),
        migrations.AddField(
            model_name='validacao',
            name='marca',
            field=sloth.db.models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='av.marca', verbose_name='Marca'),
        ),
    ]
