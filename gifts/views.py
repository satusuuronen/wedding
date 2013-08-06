import json

from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.base import (TemplateView, View)
from django.views.generic.edit import (FormView)
from django.core.context_processors import csrf
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import (reverse, reverse_lazy)
from django.forms.models import model_to_dict
from django.contrib.auth import models as auth_models

from models import Gift

class LoginView(FormView):
    template_name = 'gifts/index.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('giftlist:list')
        
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.check_and_delete_test_cookie()
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        self.set_test_cookie()
        return super(LoginView, self).form_invalid(form)

    def set_test_cookie(self):
        self.request.session.set_test_cookie()

    def check_and_delete_test_cookie(self):
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
            return True
        return False

    def get(self, request, *args, **kwargs):
        self.set_test_cookie()
        return super(LoginView, self).get(request, *args, **kwargs)


class GiftView(TemplateView):
    template_name = 'gifts/gifts.html'
    @method_decorator(login_required(None, 'next', 'giftlist:login'))
    def get(self, request, *args, **kwargs):            
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
    

class GetGiftsView(View):
    @method_decorator(login_required(None, 'next', 'giftlist:login'))
    def get(self, request, *args, **kwargs):
        gifts = Gift.objects.all()
        gift_list = []
        for gift in gifts:
            d = model_to_dict(gift)
            if d['booker'] != None:
                if d['booker'] == request.user.id:
                    d['booker'] = 'mine'
                else:
                    d['booker'] = 'reserved'
            gift_list.append(d)
        response = json.dumps(gift_list)
        return HttpResponse(response)    


class BookingsView(View): 
    @method_decorator(login_required(None, 'next', 'giftlist:login'))
    def put(self, request, *args, **kwargs):
        self.pk = self.kwargs.get('pk')
        gift = Gift.objects.get(id = self.pk)
        user = auth_models.User.objects.get(id = request.user.id)
        if gift.booker != None:
            if gift.booker == user:
                gift.booker = None
            else:
                return HttpResponse(status=400)
        else:
            gift.booker = user
        gift.save()
        return HttpResponse('Gift booked.') 
          

class LogoutView(View):
    redirect_url = reverse_lazy('giftlist:login')
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    @method_decorator(login_required(None, 'next', 'giftlist:login'))
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            auth.logout(self.request)
        return redirect(LogoutView.redirect_url)



