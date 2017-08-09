from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required


def acercaDe(request):
    return render_to_response('ProyectoNFC/acercaDe.html')

report = staff_member_required(acercaDe)