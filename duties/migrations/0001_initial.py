# Generated by Django 3.0.3 on 2020-03-20 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DutyDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DutyPerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('local_phone', models.CharField(blank=True, max_length=50, null=True)),
                ('mobile_phone', models.CharField(blank=True, max_length=50, null=True)),
                ('duties', models.ManyToManyField(to='duties.DutyDate')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='duties.Group')),
            ],
            options={
                'ordering': ['last_name'],
            },
        ),
    ]
