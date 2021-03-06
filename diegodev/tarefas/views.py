from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from diegodev.tarefas.forms import TarefaNovaForm, TarefaForm
from diegodev.tarefas.models import Tarefa


def home(request):
    if request.method == 'POST':
        form = TarefaNovaForm(request.POST)  # UM DICT QUE CONTÉM OS DADOS QUE FORAM ENVIADOS PELO POST
        if form.is_valid():
            form.save()  # OS DADOS SERÃO SALVOS NO FORMULÁRIO
            return HttpResponseRedirect(reverse('tarefas:home'))  # PARA O USUÁRIO IR PARA PÁGINA INICIAL
        else:
            tarefas_pendentes = Tarefa.objects.filter(feita=False).all()
            tarefas_feitas = Tarefa.objects.filter(feita=True).all()
            return render(request, 'tarefas/home.html',
                          {
                              'form': form,
                              'tarefas_pendentes': tarefas_pendentes,
                              'tarefas_feitas': tarefas_feitas
                          },
                          status=400)
    tarefas_pendentes = Tarefa.objects.filter(feita=False).all()
    tarefas_feitas = Tarefa.objects.filter(feita=True).all()
    return render(request, 'tarefas/home.html',
                  {
                      'tarefas_pendentes': tarefas_pendentes,
                      'tarefas_feitas': tarefas_feitas,
                  }
                  )


def detalhe(request, tarefa_id):
    if request.method == 'POST':
        tarefa = Tarefa.objects.get(id=tarefa_id)
        form = TarefaForm(request.POST, instance=tarefa)
        if form.is_valid():
            form.save()
    return HttpResponseRedirect(reverse('tarefas:home'))


def apagar(request, tarefa_id):
    if request.method == 'POST':
        Tarefa.objects.filter(id=tarefa_id).delete()
    return HttpResponseRedirect(reverse('tarefas:home'))
