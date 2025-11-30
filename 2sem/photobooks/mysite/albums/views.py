from django.shortcuts import render

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q

from .models import Album, Format, Order


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
