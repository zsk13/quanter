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
    (r'^initData/$',initData),

    url(r'^admin/', include(admin.site.urls)),

)

urlpatterns += patterns('', 
    (r'^view1/$', views, {'template_name':'1.html'}),
    (r'^view2/$', views, {'template_name':'2.html'}),
)

urlpatterns += patterns('quanter.views.login',
    (r'^index$', 'index'),
    (r'^logininfo$','logininfo')
)


urlpatterns += patterns('quanter.views',
    (r'^3k5k/$', 'show'),
)



urlpatterns += patterns('quanter.views.maStrategy',
    (r'^maStrategy/$', 'maSingleTest'),
    (r'^maStrategy/singleTest$', 'maSingleTest'),
    (r'^maStrategy/multiTest$', 'maMultiTest'),
    (r'^maStrategy/autoTest$', 'maAutoTest'),
    (r'^maStrategy/backTest/$', 'maBackTest'),
    (r'^maStrategy/autoFindParam/$', 'maAutoFindParam'),
    (r'^maStrategy/maMultiTestStockPool/$', 'maMultiTestStockPool'),
    
)

urlpatterns += patterns('quanter.views.biasStrategy',
    (r'^biasStrategy/$', 'biasSingleTest'),
    (r'^biasStrategy/singleTest$', 'biasSingleTest'),
    (r'^biasStrategy/multiTest$', 'biasMultiTest'),
    (r'^biasStrategy/backTest/$', 'biasBackTest'),
    (r'^biasStrategy/multiTestStockPool/$', 'biasMultiTestStockPool'),
    
)


urlpatterns += patterns('quanter.views',
    (r'^svmStrategy/$', 'svmStrategy'),
    (r'^svmStrategy/training$', 'svm_training'),
    (r'^svmStrategy/backTest/$','svm_test'),
    (r'^svmStrategy/result$','svm_result'),
    # (r'^backTest/$', 'backTest'),
)

urlpatterns += patterns('quanter.views',
    (r'^customStrategy/$', 'customSingleTest'),
    (r'^customStrategy/singleTest$', 'customSingleTest'),
    (r'^customStrategy/backTest/$','customBackTest'),
    (r'^customStrategy/multiTest$', 'customMultiTest'),
    (r'^customStrategy/multiTestStockPool$','customMultiTestStockPool'),
    # (r'^backTest/$', 'backTest'),
)

urlpatterns += patterns('quanter.views',
    (r'^stockpool/$', 'showStock'),
    (r'^stockpool/showStock$', 'showStock'),
    (r'^stockpool/searchStock$', 'searchStock'),
     (r'^stockpool/addStock$', 'addStock'),
    (r'^stockpool/showStockPool$', 'showStockPool'),
    (r'^stockpool/deleteStock$', 'deleteStock'),
    # (r'^backTest/$', 'backTest'),
)

urlpatterns += patterns('',
  # existing patterns here...
  url(r'', include('users.urls')),
)
