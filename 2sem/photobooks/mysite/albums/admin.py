from django.contrib import admin

from django.contrib import admin
from .models import (
    Role, Format, CoverType, AlbumStatus,
    UserRole, Photo, Album, AlbumPage, AlbumPagePhoto,
    Order, OrderItem, FavoriteAlbum
) 


# ---------- INLINE КЛАССЫ ----------

class AlbumPageInline(admin.TabularInline):
    model = AlbumPage
    extra = 1
    readonly_fields = ("created_at", "updated_at")


class AlbumPagePhotoInline(admin.TabularInline):
    model = AlbumPagePhoto
    extra = 1
    raw_id_fields = ("photo",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    raw_id_fields = ("album",)


# ---------- РЕГИСТРАЦИЯ МОДЕЛЕЙ ----------

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "assigned_at", "assigned_by")
    list_filter = ("role",)
    search_fields = ("user__username", "role__name")
    raw_id_fields = ("user", "assigned_by")


@admin.register(Format)
class FormatAdmin(admin.ModelAdmin):
    list_display = ("name", "orientation", "size_mm", "is_active")
    list_filter = ("orientation", "is_active")
    search_fields = ("name",)
    readonly_fields = ()

    @admin.display(description="Размер (мм)")
    def size_mm(self, obj):
        return f"{obj.width_mm} × {obj.height_mm}"


@admin.register(CoverType)
class CoverTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(AlbumStatus)
class AlbumStatusAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "file_path", "file_size_bytes", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username",)
    raw_id_fields = ("user",)
    date_hierarchy = "created_at"
    readonly_fields = ("thumbnail_path",)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "format", "status", "page_count", "updated_at", "ready_flag")
    list_filter = ("format", "status")
    list_display_links = ("title",)
    search_fields = ("title", "user__username")
    raw_id_fields = ("user", "cover_photo")
    inlines = [AlbumPageInline]
    date_hierarchy = "created_at"

    @admin.display(description="Готов?")
    def ready_flag(self, obj):
        return "Да" if obj.is_ready else "Нет"


@admin.register(AlbumPage)
class AlbumPageAdmin(admin.ModelAdmin):
    list_display = ("album", "page_number", "updated_at")
    list_filter = ("album",)
    inlines = [AlbumPagePhotoInline]
    search_fields = ("album__title",)
    date_hierarchy = "updated_at"


@admin.register(AlbumPagePhoto)
class AlbumPagePhotoAdmin(admin.ModelAdmin):
    list_display = ("page", "photo", "x", "y", "z_index")
    list_filter = ("page", "z_index")
    raw_id_fields = ("page", "photo")
    search_fields = ("page__album__title",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "total_price", "created_at", "updated_at")
    list_filter = ("status",)
    search_fields = ("user__username",)
    date_hierarchy = "created_at"
    inlines = [OrderItemInline]
    raw_id_fields = ("user",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "album", "quantity", "price_per_item")
    raw_id_fields = ("order", "album")


@admin.register(FavoriteAlbum)
class FavoriteAlbumAdmin(admin.ModelAdmin):
    list_display = ("user", "album", "added_at")
    search_fields = ("user__username", "album__title")
    raw_id_fields = ("user", "album")