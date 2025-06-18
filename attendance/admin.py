from django.contrib import admin
from .models import Attendance


# Register your models here.
# admin.site.register(Attendance)
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'status', 'date', 'formatted_check_in', 'formatted_check_out', 'worked_hours', 'remarks')
    readonly_fields = ('worked_hours',)

    def check_in_formatted(self, obj):
        if obj.check_in:
            return obj.check_in.strftime('%I:%M %p')  # e.g., 04:07 PM
        return '-'
    check_in_formatted.short_description = 'Check In'

    def check_out_formatted(self, obj):
        if obj.check_out:
            return obj.check_out.strftime('%I:%M %p')  # e.g., 04:07 PM
        return '-'
    check_out_formatted.short_description = 'Check Out'

    def worked_hours_formatted(self, obj):
        if obj.worked_hours:
            total_seconds = int(obj.worked_hours.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"{hours:02d}:{minutes:02d} hrs"
        return '-'
    worked_hours_formatted.short_description = 'Worked Hours'
