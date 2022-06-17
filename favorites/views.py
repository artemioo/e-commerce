from django.shortcuts import render, redirect


def favorites_list(request):
    context = {}
    return render(request, 'favorites_list.html', context)


def add_to_favorites(request, id):
    if request.method == 'POST':
        if not request.session.get('favorites'):  # если у нас нет избранного
            request.session['favorites'] = list()  # создается избранное
        else:
            request.session['favorites'] = list(request.session['favorites'])  #  иначе заполняем избранное

        # проверяем есть объект в нашем избранном
        # item_exist = next((item for item in request.session['favorites'] if item['type'] == request.POST.get['type']
        #                    and item['id'] == id), False)

        item_exist = False

        for item in request.session['favorites']:
            if item['type'] == request.POST.get('type') and item['id'] == id:
                item_exist = True
            else:
                item_exist = False

        add_data = {
            'type': request.POST.get('type'),
            'id': id
        }

        if not item_exist:
            request.session['favorites'].append(add_data)
            request.session.modified = True
        print(request.session['favorites'])
    return redirect(request.POST.get('url_from'))


def remove_from_favorites(request, id):
    if request.method == 'POST':

        #  удаляем объект из избранного
        for item in request.session['favorites']:
            if item['id'] == id and item['type'] == request.POST.get('type'):
                item.clear()

        # удаляем пустые сеты из нашего списка
        while {} in request.session['favorites']:
            request.session['favorites'].remove({})

        # удаляем избранное если пустое
        if not request.session['favorites']:
            del request.session['favorites']

        request.session.modified = True
    return redirect(request.POST.get('url_from'))


def delete_favorites(request):
    if request.session.get['favorites']:
        del request.session['favorites']
    return redirect(request.POST.get('url_from'))
