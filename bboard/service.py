from django_filters import rest_framework as filters

from bboard.models import Comment


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class CommentFilter(filters.FilterSet):
    """Custom filtration by Category or Post"""
    category = CharFilterInFilter(field_name='post__category__name', lookup_expr='in', label='Category')

    class Meta:
        model = Comment
        fields = ['post_id']
