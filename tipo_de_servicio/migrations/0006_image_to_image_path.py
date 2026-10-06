from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tipo_de_servicio', '0005_alter_typeofservice_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='typeofservice',
            name='image',
        ),
        migrations.AddField(
            model_name='typeofservice',
            name='image_path',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]