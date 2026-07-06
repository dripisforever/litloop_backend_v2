from django.urls import path
from todos.views import (
    get_todos,
    get_todo,
    create_todo,
    update_todo,
    delete_todo,
    upload_background_image,
    get_lists,
    create_list,
    update_list,
    delete_list,
    reorder_lists,
    reorder_todos,

)

urlpatterns = [
    path('all', get_todos, name='get_todos'),
    path('<int:todo_id>/', get_todo, name='get_todo'),
    path('create/', create_todo, name='create_todo'),
    path('<int:todo_id>/update/', update_todo, name='update_todo'),
    path('<int:todo_id>/delete/', delete_todo, name='delete_todo'),
    path('reorder/', reorder_todos, name='reorder_todos'),
    path('background-image/', upload_background_image, name='upload_background_image'),
    path('lists/', get_lists, name='get_lists'),
    path('lists/create/', create_list, name='create_list'),
    path('lists/<int:list_id>/update/', update_list, name='update_list'),
    path('lists/<int:list_id>/delete/', delete_list, name='delete_list'),
    path('lists/reorder/', reorder_lists, name='reorder_lists'),
]
