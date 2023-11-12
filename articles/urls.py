from django.urls import path
from .views import ArticleListView, ArticleDetailView, UserArticlesListView, ArticleUpdateView, ArticleDeleteView, CommentCreateView, ReactToArticle, CommentUpdateView, CommentDeleteView, ReactToComment, ArticleCommentsListView, CategoryListCreateView, CategoryRetrieveUpdateDestroyView
from .views import TagListCreateView, TagRetrieveUpdateDestroyView, UserFollowingArticlesView, UserArticlesView
from .views import LikedArticlesView, ArticleSearchView, get_articles_by_user, ReplyToCommentView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article-list'),
    path('articles/search/', ArticleSearchView.as_view(), name='article-search'),
    path('articles/user/following/', UserFollowingArticlesView.as_view(), name='following-articles'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('user/articles/', UserArticlesListView.as_view(), name='user-articles'),
    # path('user/articles/liked', UserArticlesListView.as_view(), name='user-articles'),
    path('articles/liked/', LikedArticlesView.as_view(), name='liked-articles'),
    path('articles/<int:pk>/edit/', ArticleUpdateView.as_view(), name='edit-article'),
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='delete-article'),
    path('articles/<int:article_id>/react/<str:reaction_type>/', ReactToArticle.as_view(), name='article-reaction'),
    path('articles/<int:article_id>/comments/', ArticleCommentsListView.as_view(), name='article-comments-list'),
    path('comments/<int:comment_id>/react/<str:reaction_type>/', ReactToComment.as_view(), name='comment-reaction'),
    path('comments/<int:comment_id>/reply/', ReplyToCommentView.as_view(), name='comment-reaction'),
    path('articles/<int:article_id>/comment/', CommentCreateView.as_view(), name='create-comment'),
    path('comments/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment-update'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-retrieve-update-delete'),
    path('tags/', TagListCreateView.as_view(), name='tag-list-create'),
    path('tags/<int:pk>/', TagRetrieveUpdateDestroyView.as_view(), name='tag-retrieve-update-delete'),
    # path('articles/users/<int:user_id>/', get_articles_by_user, name='get-articles-by-user'),
    path('articles/users/<int:user_id>/', UserArticlesView.as_view(), name='user-articles'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)