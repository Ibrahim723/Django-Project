# Generated by Django 4.2.9 on 2024-01-22 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('stocks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_id', models.AutoField(primary_key=True, serialize=False)),
                ('transaction_type', models.CharField(max_length=10)),
                ('transaction_volume', models.IntegerField()),
                ('transaction_price', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.stockdata')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
        ),
    ]