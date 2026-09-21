from django.urls import path

from . import views


# Added app_name to avoid namespace collisions with other apps in the project. While this may not be important for this project, it is good practice that I want to get in the habit of doing.
# It also allows for more flexibility in the future if I want to add more apps to the project.
app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new"),
    path("wiki/<str:entry>/edit", views.edit, name="edit"),
    path("random", views.random, name="random")
]
