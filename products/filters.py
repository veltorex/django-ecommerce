from django.db.models import Q


def filter_products(query, queryset, request):
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    selected_category = request.GET.getlist("category")

    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    sort_by = request.GET.get("sort")

    if min_price:
        queryset = queryset.filter(price__gte=min_price)

    if max_price:
        queryset = queryset.filter(price__lte=max_price)

    if selected_category:
        queryset = queryset.filter(
            category_id__in=selected_category
        )

    if sort_by == "price_low":
        queryset = queryset.order_by("price")

    elif sort_by == "price_high":
        queryset = queryset.order_by("-price")

    elif sort_by == "newest":
        queryset = queryset.order_by("-created_at")

    return queryset