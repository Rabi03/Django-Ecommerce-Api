# Generated by Django 4.0.5 on 2022-07-04 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_alter_customer_options_remove_customer_email_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': [('cancel_order', 'Can cancel order')]},
        ),
    ]
