from django.contrib.sites.models import Site
mysite = Site.objects.get_current()
mysite.domain = '127.0.0.1'
mysite.name = 'The Center for Genetic Immune Diseases'
mysite.save()
