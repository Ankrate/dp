from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Products, Categories
from django.db.models import Count, Min, Max
from django.db.models import Q, Subquery
from django.core.paginator import Paginator
from django.conf import settings
import os
from django.contrib.contenttypes.models import ContentType
from comments.forms import CommentForm
from comments.models import Comment
from django.utils.html import strip_tags
from django.core.mail import send_mail
from email_form.forms import EmailFormLight, EmailFormOneField
from email_form.models import EmailModel


def show_cars():
    qs = Products.objects.values('car').annotate(dcount=Count('car'))
    return qs

def show_brands(pk, car, cat):
    for k, v in kwargs.items():
        pass
    qs = Products.objects.filter(cat = 2502).values('brand').annotate(dbrand=Count('brand'))
    return qs

def show_price(price_min, price_max):
    price_range = Products.objects.filter(price__range=[price_min, price_max])
    p_min = Products.objects.all().aggregate(Min('price'))
    p_max = Products.objects.all().aggregate(Max('price'))
    return p_min, p_max, price_range

def categories_tree(pk):

    if pk > 999:
        cats = Categories.objects.filter(id=pk)
    if pk < 999 and pk > 99:
        cats = Categories.objects.filter(parent_id=pk)
    if pk < 99:
        cats_sub = Categories.objects.filter(parent_id=pk)
        c_l = []
        for cat_sub in cats_sub:
            c_l.append(cat_sub.id)
        cats = Categories.objects.filter(parent_id__in=c_l)
    return cats        
    

def get_image_path(qs):

    working_dir = settings.STATICFILES_DIRS[1] 
    for obj in qs:
        try:
            if  obj.main_img:
                f = os.path.join(obj.cat_n, obj.main_img)
            else:
                files  =  os.listdir(os.path.join(working_dir, obj.cat_n))
                f = os.path.join(obj.cat_n, files[0])

            setattr(obj, 'image_path', f) 
        except Exception as e:
            print(e)
    return qs


def newparts(request):
    qs = Products.objects.all()[:100]
    qs = get_image_path(qs)
    cats = Categories.objects.filter(parent_id=0)
    try:
        p = Paginator(qs, 20)
        page = request.GET.get('page')
        objects = p.get_page(page)
    except:
        pass
    if request.GET.get('load_all') == 'all':
        objects = get_image_path(objects)

    sale_prod = [2274, 2582, 2027]
    brakes = Products.objects.filter(id__in=sale_prod)
    brakes = get_image_path(brakes)
    context = {
            'objects': objects, 
            'categories': cats,
            'cars': show_cars(),
            'brakes': brakes,
           # 'brands': show_brands(),
            }
    return render(request, 'products/newparts.html', context)


def cars(request, car):
    qs = Products.objects.filter(car=car).order_by('?')[:50]
    cats_tmp = Categories.objects.filter(parent_id=0)
    cats = []
    for c in cats_tmp:
        nums = Products.objects.filter(car=car, cat__in=categories_tree(c.id)).count()
        if nums != 0:
            setattr(c, 'prod_count', nums)
            cats.append(c)
    try:
        p = Paginator(qs, 20)
        page = request.GET.get('page')
        objects = p.get_page(page)
    except:
        pass
    if request.GET.get('load_all') == 'all':
        objects = qs
    objects = get_image_path(objects)

    sale_prod = [2274, 2582, 2027]
    brakes = Products.objects.filter(id__in=sale_prod)
    brakes = get_image_path(brakes)

    context = {
            'objects': objects,
            'cars': show_cars(),
            'categories': cats,
            'single_car': car,
            'brakes': brakes,
            }
    return render(request, 'products/newparts.html', context)

def cars_subcats(request, car, slug, **kwargs):
    brand = request.GET.get('brand', None)
    cats_tmp = Categories.objects.get(slug=slug)
    second_level_cats = Categories.objects.filter(parent_id=cats_tmp.id)
    cats = []
    for c in second_level_cats:
        nums = Products.objects.filter(car=car, cat__in=categories_tree(c.id)).count()
        if nums != 0:
            setattr(c, 'prod_count', nums) 
            cats.append(c)

    cats_list = [] 
    if len(cats) == 0:
        if brand:
            qs = Products.objects.filter(car=car, cat=cats_tmp.id, brand=brand).distinct()
        else:
            qs = Products.objects.filter(car=car, cat=cats_tmp.id).distinct()
    else:
        for c in cats:
            cats_list.append(c.id)
        groups = Categories.objects.filter(parent_id__in=cats_list)
        for g in groups:
            cats_list.append(g.id) 
        if brand:
            qs = Products.objects.filter(car=car, cat__in=cats_list, brand=brand).distinct()
        else:
            qs = Products.objects.filter(car=car, cat__in=cats_list).distinct()
    
    brands = qs.values('brand').annotate(brand_count=Count('brand')) 
    h1 = cats_tmp.name
    try:
        p = Paginator(qs, 20)
        page = request.GET.get('page')
        objects = p.get_page(page)
    except:
        pass
    if request.GET.get('load_all') == 'all':
        objects = qs
    
    objects = get_image_path(objects)

    sale_prod = [2274, 2582, 2027]
    brakes = Products.objects.filter(id__in=sale_prod)
    brakes = get_image_path(brakes)

    context = {
            'objects': objects,
            'cars': show_cars(),
            'categories': cats,
            'single_car': car,
            'brands': brands,
            'title_h1': h1,
            'car': car,
            'brand': brand,
            'brakes': brakes,
            }
    
    return render(request, 'products/newparts.html', context)

# HERE IS SAME STUFF BUT NO CAR

def subcat(request, slug, **kwargs):
    brand = request.GET.get('brand', None)
    cats_tmp = Categories.objects.get(slug=slug)
    second_level_cats = Categories.objects.filter(parent_id=cats_tmp.id)
    cats = []
    for c in second_level_cats:
        nums = Products.objects.filter(cat__in=categories_tree(c.id)).count()
        if nums != 0:
            setattr(c, 'prod_count', nums) 
            cats.append(c)

    cats_list = [] 
    if len(cats) == 0:
        if brand:
            qs = Products.objects.filter(cat=cats_tmp.id, brand=brand).distinct()
        else:
            qs = Products.objects.filter(cat=cats_tmp.id).distinct()
    else:
        for c in cats:
            cats_list.append(c.id)
        groups = Categories.objects.filter(parent_id__in=cats_list)
        for g in groups:
            cats_list.append(g.id) 
        if brand:
            qs = Products.objects.filter(cat__in=cats_list, brand=brand).distinct()
        else:
            qs = Products.objects.filter(cat__in=cats_list).distinct()
    
    brands = qs.values('brand').annotate(brand_count=Count('brand')) 
    h1 = cats_tmp.name
    try:
        p = Paginator(qs, 20)
        page = request.GET.get('page')
        objects = p.get_page(page)
    except:
        pass
    if request.GET.get('load_all') == 'all':
        objects = qs
    
    objects = get_image_path(objects)
    sale_prod = [2274, 2582, 2027]
    brakes = Products.objects.filter(id__in=sale_prod)
    brakes = get_image_path(brakes)
            

    context = {
            'objects': objects,
            'cars': show_cars(),
            'categories': cats,
            'brands': brands,
            'title_h1': h1,
            'brand': brand,
            'brakes': brakes,
            }
    
    return render(request, 'products/newparts.html', context)

#Detailed product view starts here

def detailed(request, pk):
    cats = Categories.objects.filter(parent_id=0)
    obj = Products.objects.get(id=pk)
    
    # Redefine function inside to returning lists of files in the directories
    def get_image_path(obj):
        working_dir = settings.STATICFILES_DIRS[1] 
        files  =  os.listdir(os.path.join(working_dir, obj.cat_n))[:10]
        img_list = []
        for f in files:
            img_list.append(os.path.join(obj.cat_n, f))
        setattr(obj, 'image_path', img_list ) 
        return obj


    comments = Comment.objects.filter_by_instance(obj)
    comments = Comment.objects.filter_by_instance(obj)

    initial_data = {
        'content_type': obj.get_content_type,
        'object_id': obj.id,
    }

    form = CommentForm(request.POST or None, initial=initial_data)
    user_string = None
    if form.is_valid():

        if request.user.is_authenticated:
            user_string = request.user
        elif form.cleaned_data.get('user') is not None:
            user_string = form.cleaned_data.get('user')
        else:
            user_string = 'ANONIMUS'

        c_type = form.cleaned_data.get('content_type')
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get('content')
        parent_obj = None
        try:
            parent_id = request.POST.get('parent_id')
            print(parent_id)
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists():
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
            content_type=content_type,
            object_id=obj_id,
            content=strip_tags(content_data),
            parent=parent_obj,
            user=strip_tags(user_string),
        )
        url = new_comment.content_object.get_absolute_url()
        send_mail(
                'Ducatoparts.ru новый комментарий',
                f'На дукато партс оставили новый комментарий на странице {url}',
                'angara99@gmail.com',
                ['angara99@gmail.com', 'yellkalolka@gmail.com'],
                fail_silently=False,
                )
        return HttpResponseRedirect(url)
    

    #comments count stuff
    def check_comment_count():
        count = comments.count() % 10
        comment_word = 'КОММЕНТАРИЕВ'
        if count == 1:
            comments_word = 'КОММЕНТАРИЙ'
        elif count > 1 and count < 5:
            comment_word = 'КОММЕНТАРИЯ'
        elif count >= 5:
            comment_word = 'КОММЕНТАРИЕВ'
        return comment_word
    # Форма звонка Вася

    e_form = EmailFormLight(request.POST or None)

    if e_form.is_valid():

        phone = e_form.cleaned_data.get('phone')
        name = e_form.cleaned_data.get('name')
        callback, created = EmailModel.objects.get_or_create(phone=phone, name=name)
    # Похожие товары

    context = {
            'object': get_image_path(obj),
            'categories': cats,
            'cars': show_cars(),
            'comments': comments,
            'comment_count_word': check_comment_count(),
            'comment_form': form,
            'email_form': e_form,
            }
    return render(request, 'products/product.html', context)


def search(request):
    qs = Products.objects.filter(name__icontains="фильтр").distinct()
    
    search = request.GET.get('search')

    def search_splitter(search):
        from .stemmer import Porter
        s = Porter()
        search_list = search.split(' ')
        new_search_list = []
        for word in search_list:
            n_w = s.stem(word)
            new_search_list.append(n_w)
        return(new_search_list)

    search_list = search_splitter(search)

    if len(search_list) == 1:
        qs_s = f'Products.objects.filter(name__icontains="{search}").distinct().filter('
    else:
        qs_s = f'Products.objects.filter('
        for word in search_list:
            qs_s += f'Q(name__icontains="{word}") & '
#        qs_s = qs_s.rstrip()
#        qs_s = qs_s.rstrip('&').rstrip()
#        qs_s += ').distinct()'
#        print(qs_s)

    cars_l = request.GET.getlist('car')
    cats_l = request.GET.getlist('cat')
    brands_l = request.GET.getlist('brand')
    if cars_l:
        qs_s += f'Q(car__in={cars_l}) & '
    if cats_l:
        qs_s += f'Q(cat__in={cats_l}) & '
    if brands_l:
        qs_s += f'Q(brand__in={brands_l}) & '
    else:
        pass
    qs_s = qs_s.rstrip()
    qs_s = qs_s.rstrip('&').rstrip()
    qs_s += ')'
    print(qs_s)
    qs = eval(qs_s)

    qs_cars = qs.values('car').annotate(scount=Count('car'))

    qs_brand = qs.values('brand').annotate(bcount=Count('brand'))

    qs_cats = qs.prefetch_related('cat')#.annotate(ccount=Count('cat'))
    l = []
    for q in qs_cats:
        for c in q.cat.all():
            caa = Categories.objects.get(id=c.parent_id)
            if caa.id not in l:
                l.append(caa.id)
    cats = Categories.objects.filter(parent_id__in=l)
    
    ca = [] 
    for c in cats:
        p = qs.filter(cat=c.id)
        if not p:
            continue
        ca.append({'cat': c, 'ccount': p.count()})
    

    try:
        p = Paginator(qs, 20)
        page = request.GET.get('page')
        objects = p.get_page(page)
    except:
        pass
    if request.GET.get('load_all') == 'all':
        objects = qs
    
    objects = get_image_path(objects)
    context = {
                'objects': objects,
                'cars': qs_cars, 
                'search_categories': ca,
                'brands': qs_brand,
            }
    return render(request, 'products/search.html', context)
