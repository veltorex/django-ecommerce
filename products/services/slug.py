from django.utils.text import slugify


def create_unique_slug(title, model):
    base_slug = slugify(title)
    slug = base_slug
    counter = 2

    while model.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug