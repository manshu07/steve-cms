# Generated migration for header_buttons_json field

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('marketing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='navmenu',
            name='header_buttons_json',
            field=models.JSONField(blank=True, help_text='Array of button objects with label, url, style, and open_new_tab', null=True),
        ),
    ]
