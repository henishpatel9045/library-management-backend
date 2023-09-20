from typing import Any
from django.contrib.admin.filters import SimpleListFilter
from django.db.models.query import QuerySet
from django.utils import timezone


class PenaltyAmountFilter(SimpleListFilter):
    title = "Penalty"
    parameter_name = "penalty_amount"

    def lookups(self, request, model_admin):
        return (
            (">0", "Penalty."),
            ("=0", "No Penalty"),
        )

    def queryset(self, request, queryset):
        if self.value() == ">0":
            return queryset.filter(penalty_amount__gt=0)
        elif self.value() == "=0":
            return queryset.filter(penalty_amount=0)


class DueDateFilter(SimpleListFilter):
    title = "Due Date filter"
    parameter_name = "due_date"

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return (
            # ("all", "All"),
            ("<0", "Past Due date"),
            ("=0", "Last date"),
        )

    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == "=0":
            return queryset.filter(due_date=timezone.now().date())
        if self.value() == "<0":
            return queryset.filter(due_date__lt=timezone.now().date())
        return queryset
