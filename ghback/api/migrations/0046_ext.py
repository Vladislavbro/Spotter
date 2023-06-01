from django.db import migrations
from django.contrib.postgres.operations import TrigramExtension


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0045_rename_profit_lost_productstat_profit_lost_fbo_and_more'),
    ]

    operations = [
        TrigramExtension(),
    ]