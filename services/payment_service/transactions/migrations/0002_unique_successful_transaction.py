from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0001_initial"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="transaction",
            constraint=models.UniqueConstraint(
                fields=["order_id"],
                condition=models.Q(status="success"),
                name="transactions_unique_successful_txn",
            ),
        ),
    ]
