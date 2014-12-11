from django.conf.urls import patterns, include, url
from django.contrib import admin
from hello.views import index,user_review,device_review,middleware_review,kvm_manage,server_info

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cimc1.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^cimc/index.html$', index),
    url(r'^cimc/user-review.html$',user_review ),
    url(r'^cimc/device-review.html$',device_review ),
    url(r'^cimc/middleware-review.html$', middleware_review),
    url(r'^cimc/kvm-manage.html$', kvm_manage),
    url(r'^cimc/server-info.html$', server_info),
)
