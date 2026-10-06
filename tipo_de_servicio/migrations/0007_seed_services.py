from django.db import migrations

SERVICES = [
    ('Básquet', 'services/basquet.png'),
    ('Frontón', 'services/fronton.jpg'),
    ('Fútbol', 'services/futbol.png'),
    ('Futsal', 'services/futsal.png'),
    ('Tenis', 'services/tennis.jpg'),
    ('Wallyball', 'services/wally.png'),
]


def seed_services(apps, schema_editor):
    TypeOfService = apps.get_model('tipo_de_servicio', 'TypeOfService')
    for name, image_path in SERVICES:
        TypeOfService.objects.get_or_create(
            name=name,
            defaults={
                'image_path': image_path,
                'price_per_hour': '30.00',
                'with_roof': False,
            },
        )


def reverse_seed_services(apps, schema_editor):
    TypeOfService = apps.get_model('tipo_de_servicio', 'TypeOfService')
    names = [name for name, _ in SERVICES]
    TypeOfService.objects.filter(name__in=names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tipo_de_servicio', '0006_image_to_image_path'),
    ]

    operations = [
        migrations.RunPython(seed_services, reverse_seed_services),
    ]