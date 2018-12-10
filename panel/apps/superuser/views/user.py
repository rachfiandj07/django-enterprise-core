'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: user.py
# Project: <<projectname>>
# File Created: Monday, 10th December 2018 2:39:06 pm
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         http://ardz.xyz>
# 
# Last Modified: Monday, 10th December 2018 2:39:06 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
# 
# Crafted by Pro
# Copyright - <<year>> Ardz & Co, -
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


from django.views.generic import TemplateView 
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from panel.libs.view import ProtectedMixin
from datatable import Datatable
from ..forms import UserForm


class UserView(ProtectedMixin, TemplateView):
    template_name = "user.html"

    def get(self, request, *args, **kwargs):

        if request.GET.get('draw', None) != None:
            return self.datatable(request)

        return self.render_to_response({})

    def delete(self, request):
        o_id = request.body.decode('utf-8').split("=")[1]
        User = get_user_model()
        qs = User.objects.filter(id__exact = o_id).first()
        qs.delete()
        return self.render_to_response({})

    def datatable(self, request):
        User = get_user_model()
        qs = User.objects.all()
        defer = ['id', 'full_name', 'is_active', 'is_staff', 'is_superuser']

        d = Datatable(request, qs, defer, key="id")
        return d.get_data()


class UserFormView(ProtectedMixin, TemplateView):
    template_name = "user.form.html"

    def get(self, request, *args, **kwargs):
        edit = request.GET.get("edit")
        User = get_user_model()

        if edit:
            form = UserForm(instance=User.objects.get(id=edit))
        else:
            form = UserForm()

        return self.render_to_response({"form":form})

    def post(self, request):
        edit = request.GET.get("edit")
        User = get_user_model()

        if edit:
            form = UserForm(request.POST, instance=User.objects.get(id=edit))
        else:
            form = UserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()            
            user.permissions.set(form.cleaned_data.get('permissions'))
            user.save()
            messages.success(request, 'User (%s) has been saved.' % user.name)
            return redirect("superuser:user")
        else:
            return self.render_to_response({"form":form})