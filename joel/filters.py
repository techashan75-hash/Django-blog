import django_filters
from .models import Post
class PostFilter(django_filters.FilterSet):
  title=django_filters.CharFilter(lookup_expr='icontains')
  content=django_filters.CharFilter(lookup_expr='icontains')
  author=django_filters.CharFilter(field_name='author__username',label='Post author')
  date_created=django_filters.DateFromToRangeFilter()

  class Meta:
    model=Post 
    fields=['title','content','author','date_created']
    
