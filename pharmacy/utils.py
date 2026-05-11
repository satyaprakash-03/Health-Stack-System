from django.db.models import Q
from .models import Medicine


def searchMedicines(request):
    search_query = ''
    category_filter = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    if request.GET.get('category'):
        category_filter = request.GET.get('category')

    medicines = Medicine.objects.filter(Q(name__icontains=search_query))

    if category_filter:
        medicines = medicines.filter(medicine_category__icontains=category_filter)

    return medicines, search_query, category_filter
