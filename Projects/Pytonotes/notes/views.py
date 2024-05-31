from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from notes.models import Workspace, Page
from django.db.models import Q
from django.http import JsonResponse

@login_required
def home(request):
    current_workspace_id = request.GET.get('workspace_id')
    if current_workspace_id:
        current_workspace = get_object_or_404(Workspace, id=current_workspace_id, members=request.user)
    else:
        current_workspace = Workspace.objects.filter(members=request.user).first()
    workspaces = Workspace.objects.filter(members=request.user).distinct()
    pages = current_workspace.pages.all() if current_workspace else []
    return render(request, 'base.html', {
        'top_workspace_text': current_workspace.name[0:11] + '...' if current_workspace else '',
        'current_workspace': current_workspace,
        'workspaces': workspaces,
        'pages': pages,
    })

def redirect_to_valid_workspace(request):
    valid_workspace = Workspace.objects.filter(Q(user=request.user) | Q(members=request.user)).first()
    if valid_workspace:
        return redirect(f'/notes/?workspace_id={valid_workspace.id}')
    else:
        return redirect('/notes/')

@login_required
def create_workspace(request):
    if request.method == 'POST':
        user = request.user
        workspace_name = f"{user.email.split('@')[0]}'s Workspace"
        workspace = Workspace.objects.create(user=user, name=workspace_name)
        workspace.members.add(user)
        return JsonResponse({
            'id': workspace.id,
            'name': workspace.name,
            'members_count': workspace.members.count()
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def delete_page(request, page_id):
    page = get_object_or_404(Page, id=page_id, workspace__members=request.user)
    if request.method == 'DELETE':
        page.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def duplicate_page(request, page_id):
    page = get_object_or_404(Page, id=page_id, workspace__members=request.user)
    if request.method == 'POST':
        new_page = Page.objects.create(
            workspace=page.workspace,
            title=f"{page.title} (Copy)",
            icon=page.icon,
            content=page.content 
        )
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def get_page_details(request, page_id):
    page = get_object_or_404(Page, id=page_id, workspace__members=request.user)
    return JsonResponse({
        'id': page.id,
        'title': page.title,
        'content': page.content
    })

@require_POST
@login_required
def update_page_title(request, page_id):
    page = get_object_or_404(Page, id=page_id, workspace__members=request.user)
    new_title = request.POST.get('title')
    new_content = request.POST.get('content')
    if new_title:
        page.title = new_title
    if new_content:
        page.content = new_content
    page.save()
    return JsonResponse({'success': True})

