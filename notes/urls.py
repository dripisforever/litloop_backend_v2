from django.urls import path
from notes.views import (
    list_pages,
    create_page,
    get_page,
    update_page,
    delete_page,
    create_block,
    update_block,
    delete_block,
    update_block_table,
    list_tags,
    add_tag,
    delete_tag,
    search_by_tags,
)

urlpatterns = [
    path('pages/', list_pages, name='list_pages'),
    path('pages/create/', create_page, name='create_page'),
    path('pages/<int:page_id>/', get_page, name='get_page'),
    path('pages/<int:page_id>/update/', update_page, name='update_page'),
    path('pages/<int:page_id>/delete/', delete_page, name='delete_page'),
    path('pages/<int:page_id>/blocks/create/', create_block, name='create_block'),
    path('blocks/<int:block_id>/update/', update_block, name='update_block'),
    path('blocks/<int:block_id>/delete/', delete_block, name='delete_block'),
    path('blocks/<int:block_id>/table/', update_block_table, name='update_block_table'),
    path('pages/<int:page_id>/tags/', list_tags, name='list_tags'),
    path('pages/<int:page_id>/tags/add/', add_tag, name='add_tag'),
    path('tags/<int:tag_id>/delete/', delete_tag, name='delete_tag'),
    path('search-by-tags/', search_by_tags, name='search_by_tags'),
]
