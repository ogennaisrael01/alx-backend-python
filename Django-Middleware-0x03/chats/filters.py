from django_filters import rest_framework as filters
from .models import Messages



class MesssageFilter(filters.FilterSet):
    date_filter  = filters.DateFromToRangeFilter(
        field_name="sent_at",
        label="sent_at"
    )
    class Meta:
        model = Messages
        fields = [
            "date_filter",
        ]
    