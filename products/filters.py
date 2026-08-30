from django.db.models import Q

def filter_products(queryset, query):
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
        
    return queryset