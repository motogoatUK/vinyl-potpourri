"""
record.utils - added to avoid code repetition in all records list
and collection records list especially as they use the same template.
"""


def get_ordering(request, model):
    ordering = request.GET.get("ordering", "title")

    if ordering:
        # Validate ordering field to prevent SQL injection
        if ordering.lstrip('-') in [
                f.name for f in model._meta.get_fields()]:
            return ordering
        return None
