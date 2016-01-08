def mark_attendance(modeladmin, request, queryset):
    queryset.update(attended='true')

