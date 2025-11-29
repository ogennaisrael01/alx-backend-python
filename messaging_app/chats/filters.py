from django_filters import rest_framework as filters
from .models import Message



class MesssageFilter(filters.FilterSet):
    date_filter  = filters.DateFromToRangeFilter(
        field_name="sent_at",
        label="sent_at"
    )
    class Meta:
        model = Message
        fields = [
            "date_filter",
        ]
    