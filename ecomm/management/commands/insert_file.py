# myapp/management/commands/insert_file_data.py
import os
from django.core.management.base import BaseCommand, CommandError
from ecomm.models import Product
import csv
import pandas as pd


class Command(BaseCommand):
    help = 'Inserts data from a text file into MyTextModel.'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str,
                            help='File path')

    def handle(self, *args, **options):
        csv_path = options['file_path']

        # Read CSV with pandas
        try:
            df = pd.read_csv(csv_path)
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"File not found: {csv_path}"))
            return

        # Ensure required columns exist
        required_columns = {'name', 'category', 'price', 'stock'}
        if not required_columns.issubset(df.columns):
            self.stderr.write(self.style.ERROR(
                f"CSV must have columns: {', '.join(required_columns)}"
            ))
            return

        # Convert DataFrame rows to Product objects
        products = [
            Product(
                name=row['name'],
                category=row['category'],
                price=row['price'],
                stock=row['stock']
            )
            for _, row in df.iterrows()
            ]

        # Bulk insert
        Product.objects.bulk_create(products, batch_size=1000)

        self.stdout.write(self.style.SUCCESS(
            f"✅ Successfully inserted {len(products)} products."
        ))
