from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError


class ContactMessage(models.Model):
	name = models.CharField('nombre', max_length=100)
	email = models.EmailField('correo electrónico')
	message = models.TextField('mensaje', max_length=2000)
	created_at = models.DateTimeField('recibido el', auto_now_add=True)

	class Meta:
		ordering = ['-created_at']
		verbose_name = 'solicitud de contacto'
		verbose_name_plural = 'solicitudes de contacto'

	def __str__(self):
		return f'{self.name} - {self.email}'


class Department(models.Model):
	name = models.CharField('nombre', max_length=100, unique=True)

	class Meta:
		ordering = ['name']
		verbose_name = 'departamento'
		verbose_name_plural = 'departamentos'

	def __str__(self):
		return self.name


class Employee(models.Model):
	ROLE_CHOICES = [
		('admin', 'Administrador'),
		('manager', 'Líder de proyecto'),
		('employee', 'Empleado'),
	]
	user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='employee_profile')
	name = models.CharField('nombre completo', max_length=150)
	email = models.EmailField('correo electrónico', unique=True)
	department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='employees')
	role = models.CharField('rol', max_length=20, choices=ROLE_CHOICES, default='employee')
	is_active = models.BooleanField('activo', default=True)

	class Meta:
		ordering = ['name']
		verbose_name = 'empleado'
		verbose_name_plural = 'empleados'

	def __str__(self):
		return self.name


class Project(models.Model):
	STATUS_CHOICES = [('planning', 'Planificación'), ('active', 'Activo'), ('done', 'Finalizado')]
	name = models.CharField('nombre', max_length=150)
	description = models.TextField('descripción', blank=True)
	status = models.CharField('estado', max_length=20, choices=STATUS_CHOICES, default='planning')
	start_date = models.DateField('fecha de inicio', null=True, blank=True)
	end_date = models.DateField('fecha de finalización', null=True, blank=True)

	class Meta:
		ordering = ['-start_date', 'name']
		verbose_name = 'proyecto'
		verbose_name_plural = 'proyectos'

	def __str__(self):
		return self.name


class ProjectAssignment(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='assignments')
	project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='assignments')	
	assigned_at = models.DateField('asignado el', auto_now_add=True)

	class Meta:
		constraints = [models.UniqueConstraint(fields=['employee', 'project'], name='unique_employee_project')]
		verbose_name = 'asignación de proyecto'
		verbose_name_plural = 'asignaciones de proyectos'

	def __str__(self):
		return f'{self.employee} - {self.project}'


class WorkLog(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='work_logs')
	project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='work_logs')
	activity = models.CharField('actividad', max_length=150)
	date = models.DateField('fecha')
	hours = models.DecimalField('horas', max_digits=5, decimal_places=2)
	notes = models.TextField('notas', blank=True)

	class Meta:
		ordering = ['-date', '-id']
		constraints = [models.UniqueConstraint(fields=['employee', 'project', 'activity', 'date'], name='unique_work_log')]
		verbose_name = 'registro de horas'
		verbose_name_plural = 'registros de horas'

	def clean(self):
		if self.hours is not None and (self.hours <= 0 or self.hours > 24):
			raise ValidationError({'hours': 'Las horas deben estar entre 0.01 y 24.'})
		if self.employee_id and self.project_id and not ProjectAssignment.objects.filter(employee_id=self.employee_id, project_id=self.project_id).exists():
			raise ValidationError('El empleado debe estar asignado al proyecto antes de registrar horas.')

	def __str__(self):
		return f'{self.employee} - {self.project} - {self.date}'
