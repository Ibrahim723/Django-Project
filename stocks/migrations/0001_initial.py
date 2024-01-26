# Generated by Django 4.2.9 on 2024-01-19 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StockData',
            fields=[
                ('ticker', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('open_price', models.FloatField()),
                ('close_price', models.FloatField()),
                ('high', models.FloatField()),
                ('low', models.FloatField()),
                ('volume', models.IntegerField()),
                ('timestamp', models.DateTimeField()),
            ],
        ),
    ]