from django.contrib import admin
from django.utils import timezone
from .models import Server, AdoptionApplication

admin.site.site_header = "Server Adoption Agency — Staff Portal"
admin.site.site_title = "SAA Staff"
admin.site.index_title = "Shelter Management"


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ["name", "species", "size", "age_years", "status", "is_featured"]
    list_filter = ["status", "species", "size", "is_featured"]
    search_fields = ["name", "backstory"]
    prepopulated_fields = {"slug": ["name"]}
    readonly_fields = ["portrait_preview"]
    actions = ["mark_available", "mark_on_hold", "mark_adopted"]

    def portrait_preview(self, obj):
        if obj.portrait:
            from django.utils.html import format_html

            return format_html(
                '<img src="{}" style="max-height:200px">', obj.portrait.url
            )
        return "(no portrait)"

    @admin.action(description="Mark selected servers as Available")
    def mark_available(self, request, queryset):
        queryset.update(status=Server.Status.AVAILABLE)

    @admin.action(description="Mark selected servers as On Hold")
    def mark_on_hold(self, request, queryset):
        queryset.update(status=Server.Status.ON_HOLD)

    @admin.action(description="Mark selected servers as Adopted")
    def mark_adopted(self, request, queryset):
        queryset.update(status=Server.Status.ADOPTED)


@admin.register(AdoptionApplication)
class AdoptionApplicationAdmin(admin.ModelAdmin):
    list_display = ["applicant_name", "server", "review_status", "created_at"]
    list_filter = ["review_status", "server"]
    search_fields = ["applicant_name", "applicant_email"]
    readonly_fields = [
        "id",
        "created_at",
        "reviewed_at",
        "server",
        "applicant_name",
        "applicant_email",
        "applicant_location",
        "decibel_tolerance",
        "why_this_server",
    ]
    actions = ["approve_selected", "decline_selected"]

    @admin.action(description="Approve selected applications")
    def approve_selected(self, request, queryset):
        for application in queryset.filter(
            review_status=AdoptionApplication.ReviewStatus.PENDING
        ):
            application.review_status = AdoptionApplication.ReviewStatus.APPROVED
            application.reviewed_at = timezone.now()
            application.save()

            server = application.server
            server.status = Server.Status.ADOPTED
            server.adopted_by_name = application.applicant_name
            server.adopted_on = timezone.localdate()
            server.save()

        self.message_user(
            request, "Applications approved and servers marked as adopted."
        )

    @admin.action(description="Decline selected applications")
    def decline_selected(self, request, queryset):
        queryset.filter(review_status=AdoptionApplication.ReviewStatus.PENDING).update(
            review_status=AdoptionApplication.ReviewStatus.DECLINED,
            reviewed_at=timezone.now(),
        )
