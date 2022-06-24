from django.shortcuts import render, redirect
from shop.models import Product

from favorites.models import Favorite


def favorites_list(request):
    product = Favorite.objects.filter(user=request.user)
    context = {'products': product}
    print(request.session['favorites'].keys())
    return render(request, 'favorites/favorites.html', context)


def add_to_favorites(request, id):
    if request.method == 'POST':
        if not request.session.get('favorites'):  # если у нас нет избранного
            request.session['favorites'] = {}  # создается избранное
        else:
            request.session['favorites'] = request.session['favorites']  #  иначе заполняем избранное

        item_exist = False
        for item_id in request.session['favorites'].values():
            if item_id == id:
                item_exist = True
            else:
                item_exist = False

        if not item_exist:
            request.session['favorites'][str(id)] = {'id': id, 'name': request.POST.get('name')}
            Favorite.objects.create(
                user=request.user,
                product=Product.objects.get(id=id)
            )
            request.session.modified = True
        print(request.session['favorites'])
    return redirect(request.POST.get('url_from'))


def remove_from_favorites(request, id):
    if request.method == 'POST':
        print(request.session['favorites'].keys())
        print(id)
        #  удаляем объект из избранного
        product = Favorite.objects.get(id=id)
        print(product)
        product.delete()

        # удаляем избранное если пустое
        if not request.session['favorites']:
            del request.session['favorites']

        request.session.modified = True
    return redirect('favorites_list')


def delete_favorites(request):
    if request.session.get['favorites']:
        del request.session['favorites']
    return redirect(request.POST.get('url_from'))
