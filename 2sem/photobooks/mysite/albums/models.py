from django.db import models

from django.db import models
from django.contrib.auth.models import User


# ---------- SPRAWOCHNIKI ----------

class Role(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название роли")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"

    def __str__(self):
        return self.name


class Format(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название формата")
    width_mm = models.PositiveIntegerField(verbose_name="Ширина, мм")
    height_mm = models.PositiveIntegerField(verbose_name="Высота, мм")
    orientation = models.CharField(max_length=30, choices=[
        ("portrait", "Портрет"),
        ("landscape", "Альбом"),
        ("square", "Квадрат"),
    ], verbose_name="Ориентация")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Формат"
        verbose_name_plural = "Форматы"

    def __str__(self):
        return f"{self.name} ({self.width_mm}x{self.height_mm})"


class CoverType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Тип обложки")
    description = models.TextField(blank=True, verbose_name="Описание")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Тип обложки"
        verbose_name_plural = "Типы обложек"

    def __str__(self):
        return self.name


class AlbumStatus(models.Model):
    name = models.CharField(max_length=50, verbose_name="Статус")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Статус альбома"
        verbose_name_plural = "Статусы альбомов"

    def __str__(self):
        return self.name


# ---------- USER RELATIONS ----------

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name="Роль")
    assigned_at = models.DateTimeField(auto_now_add=True, verbose_name="Назначено")
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="assigned_roles",
                                    verbose_name="Кем назначено")

    class Meta:
        verbose_name = "Роль пользователя"
        verbose_name_plural = "Роли пользователей"
        unique_together = ('user', 'role')

    def __str__(self):
        return f"{self.user} — {self.role}"


# ---------- PHOTOS ----------

class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    file_path = models.ImageField(upload_to="photos/", verbose_name="Файл")
    thumbnail_path = models.ImageField(upload_to="thumbnails/", verbose_name="Превью", blank=True)
    file_size_bytes = models.PositiveIntegerField(verbose_name="Размер файла (байт)")
    width_px = models.PositiveIntegerField(verbose_name="Ширина")
    height_px = models.PositiveIntegerField(verbose_name="Высота")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Загружено")

    class Meta:
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"

    def __str__(self):
        return f"Фото #{self.id} пользователя {self.user}"


# ---------- ALBUMS ----------

class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    title = models.CharField(max_length=200, verbose_name="Название")
    format = models.ForeignKey(Format, on_delete=models.CASCADE, verbose_name="Формат")
    cover_type = models.ForeignKey(CoverType, on_delete=models.SET_NULL, null=True, verbose_name="Тип обложки")
    status = models.ForeignKey(AlbumStatus, on_delete=models.SET_NULL, null=True, verbose_name="Статус")
    cover_photo = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name="Фото обложки", related_name="cover_for")
    page_count = models.PositiveIntegerField(default=0, verbose_name="Количество страниц")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Изменён")
    favorited_by = models.ManyToManyField(
        User,
        through="FavoriteAlbum",
        related_name="favorite_albums",
        blank=True,
        verbose_name="Пользователи, добавившие в избранное"
     )

    class Meta:
        verbose_name = "Альбом"
        verbose_name_plural = "Альбомы"

    def __str__(self):
        return f"{self.title} ({self.user.username})"

    @property
    def is_ready(self):
        return self.status and self.status.name.lower() == "ready"


class AlbumPage(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, verbose_name="Альбом")
    page_number = models.PositiveIntegerField(verbose_name="Номер страницы")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Изменено")

    class Meta:
        verbose_name = "Страница альбома"
        verbose_name_plural = "Страницы альбомов"
        ordering = ("album", "page_number")

    def __str__(self):
        return f"Стр. {self.page_number} альбома {self.album.title}"


class AlbumPagePhoto(models.Model):
    page = models.ForeignKey(AlbumPage, on_delete=models.CASCADE, verbose_name="Страница")
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, verbose_name="Фото")
    x = models.FloatField(verbose_name="Позиция X")
    y = models.FloatField(verbose_name="Позиция Y")
    width = models.FloatField(verbose_name="Ширина")
    height = models.FloatField(verbose_name="Высота")
    rotation_angle = models.FloatField(default=0, verbose_name="Поворот")
    z_index = models.IntegerField(default=0, verbose_name="Слой")
    caption_text = models.CharField(max_length=300, blank=True, verbose_name="Подпись")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Изменено")

    class Meta:
        verbose_name = "Фото на странице"
        verbose_name_plural = "Фото на страницах"

    def __str__(self):
        return f"Фото {self.photo_id} на странице {self.page_id}"


# ---------- ORDERS ----------

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    status = models.CharField(max_length=50, verbose_name="Статус")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость")
    delivery_address = models.TextField(verbose_name="Адрес доставки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ #{self.id} ({self.user.username})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    album = models.ForeignKey(Album, on_delete=models.CASCADE, verbose_name="Альбом")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказов"

    def __str__(self):
        return f"{self.album.title} × {self.quantity}"

class FavoriteAlbum(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    album = models.ForeignKey("Album", on_delete=models.CASCADE, verbose_name="Альбом")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлен в избранное")

    class Meta:
        verbose_name = "Избранный альбом"
        verbose_name_plural = "Избранные альбомы"
        unique_together = ("user", "album")

    def __str__(self):
        return f"{self.user.username} → {self.album.title}"
