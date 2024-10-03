from django.db import models

from config.settings import base

D_LENGTH = 20


class Description(models.Model):
    description = models.TextField(unique=True)

    def __str__(self):
        return self.description[:D_LENGTH] + (
            "..." if len(self.description) > D_LENGTH else ""
        )


class Breed(models.Model):
    breed = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.breed


class Color(models.Model):
    color = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.color


class Nickname(models.Model):
    nickname = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nickname


class Animal(models.Model):
    nickname = models.ForeignKey(Nickname, on_delete=models.CASCADE, unique=False)
    description = models.OneToOneField(Description, on_delete=models.CASCADE)
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, unique=False)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, unique=False)
    age = models.PositiveIntegerField(null=True, blank=True, unique=False)
    user = models.ForeignKey(
        base.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=False
    )

    class Meta:
        unique_together = ("user", "nickname")

    def __str__(self):
        return f"{self.nickname} ({self.breed}, {self.get_age_display()})"

    def get_age_display(self):
        if self.age is not None:
            years = self.age // 12
            months = self.age % 12
            return (
                f"{years} year(s) {months} month(s)" if years else f"{months} month(s)"
            )
        return "Unknown age"


class Rating(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    user = models.ForeignKey(base.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "animal")

    def __str__(self):
        return f"Rating {self.rating} for {self.animal}"
