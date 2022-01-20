# Generated by Django 3.2.8 on 2021-12-29 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_character'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('display_name', models.CharField(max_length=64)),
                ('id', models.CharField(max_length=3, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=64)),
                ('ordering', models.IntegerField()),
                ('role', models.CharField(choices=[('tank', 'tank'), ('heal', 'heal'), ('dps', 'dps')], max_length=4)),
            ],
            options={
                'ordering': ['-role', 'ordering'],
            },
        ),
    ]
