from django.db import migrations, models


class Migration(migrations.Migration):

	initial = True

	dependencies = []

	operations = [
		migrations.CreateModel(
			name='ContactMessage',
			fields=[
				('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('name', models.CharField(max_length=100, verbose_name='nombre')),
				('email', models.EmailField(max_length=254, verbose_name='correo electrónico')),
				('message', models.TextField(max_length=2000, verbose_name='mensaje')),
				('created_at', models.DateTimeField(auto_now_add=True, verbose_name='recibido el')),
			],
			options={
				'verbose_name': 'solicitud de contacto',
				'verbose_name_plural': 'solicitudes de contacto',
				'ordering': ['-created_at'],
			},
		),
	]