from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from reviews.models import Categories, Comment, Genres, Review, Title
from reviews.validators import validate_year
from users.validators import UsernameValidator

User = get_user_model()


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=settings.EMAIL_MAX_LENGTH,
        required=True,
    )
    username = serializers.CharField(
        max_length=settings.USERNAME_MAX_LENGTH,
        required=True,
        validators=(UsernameValidator(),)
    )


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=settings.USERNAME_MAX_LENGTH,
        required=True,
        validators=(UsernameValidator(),)
    )
    confirmation_code = serializers.CharField(required=True)


class UsersSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=settings.USERNAME_MAX_LENGTH,
        required=True,
        validators=(
            UniqueValidator(queryset=User.objects.all()),
            UsernameValidator(),
        )
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        lookup_field = 'username'


class UsersMeSerializer(UsersSerializer):
    role = serializers.CharField(read_only=True)


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        lookup_field = 'slug'
        fields = ('name', 'slug',)


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        lookup_field = 'slug'
        fields = ('name', 'slug',)


class GenresListingField(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = GenresSerializer(value)
        return serializer.data


class CategoriesListingField(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = CategoriesSerializer(value)
        return serializer.data


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для запросов на создание, удаление произведений."""
    genre = GenresListingField(
        slug_field='slug', many=True, queryset=Genres.objects.all()
    )
    category = CategoriesListingField(
        slug_field='slug', queryset=Categories.objects.all()
    )
    year = serializers.IntegerField(validators=[validate_year])

    class Meta:
        model = Title
        fields = '__all__'


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для запросов на получение произведений."""
    genre = GenresSerializer(many=True)
    category = CategoriesSerializer()
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'
        read_only = True


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для запросов на получение отзывов."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    score = serializers.IntegerField(
        validators=[
            MinValueValidator(1, message='Минимальное значение рейтинга 1'),
            MaxValueValidator(10, message='Максимальное значение рейтинга 10')
        ]
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title',)

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            author = request.user
            title_id = self.context['view'].kwargs.get('title_id')
            title = get_object_or_404(Title, id=title_id)
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError(
                    'Вы уже оставили свой отзыв о данном произведении.'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для запросов на получение комментариев."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review',)
