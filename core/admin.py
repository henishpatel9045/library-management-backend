from datetime import timedelta
from typing import Any
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django_object_actions import DjangoObjectActions
from django.db.transaction import atomic

from core import models
from core.filters import DueDateFilter, PenaltyAmountFilter
from core.forms import IssueAdminForm

admin.site.site_header = "Library Management System"

# Register your models here.
User = get_user_model()
MAX_ISSUE_PERIOD_STUDENT = 15
MAX_ISSUE_PERIOD_TEACHER = 30
PENALTY_AMOUNT_PER_DAY = 2


@admin.register(models.BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "barcode", "is_available"]
    search_fields = [
        "barcode",
    ]

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).prefetch_related("book")

    def title(self, obj):
        return obj.book.title


class BookCopyInline(admin.TabularInline):
    model = models.BookCopy
    min_num = 1
    extra = 0


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "issued",
        "available",
    )
    inlines = [
        BookCopyInline,
    ]
    search_fields = (
        "title",
        "author",
        "isbn",
    )

    def issued(self, obj):
        count = models.BookCopy.objects.filter(is_available=False).count()
        return count

    def available(self, obj):
        count = models.BookCopy.objects.filter(is_available=True).count()
        return count


@admin.register(models.Issue)
class IssueAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ["book_title", "username", "issue_date", "return_date", "is_late"]
    form = IssueAdminForm
    search_fields = [
        "book__book__title",
        "user__username",
        "book__barcode",
    ]
    actions = ["renew_action"]
    change_actions = ["renew", "return_book"]
    list_filter = [PenaltyAmountFilter, DueDateFilter]
    autocomplete_fields = (
        "book",
        "user",
    )

    def is_late(self, obj):
        return obj.penalty_amount != 0

    def renew(self, request, obj):
        new_due_date = timezone.now() + timedelta(days=15)
        obj.due_date = new_due_date
        obj.save()

        self.message_user(request, f"Due date updated to {new_due_date.date()}.")

    def return_book(self, request, obj):
        return_date = timezone.now().date()
        over_days = (return_date - obj.due_date).days
        penalty_amount = 0

        if over_days > 0:
            if not (
                obj.user.role.lower() == "teacher"
                and over_days <= MAX_ISSUE_PERIOD_TEACHER
            ):
                penalty_amount = over_days * PENALTY_AMOUNT_PER_DAY

        with atomic():
            obj.penalty_amount = penalty_amount
            obj.return_date = return_date
            obj.book.is_available = True
            obj.book.save()
            obj.save()

        self.message_user(request, f"Book returned successfully.")

    @admin.action(
        description="Renew the issue and update due date of selected records."
    )
    def renew_action(self, request, queryset):
        new_due_date = timezone.now() + timedelta(days=15)
        rows_updated = queryset.update(due_date=new_due_date)

        self.message_user(
            request, f"{rows_updated} issues updated to have a due date 15 days later."
        )

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        try:
            return super().save_model(request, obj, form, change)
        except Exception as e:
            return self.message_user(request, e.args[0], level="Error")


@admin.register(models.IssueRequest)
class IssueRequestAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "username",
        "book_title",
        "is_approved",
        "request_date",
    ]
