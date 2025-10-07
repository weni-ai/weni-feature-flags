# Generated manually for Django library
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FeatureFlagsDefinitions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('definitions', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Feature Flags Definitions',
                'verbose_name_plural': 'Feature Flags Definitions',
            },
        ),
    ]
