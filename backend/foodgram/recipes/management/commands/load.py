import os
import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Tag

Tags_data = (
    {'name': 'Завтрак', 'color': '#E26C2D', 'slug': 'breakfast'},
    {'name': 'Обед', 'color': '#49B64E', 'slug': 'lunch'},
    {'name': 'Ужин', 'color': '#8775D2', 'slug': 'dinner'},
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        user_dir = os.path.expanduser('~')
        path = os.path.join(
            user_dir,
            'Dev', 'foodgram-project-react', 'data', 'ingredients.csv'
        )
        print('File path: ', path)

        with open(path) as f:
            reader = csv.reader(f)
            for row in reader:
                _, created = Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1]
                )

        for tag_data in Tags_data:
            _, created = Tag.objects.get_or_create(
                name=tag_data['name'],
                color=tag_data['color'],
                slug=tag_data['slug'],
            )

        return print('Загрузка данных Ingredient и Tag готова!')
