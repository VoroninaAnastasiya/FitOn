from django.db import models

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager, PermissionsMixin
)

from django.db import models

class UserManager(BaseUserManager):
    """
    Django требует, чтобы кастомные пользователи определяли свой собственный
    класс Manager. Унаследовавшись от BaseUserManager, мы получаем много того
    же самого кода, который Django использовал для создания User (для демонстрации).
    """

    def create_user(self, username, email, password=None, name=None,
                    lastname=None, contact_phone=None, **extra_fields):
        """ Создает и возвращает пользователя с имэйлом, паролем и именем. """
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        email = self.normalize_email(email)

        user = self.model(
            username=username,
            email=email,
            name=name,
            lastname=lastname,
            contact_phone=contact_phone,
            **extra_fields
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """ Создает и возввращет пользователя с привилегиями суперадмина. """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель пользователя.

    Наследование:
    - AbstractBaseUser — предоставляет базовые поля и методы аутентификации
      (password, last_login, set_password, check_password).
    - PermissionsMixin — добавляет поля is_superuser, группы и разрешения.

    Особенности модели:
    - email используется как логин (USERNAME_FIELD = 'email');
    - username остаётся уникальным публичным идентификатором;
    - email и username индексируются и уникальны (db_index + unique);
    - дополнительные поля: имя, фамилия, телефон;
    - флаги is_active и is_staff управляют доступом;
    - created_at и updated_at — автоматические временные метки.

    Модель полностью совместима с Django Admin, аутентификацией и SimpleJWT.
    """

    # Каждому пользователю нужен понятный человеку уникальный идентификатор,
    # который мы можем использовать для предоставления User в пользовательском
    # интерфейсе. Мы так же проиндексируем этот столбец в базе данных для
    # повышения скорости поиска в дальнейшем.
    username = models.CharField(db_index=True, max_length=255, unique=True)
    name = models.CharField(max_length=50, verbose_name='Имя пользователя', null=True, blank=True)
    lastname = models.CharField(max_length=50, verbose_name='Фамилия пользователя', null=True, blank=True)
    contact_phone = models.IntegerField(verbose_name='Номер телефона', null=True, blank=True)

    # Так же мы нуждаемся в поле, с помощью которого будем иметь возможность
    # связаться с пользователем и идентифицировать его при входе в систему.
    # Поскольку адрес почты нам нужен в любом случае, мы также будем
    # использовать его для входа в систему, так как это наиболее
    # распространенная форма учетных данных на данный момент (еще телефон).
    email = models.EmailField(db_index=True, unique=True)

    # Когда пользователь более не желает пользоваться нашей системой, он может
    # захотеть удалить свой аккаунт. Для нас это проблема, так как собираемые
    # нами данные очень ценны, и мы не хотим их удалять :) Мы просто предложим
    # пользователям способ деактивировать учетку вместо ее полного удаления.
    # Таким образом, они не будут отображаться на сайте, но мы все еще сможем
    # далее анализировать информацию.
    is_active = models.BooleanField(default=True)

    # Этот флаг определяет, кто может войти в административную часть нашего
    # сайта. Для большинства пользователей это флаг будет ложным.
    is_staff = models.BooleanField(default=False)

    # Временная метка создания объекта.
    created_at = models.DateTimeField(auto_now_add=True)

    # Временная метка показывающая время последнего обновления объекта.
    updated_at = models.DateTimeField(auto_now=True)

    # Дополнительный поля, необходимые Django при указании кастомной модели пользователя.
    # Свойство USERNAME_FIELD сообщает нам, какое поле мы будем использовать
    # для входа в систему. В данном случае мы хотим использовать почту.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Сообщает Django, что определенный выше класс UserManager
    # должен управлять объектами этого типа.
    objects = UserManager()

    class Meta:
        #улучшает отображение модели в Django Admin
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        """ Строковое представление модели (отображается в консоли) """
        return self.email


    def get_full_name(self):
        """
        Этот метод требуется Django для таких вещей, как обработка электронной
        почты. Обычно это имя фамилия пользователя, но поскольку мы не
        используем их, будем возвращать username.
        Возвращает полное имя пользователя
        """
        return f"{self.name} {self.lastname}".strip()
    #
    def get_short_name(self):
        """ Аналогично методу get_full_name().
        Возвращает короткое имя пользователя."""
        return self.name or self.username