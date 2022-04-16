from django.contrib import admin

from movielist_web_project.accounts.models import Profile, MovieListUser

admin.site.site_header = 'MovieList Administration'

@admin.register(MovieListUser)
class MovieListUser(admin.ModelAdmin):
    list_display = ['email', 'is_staff', 'is_superuser', ]

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'facebook', 'instagram', 'twitter', 'website']
    exclude = ['user']