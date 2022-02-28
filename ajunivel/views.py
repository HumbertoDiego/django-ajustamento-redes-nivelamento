# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import dp, successcount
from .forms import AjustamentoForm,AjustamentoCustomForm
from . import NivParamet


def menu(request):
    context = {
        'dps': dp.objects.all(),
    }
    return render(request, 'ajunivel/menu.html', context)


def index(request):
    retorno = "" #str(request.GET)
    erro = False
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AjustamentoCustomForm(request.POST, request.FILES)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            X = form.cleaned_data['dp']
            auto = form.cleaned_data['automatico']
            dp_na_4col = form.cleaned_data['dpinformado']
            c = []
            for line in request.FILES['arquivo']:
                if len(line.split()) == 4:
                    c.append([l.decode("utf-8")  for l in line.split()])
                else: # acrescentar 0 na 1º pos das linhas que só possuírem 3 dados e gravar tudo em uma matriz c[] para aceitar injunções
                    temp = [l.decode("utf-8")  for l in line.split()]
                    temp.insert(0, 0)
                    c.append(temp)
            retorno = NivParamet.parametrico(c, X, auto, dp_na_4col).copy()
            # atualizar o succesos count
            if len(successcount.objects.all()):
                old  = successcount.objects.all()[0].contador
                new = successcount.objects.filter(pk=1)
                new.update(contador=str(int(old)+1))
            else:
                successcount.objects.create(contador="0")
            tab1 = ""
            for i in range(0,len(c)):
                tab1 += "<tr>"
                for k in range(0,len(c[i])):
                    tab1 += "<td>"+c[i][k]+"</td>"
                tab1 += "<td>"+str(retorno['dp'][i])+"</td>"
                tab1 += "<td>"+str(retorno['La'][i])+"</td>"
                tab1 += "<td>"+str(retorno['V'][i])+"</td>"
                tab1 += "</tr>"
            retorno['tab1'] = tab1
            tab2 = ""
            for i in range(0,len(retorno['Incognitas'])):
                tab2 += "<tr>"
                tab2 += "<td>"+str(retorno['Incognitas'][i])+"</td>"
                tab2 += "<td>"+str(retorno['X'][i])+"</td>"
                tab2 += "<td>"+str(retorno['desvio_hi'][i])+"</td>"
                tab2 += "</tr>"
            retorno['tab2'] = tab2
            tab3 = ""
            for i in range(0,len(c)):
                tab3 += "<tr>"
                tab3 += "<td>"+str(i+1)+"</td>"
                for k in range(0,len(c[i])):
                    tab3 += "<td>"+c[i][k]+"</td>"
                tab3 += "<td>"+str(retorno['V'][i])+"</td>"
                tab3 += "<td>"+str(retorno['desvio_vi'][i])+"</td>"
                tab3 += "<td>"+str(retorno['wi'][i])+"</td>"
                if retorno['aceitar']=='aceito':
                    tab3 += "<td style='color:green'>Não existe evidências estatísticas para a rejeição</td>"
                else:
                    tab3 += "<td style='color:red'>Existe evidências estatísticas para a rejeição</td>"
                tab3 += "</tr>"
            retorno['tab3'] = tab3
    else:
        form = AjustamentoCustomForm()
    context = {
        'erro': erro,
        'retorno': retorno,
        'form': form,
        'dps': dp.objects.all(),
        'sucessos': successcount.objects.all()[0] if len(successcount.objects.all()) else "!",
    }
    return render(request, 'ajunivel/index.html', context)
