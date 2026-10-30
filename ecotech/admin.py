from django.contrib import admin

from .models import ContactMessage, Department, Employee, Project, ProjectAssignment, WorkLog


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'created_at')
	list_filter = ('created_at',)
	search_fields = ('name', 'email', 'message')
	readonly_fields = ('created_at',)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
	search_fields = ('name',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'department', 'role', 'is_active')
	list_filter = ('department', 'role', 'is_active')
	search_fields = ('name', 'email')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
	list_display = ('name', 'status', 'start_date', 'end_date')
	list_filter = ('status',)
	search_fields = ('name', 'description')


@admin.register(ProjectAssignment)
class ProjectAssignmentAdmin(admin.ModelAdmin):
	list_display = ('employee', 'project', 'assigned_at')
	list_filter = ('project',)
	search_fields = ('employee__name', 'project__name')


@admin.register(WorkLog)
class WorkLogAdmin(admin.ModelAdmin):
	list_display = ('date', 'employee', 'project', 'activity', 'hours')
	list_filter = ('project', 'employee', 'date')
	search_fields = ('employee__name', 'project__name', 'activity')
from django.contrib import admin

# Register your models here.
