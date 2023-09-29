# Generated by Django 3.2 on 2023-09-29 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(related_name='titles', through='reviews.TitleGenre', to='reviews.Genre', verbose_name='Жанр произведения'),
        ),
        migrations.AlterField(
            model_name='title',
            name='name',
            field=models.TextField(help_text='Укажите название произведения', max_length=256, verbose_name='Название произведения'),
        ),
    ]