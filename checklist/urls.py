from django.urls import path
from . import views
from .views import (ChecklistListView,
    UserChecklistListView, 
	ChecklistDetailView, 
	ChecklistCreateView,
	ChecklistUpdateView,
	ChecklistDeleteView,

)

urlpatterns = [
    # path('', ChecklistListView.as_view(), name='checklist-home'),
    path('', views.home, name='checklist-home'), 
    path('user/<str:username>', UserChecklistListView.as_view(), name='user-checklists'), #path('', views.home, 
    path('checklist/<int:pk>/', ChecklistDetailView.as_view(), name='checklist-detail'),
    path('checklist/new/', ChecklistCreateView.as_view(), name='checklist-create'),
    path('checklist/<int:pk>/update/', ChecklistUpdateView.as_view(), name='checklist-update'),
    path('checklist/<int:pk>/delete/', ChecklistDeleteView.as_view(), name='checklist-delete'),
    path('about/', views.about, name='checklist-about'),
    path('mychecklist/', views.mychecklist, name='checklist-mychecklist'),
    path('checklist/<int:checklist_id>/<str:username>/upvote/', views.upvote_checklist, name='checklist-upvote'),
    path('checklist/<int:checklist_id>/<str:username>/bookmark/', views.bookmark_checklist, name='checklist-bookmark')
]