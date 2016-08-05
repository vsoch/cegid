from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required
from django.contrib.sitemaps.views import sitemap, index
from django.conf.urls import include, url, patterns
from cegid.apps.users import urls as users_urls
from django.http import Http404, HttpResponse
from cegid.apps.main import urls as main_urls
from cegid.apps.api.sitemap import sitemaps
from django.conf.urls.static import static
import django.contrib.sitemaps.views as sitemap_views
from django.views.static import serve
from django.conf import settings
from django.contrib import admin
import os

# Custom error views
from django.conf.urls import ( handler404, handler500 )

# Configure custom error pages
handler404 = 'cegid.apps.main.views.handler404'
handler500 = 'cegid.apps.main.views.handler500'

admin.autodiscover()

urlpatterns = [ 
                url(r'^admin/tools/', include('admin_tools.urls')),
                url(r'^', include(main_urls)),
                url(r'^accounts/', include(users_urls)),
                url(r'^admin/', include(admin.site.urls)),
                url(r'^weblog/', include('zinnia.urls')),
                url(r'^comments/', include('django_comments.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Add sitemaps for blog, etc.
#urlpatterns += [
#    sitemap_views,
#    url(r'^sitemap.xml$', index,{'sitemaps': sitemaps}),
#    url(r'^sitemap-(?P<section>.+)\.xml$', sitemap,{'sitemaps': sitemaps}),
#]


if settings.DEBUG:
    urlpatterns += [
        url(r'^(?P<path>favicon\.ico)$', serve, {
            'document_root': settings.STATIC_ROOT}),
    ]
