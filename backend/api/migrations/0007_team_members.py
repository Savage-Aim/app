# Generated by Django 3.2.10 on 2022-01-10 01:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_team'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lead', models.BooleanField(default=False)),
                ('bis_list', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.bislist')),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.character')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='api.team')),
            ],
            options={
                'ordering': ['-bis_list__job__role', '-bis_list__job__ordering'],
                'unique_together': {('character', 'team')},
            },
        ),
    ]
