# Generated by Django 3.2.8 on 2022-01-11 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_loot_helper'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teammember',
            options={'ordering': ['-bis_list__job__role', 'bis_list__job__ordering']},
        ),
    ]
