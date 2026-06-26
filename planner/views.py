"""
Vistas basadas en funciones (FBVs) para la aplicacion FeedPlan.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import models as db_models
from .models import MediaPost, AgendaItem
from .forms import RegisterForm, MediaUploadForm, AgendaItemForm


def index(request):
    """Pagina de inicio: redirige al dashboard si el usuario esta autenticado."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'planner/index.html')


def register(request):
    """Registro de nuevo usuario."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registro exitoso. ¡Bienvenido!')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'planner/register.html', {'form': form})


def user_login(request):
    """Inicio de sesion de usuario."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Usuario o contrasena incorrectos.')
    return render(request, 'planner/login.html')


@login_required
def user_logout(request):
    """Cierre de sesion."""
    logout(request)
    return redirect('index')


@login_required
def dashboard(request):
    """
    Dashboard principal con simulador visual de feeds.
    Permite subir imagenes y previsualizarlas en formato Instagram, Facebook o TikTok.
    """
    view_mode = request.GET.get('view', 'instagram')
    media_list = MediaPost.objects.filter(user=request.user)

    if request.method == 'POST':
        form = MediaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            media = form.save(commit=False)
            media.user = request.user
            max_order = media_list.aggregate(db_models.Max('order'))['order__max']
            media.order = (max_order or 0) + 1
            media.save()
            messages.success(request, 'Imagen subida correctamente.')
            return redirect('dashboard')
    else:
        form = MediaUploadForm()

    return render(request, 'planner/dashboard.html', {
        'form': form,
        'media_list': media_list,
        'view_mode': view_mode,
    })


@login_required
def media_delete(request, media_id):
    """Elimina una imagen subida por el usuario."""
    media = get_object_or_404(MediaPost, id=media_id, user=request.user)
    media.delete()
    messages.success(request, 'Imagen eliminada.')
    return redirect('dashboard')


@login_required
def media_reorder(request):
    """
    Reordena las imagenes via drag & drop.
    Recibe JSON con {media_id: new_order, ...}
    """
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        for media_id, new_order in data.items():
            MediaPost.objects.filter(id=media_id, user=request.user).update(order=new_order)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def agenda(request):
    """Vista de la agenda semanal con todos los posts del usuario."""
    days_order = ['LU', 'MA', 'MI', 'JU', 'VI', 'SA', 'DO']
    items = AgendaItem.objects.filter(user=request.user)
    agenda_by_day = {day: items.filter(day=day) for day in days_order}
    return render(request, 'planner/agenda.html', {
        'agenda_by_day': agenda_by_day,
        'days': AgendaItem.DAYS,
        'days_order': days_order,
    })


@login_required
def agenda_add(request):
    """Agrega un nuevo post a la agenda semanal."""
    user_images = MediaPost.objects.filter(user=request.user)
    if request.method == 'POST':
        form = AgendaItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            form.save_m2m()
            messages.success(request, 'Post agregado a la agenda.')
            return redirect('agenda')
    else:
        form = AgendaItemForm()
        form.fields['images'].queryset = user_images
    return render(request, 'planner/agenda_form.html', {
        'form': form, 'title': 'Agregar Post', 'user_images': user_images,
    })


@login_required
def agenda_edit(request, item_id):
    """Edita un post existente en la agenda."""
    item = get_object_or_404(AgendaItem, id=item_id, user=request.user)
    user_images = MediaPost.objects.filter(user=request.user)
    if request.method == 'POST':
        form = AgendaItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post actualizado.')
            return redirect('agenda')
    else:
        form = AgendaItemForm(instance=item)
        form.fields['images'].queryset = user_images
    return render(request, 'planner/agenda_form.html', {
        'form': form, 'title': 'Editar Post', 'user_images': user_images,
    })


@login_required
def agenda_delete(request, item_id):
    """Elimina un post de la agenda."""
    item = get_object_or_404(AgendaItem, id=item_id, user=request.user)
    item.delete()
    messages.success(request, 'Post eliminado de la agenda.')
    return redirect('agenda')


@login_required
def agenda_move(request, item_id):
    """Mueve un post a otro dia de la semana."""
    item = get_object_or_404(AgendaItem, id=item_id, user=request.user)
    if request.method == 'POST':
        new_day = request.POST.get('new_day')
        if new_day in dict(AgendaItem.DAYS):
            item.day = new_day
            item.save()
            messages.success(request, f'Post movido a {item.get_day_display()}.')
    return redirect('agenda')
