# Generated by Django 3.2.10 on 2022-01-11 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_fix_team_ordering'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('greed', models.BooleanField(default=False)),
                ('item', models.TextField()),
                ('obtained', models.DateField(auto_now_add=True)),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.teammember')),
                ('tier', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.tier')),
            ],
            options={
                'ordering': ['-obtained'],
            },
        ),
    ]
