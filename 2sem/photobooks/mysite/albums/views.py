from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
from .forms import AlbumForm
from django.http import JsonResponse

from .models import Album, Format, Order, AlbumPage, AlbumPagePhoto, FavoriteAlbum


@login_required
def index(request):
    user = request.user

    # 1) Мои последние альбомы (top-5)
    last_albums = (
        Album.objects
        .filter(user=user)
        .select_related('format', 'status')
        .annotate(photo_count=Count('albumpage__albumpagephoto', distinct=True))
        .order_by('-updated_at')[:5]
    )

    # 2) Популярные форматы альбомов по количеству заказов
    popular_formats = (
        Format.objects
        .annotate(order_count=Count('album__orderitem', distinct=True))
        .filter(order_count__gt=0)
        .order_by('-order_count')[:5]
    )

    last_albums = Album.objects.filter(user=user).annotate(
    is_favorite=Exists(
        FavoriteAlbum.objects.filter(user=user, album=OuterRef('pk'))
    )
)

    # 3) Активные заказы пользователя (не завершённые)
    active_orders = (
        Order.objects
        .filter(user=user)
        .exclude(status__iexact='completed')
        .order_by('-created_at')[:5]
    )

    # 4) Поиск по альбомам
    query = request.GET.get('q')
    search_results = None
    total_photos_in_found_albums = None

    if query:
        search_results = (
            Album.objects
            .filter(user=user)
            .filter(
                Q(title__icontains=query) |
                Q(format__name__icontains=query)
            )
            .select_related('format', 'status')
            .annotate(photo_count=Count('albumpage__albumpagephoto', distinct=True))
            .order_by('-updated_at')
        )

        # Пример агрегатной функции SUM: сколько всего фото во всех найденных альбомах
        total_photos_in_found_albums = search_results.aggregate(
            total_photos=Sum('photo_count')
        )['total_photos']

    context = {
        'last_albums': last_albums,
        'popular_formats': popular_formats,
        'active_orders': active_orders,
        'query': query,
        'search_results': search_results,
        'total_photos_in_found_albums': total_photos_in_found_albums,
    }
    return render(request, 'index.html', context)

@login_required
def album_list(request):
    """Список всех альбомов текущего пользователя + кнопки CRUD."""
    albums = (
        Album.objects
        .filter(user=request.user)
        .select_related("format", "cover_type", "status")
        .annotate(photo_count=Count("albumpage__albumpagephoto", distinct=True))
        .order_by("-updated_at")
    )
    return render(request, "albums/album_list.html", {"albums": albums})


@login_required
def album_detail(request, album_id):
    """Отдельная страница альбома: вся инфа + связанные объекты."""
    album = get_object_or_404(
        Album.objects.select_related("format", "cover_type", "status", "user"),
        pk=album_id,
        user=request.user,
    )

    pages = (
        AlbumPage.objects
        .filter(album=album)
        .order_by("page_number")
    )

    # Все фото с координатами по страницам
    page_photos = (
        AlbumPagePhoto.objects
        .filter(page__album=album)
        .select_related("page", "photo")
        .order_by("page__page_number", "z_index")
    )

    # Простая группировка: страница -> список фото
    photos_by_page = {}
    for ap in page_photos:
        photos_by_page.setdefault(ap.page_id, []).append(ap)

    context = {
        "album": album,
        "pages": pages,
        "photos_by_page": photos_by_page,
    }
    return render(request, "albums/album_detail.html", context)


@login_required
def album_create(request):
    """Создание нового альбома."""
    if request.method == "POST":
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.save()
            return redirect("album_detail", album_id=album.id)
    else:
        form = AlbumForm()

    return render(request, "albums/album_form.html", {
        "form": form,
        "mode": "create",
    })


@login_required
def album_update(request, album_id):
    """Редактирование существующего альбома."""
    album = get_object_or_404(Album, pk=album_id, user=request.user)

    if request.method == "POST":
        form = AlbumForm(request.POST, request.FILES, instance=album)
        if form.is_valid():
            form.save()
            return redirect("album_detail", album_id=album.id)
    else:
        form = AlbumForm(instance=album)

    return render(request, "albums/album_form.html", {
        "form": form,
        "mode": "edit",
        "album": album,
    })


@login_required
def album_delete(request, album_id):
    """Удаление альбома (с подтверждением)."""
    album = get_object_or_404(Album, pk=album_id, user=request.user)

    if request.method == "POST":
        album.delete()
        return redirect("album_list")

    return render(request, "albums/album_confirm_delete.html", {
        "album": album,
    })

@login_required
def toggle_favorite(request, album_id):
    album = Album.objects.get(id=album_id)
    user = request.user

    fav, created = FavoriteAlbum.objects.get_or_create(user=user, album=album)

    if not created:
        # уже было в избранном → удаляем
        fav.delete()
        return JsonResponse({"status": "removed"})

    return JsonResponse({"status": "added"})