from django.conf.urls import patterns, include, url
from django.contrib import admin
from quanter.temp_views import *


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'^hello/$', hello),
    (r'hello/(\d+)/$',hello1),
    (r'^extend/$',views),
    (r'^form/$',form),

    url(r'^admin/', include(admin.site.urls)),

)

urlpatterns += patterns('', 
    (r'^view1/$', views, {'template_name':'1.html'}),
    (r'^view2/$', views, {'template_name':'2.html'}),
)

urlpatterns += patterns('',
    (r'^index$', views, {'template_name':'index.html'}),
    (r'^strategy$', views, {'template_name':'strategy.html'}),
)


urlpatterns += patterns('quanter.views',
    (r'^3k5k/$', 'show'),
)