from collections.abc import Iterable
from datetime import timedelta
from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


User = get_user_model()
MAX_ISSUE_PERIOD_STUDENT = 15
MAX_ISSUE_PERIOD_TEACHER = 30
PENALTY_AMOUNT_PER_DAY = 2


def upload_book(instance, fileName: str):
    return instance.author + "/" + fileName


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    image = models.ImageField(upload_to=upload_book, null=True, blank=True)

    def __str__(self) -> str:
        return self.title


class BookCopy(models.Model):
    barcode = models.CharField(max_length=20, unique=True, null=False, blank=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.barcode


class IssueRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-request_date"]

    def username(self):
        return self.user.username

    def book_title(self):
        return self.book.title

    def __str__(self) -> str:
        return self.user.username + ", " + self.book.title


class Issue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(BookCopy, on_delete=models.CASCADE, to_field="barcode")
    issue_date = models.DateField()
    due_date = models.DateField(blank=True)
    return_date = models.DateField(null=True, blank=True)
    penalty_amount = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0, "Penalty amount can't be negative.")],
    )

    class Meta:
        ordering = ["-issue_date", "-return_date"]

    def username(self):
        return self.user.username

    def book_title(self):
        return self.book.book.title

    def save(self) -> None:
        if self.pk is None:
            with transaction.atomic():
                if not self.book.is_available:
                    raise ValidationError(
                        f"Book with barcode {self.book.barcode} is already issued."
                    )
                self.book.is_available = False
                self.book.save()

                check_req = IssueRequest.objects.filter(
                    user=self.user, book=self.book.book
                )
                if check_req.exists():
                    check_req.update(is_approved=True)

                self.due_date = self.issue_date + timedelta(
                    days=(
                        MAX_ISSUE_PERIOD_TEACHER
                        if self.user.role.lower() == "teacher"
                        else MAX_ISSUE_PERIOD_STUDENT
                    )
                )
                return super().save()

        return super().save()

    def delete(self):
        with transaction.atomic():
            self.book.is_available = True
            self.book.save()
            return super().delete()

    def __str__(self) -> str:
        return self.user.username + ", " + self.book.book.title
