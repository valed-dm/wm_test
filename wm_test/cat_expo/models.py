"""Models module for cat_expo app."""

from django.db import models

from config.settings import base

D_LENGTH = 20


class Description(models.Model):
    """
    Model representing a unique description for a kitten.
    Each description is stored as a TextField and must be unique.
    """

    description = models.TextField(unique=True)

    def __str__(self) -> str:
        """
        Returns a truncated version of the description if it's longer than D_LENGTH.
        """
        return self.description[:D_LENGTH] + (
            "..." if len(self.description) > D_LENGTH else ""
        )


class Breed(models.Model):
    """
    Model representing the breed of a kitten.
    The breed is stored as a unique CharField with a maximum length of 255 characters.
    """

    breed = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        """
        Returns the string representation of the breed.
        """
        return self.breed


class Color(models.Model):
    """
    Model representing the color of a kitten.
    The color is stored as a unique CharField with a maximum length of 255 characters.
    """

    color = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        """
        Returns the string representation of the color.
        """
        return self.color


class Nickname(models.Model):
    """
    Model representing the nickname of a kitten.
    Each nickname is stored as a unique CharField with a maximum length of
    255 characters.
    """

    nickname = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        """
        Returns the string representation of the nickname.
        """
        return self.nickname


class Kitten(models.Model):
    """
    Model representing a kitten.
    A kitten has a nickname, description, breed, color, and age, and is linked
    to a user. The combination of user and nickname must be unique.
    """

    nickname = models.ForeignKey(Nickname, on_delete=models.CASCADE, unique=False)
    description = models.OneToOneField(Description, on_delete=models.CASCADE)
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, unique=False)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, unique=False)
    age = models.PositiveIntegerField(null=True, blank=True, unique=False)
    user = models.ForeignKey(
        base.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=False
    )

    class Meta:
        """
        Ensures that a user cannot have two kittens with the same nickname.
        """

        unique_together = ("user", "nickname")

    def __str__(self) -> str:
        """
        Returns the string representation of the kitten, including its nickname, breed,
        and age in years and months.
        """
        return f"{self.nickname} ({self.breed}, {self.get_age_display()})"

    def get_age_display(self) -> str:
        """
        Returns the age of the kitten in a human-readable format (years and months),
        or 'Unknown age' if the age is not specified.
        """
        if self.age is not None:
            years = self.age // 12
            months = self.age % 12
            return (
                f"{years} year(s) {months} month(s)" if years else f"{months} month(s)"
            )
        return "Unknown age"


class Rating(models.Model):
    """
    Model representing a rating given to a kitten by a user.
    Ratings are on a scale of 1 to 5, and each user can only rate a kitten once.
    """

    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    kitten = models.ForeignKey(Kitten, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    user = models.ForeignKey(base.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        """
        Ensures that a user cannot rate the same kitten more than once.
        """

        unique_together = ("user", "kitten")

    def __str__(self) -> str:
        """
        Returns a string representation of the rating, including the rating value
        and the associated kitten.
        """
        return f"Rating {self.rating} for {self.kitten}"
