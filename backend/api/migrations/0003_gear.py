# Generated by Django 3.2.8 on 2021-12-29 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_jobs'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_accessories', models.BooleanField(default=False)),
                ('has_armour', models.BooleanField(default=False)),
                ('has_weapon', models.BooleanField(default=False)),
                ('item_level', models.IntegerField()),
                ('name', models.TextField()),
            ],
            options={
                'ordering': ['-item_level', '-id'],
                'unique_together': {('name', 'item_level')},
            },
        ),
    ]
