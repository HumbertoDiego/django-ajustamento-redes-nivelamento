# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
from . import Mtools
from scipy.stats import chi2
from numpy import size, array, linspace, mean
from math import sqrt
import pandas
import io
import base64

def parametrico(c, x , auto, dp_na_4col):
    ############ 1ª etapa - leitura do arquivo texto
    print(pandas.DataFrame(c))
    ############ 2ª etapa - pré processamento
    # gravando os dados em variáveis separadas
    re = []
    vante =[]
    observado = []
    dist = []
    dpinjuc = []
    aviso = ''
    for i in range(0, size(c, 0)): # converter numeros com virg para numeros com ponto
        re.append(str(c[i][0]).replace(',','.')) # 1ª col são estações a ré
        vante.append(str(c[i][1]).replace(',','.')) # 2ª col são estações a vante
        observado.append(str(c[i][2]).replace(',','.'))  # 3ª col são os desniveis observados
        print(observado[i])
        if c[i][0] == 0:
            dpinjuc.append(str(c[i][3]).replace(',','.'))
            dist.append(0)
            auto = False
            aviso = 'Aviso: Desvio Padrão convertido para manual devido a presença de Injuções'
        else:
            dpinjuc.append(0)
            dist.append(str(c[i][3]).replace(',','.'))
    observado = array(observado, float)
    dist = array(dist, float)
    dpinjuc = array(dpinjuc, float)

    RNsinvantes = []
    Pontos = []
    for i in range(0, len(vante)):
        try:
            array(vante[i], float)
            RNsinvantes.append(vante[i])
        except ValueError:
            RNsinvantes.append(0)
            Pontos.append(vante[i])

    RNsinres =[]
    for i in range(0, len(re)):
        try:
            array(re[i], float)
            RNsinres.append(re[i])
        except ValueError:
            RNsinres.append(0)
            Pontos.append(re[i])
    RNsinvantes = array(RNsinvantes, float)
    RNsinres = array(RNsinres, float)

    # qtPontos (parametros) = Qt de colunas da matriz A (u)
    qtPontos = len(set(Pontos))
    # qtEq = Qt de linhas da matriz A (n)
    qtEq = len(observado)
    # Graus de liberdade - Degrees of freedom - df
    df = qtEq - qtPontos
    # Lb = formado pelos termos independentes da equacao
    L0 = RNsinres - RNsinvantes
    Lb = observado + L0

    # Em vanteere: float devem ser trocadas por zero
    vanteere = re + vante
    for i in vanteere:
        try:
            array(i, float)
            local = vanteere.index(i)
            vanteere[local] = 0
        except ValueError:
             pass
    # Em vanteere: strings devem ser trocadas por Ids(1,2,3...)
    k = 1
    Incognitas =[]
    for i in vanteere:
        if type(i) == str:
            Incognitas.append(i)
            while i in vanteere:
                local = vanteere.index(i)
                vanteere[local] = k
            k = k+1
    res = array(vanteere[:qtEq],float)
    vantes = array(vanteere[qtEq:],float)

    ###   Modelagem Matemática: Método paramétrico de ajuste dos parâmetros X=(h1,h2,h3,...)
    ##    A*X = Lb + V    e  Xa = inv(A'*P*A)*(A'*P*L)
    A= Mtools.montA(vantes, res)
    # Montagem da matriz P de pesos
    sigmapriori = 1 ## em [mm^2]
    if dp_na_4col:
        auto = False
        SigmaLb , dp = Mtools.montSigmaLb_dp_na_4col(dist, dpinjuc)
    else:
        SigmaLb , dp = Mtools.montSigmaLb(dist, x, dpinjuc)
    pesos = sigmapriori*SigmaLb
    # X=inv(A'PA)A'PLb
    X= Mtools.Xa_parametrico(A,pesos,Lb)
    # V=A*X-Lb  [m]
    V=A.dot(X)-Lb

    ####################################### Estatistics #######################################################
    #################################### Teste chi^2 ##########################################################
    # sigma posterioti = V'PV/gl
    sigmaposteriori= V.transpose().dot(pesos).dot(V)/(df) ## em [m^2]
    quicalc = sigmaposteriori*df/sigmapriori
    signif = 0.05
    quitabmax = chi2.ppf(1-signif/2, df)
    quitabmin = chi2.ppf(signif/2, df)
    quicalcideal =  (quitabmax + quitabmin)/2
    # automatizacao do teste Chi²
    if auto:
        if quicalc>quicalcideal:
            while (quicalc-quicalcideal>0.5):
                SigmaLb , dp = Mtools.montSigmaLb(dist, x, dpinjuc)
                # nãp precisa repetir a fórmula X=inv(A'PA)A'PLb pq X é cte independente de variações lineares em Pesos
                # se X, A, Lb são ctes então V=A.dot(X)-Lb é cte
                quicalc = V.transpose().dot(SigmaLb).dot(V)
                x = x+1
        else:
            while (quicalcideal-quicalc>0.1):
                print(x)
                SigmaLb , dp = Mtools.montSigmaLb(dist, x, dpinjuc)
                # nãp precisa repetir a fórmula X=inv(A'PA)A'PLb pq X é cte independente de variações lineares em Pesos
                # se X, A, Lb são ctes então V=A.dot(X)-Lb é cte
                quicalc = V.transpose().dot(SigmaLb).dot(V)
                x = x - 0.1
        sigmaposteriori= V.transpose().dot(SigmaLb).dot(V)/(df) ## em [m^2]
        pesos = sigmapriori*SigmaLb
    if quicalc>quitabmax or quicalc<quitabmin:
        aviso2 = 'Aviso: Aumentar o desvio padrão inicial => Diminuir o Valor X^2 de teste'

    # # La=A*X ou La=Lb+V
    La=A.dot(X)
    La = La - L0
    dp = array(dp, float)
    var = dp*dp

    ####################################### MVC ##############################################
    SigmaXa = Mtools.estatistics_sigmaXa(sigmaposteriori, A, pesos) ## em [m^2]
    SigmaLa = Mtools.estatistics_sigmaLa(sigmaposteriori, A, pesos) ## em [m^2]
    SigmaV = Mtools.estatistics_sigmaV(sigmapriori, A, pesos) ## em [m^2]
    desvio_hi = Mtools.get_dp_hi(SigmaXa) ## em [m]
    desvio_vi = Mtools.get_dp_vi(SigmaV) ## em [m]

    ####################################### Teste Baarda ######################################
    wi =  Mtools.wi(V, desvio_vi)
    a0 = signif/qtEq
    aceitabaarda = sqrt(chi2.pdf(a0, 1))
    aceitar = []
    for i in range(0, len(wi)):
        if wi[i]<aceitabaarda and wi[i]>-aceitabaarda:
            aceitar.append('aceito')
        else:
            aceitar.append('ñ aceito')
    #######################################   Grafico Analise Qui-quadrado    ############################
    base64_fdpqui= grafico_teste_hipotesebicaudal(quicalc, signif, df)

    dicionario = dict(c=c, qtPontos=qtPontos, qtEq=qtEq, df=df, Lb=Lb, Incognitas=Incognitas, x=x, A=A, dp=dp, aviso=aviso, var=var, pesos=pesos, X=X,
                      V=V, La=La, sigmaposteriori=sigmaposteriori, sigmapriori=1, SigmaXa=SigmaXa, desvio_hi=desvio_hi, desvio_vi=desvio_vi, wi=wi,
                      a0=a0, aceitabaarda=aceitabaarda, aceitar=aceitar,SigmaLa=SigmaLa, SigmaV=SigmaV, signif=signif, quitabmaxbicaudal = quitabmax,
                      quitabminbicaudal = quitabmin, quicalc = quicalc, dp_na_4col=dp_na_4col,base64_fdpqui=base64_fdpqui)
    #print(dicionario)
    return dicionario

def grafico_teste_hipotesebicaudal(quicalc, signif, df):
    x = []
    x.append(linspace(0, chi2.ppf(signif/2, df), 100))
    x.append(linspace(chi2.ppf(signif/2, df), chi2.ppf(signif/2, df) + 0.2*(chi2.ppf(1-(signif/2), df)-chi2.ppf(signif/2, df)), 100))
    x.append(linspace(chi2.ppf(signif/2, df) + 0.2*(chi2.ppf(1-(signif/2), df)-chi2.ppf(signif/2, df)),
                      chi2.ppf(signif/2, df) + 0.4*(chi2.ppf(1-(signif/2), df)-chi2.ppf(signif/2, df)), 100))
    x.append(linspace(chi2.ppf(signif/2, df) + 0.4*(chi2.ppf(1-(signif/2), df)-chi2.ppf(signif/2, df)),
                      chi2.ppf(signif/2, df) + 0.6*(chi2.ppf(1-(signif/2), df)-chi2.ppf(signif/2, df)), 100))
    x.append(linspace(chi2.ppf(signif/2, df) + 0.6*(chi2.ppf(1-(signif/2), df)-chi2.ppf(signif/2, df)),
                      chi2.ppf(signif/2, df) + 0.8*(chi2.ppf(1-(signif/2), df)-chi2.ppf(signif/2, df)), 100))
    x.append(linspace(chi2.ppf(signif/2, df) + 0.8*(chi2.ppf(1-(signif/2), df)-chi2.ppf(signif/2, df)), chi2.ppf(1-(signif/2), df), 100))
    x.append(linspace(chi2.ppf(1-(signif/2), df), chi2.ppf(0.99, df), 100))


    if df ==1:
        maxY = 2
    else:
        maxY = 1.02 * max(chi2.pdf(x[0], df).tolist() + chi2.pdf(x[1], df).tolist() + chi2.pdf(x[2], df).tolist() + chi2.pdf(x[3], df).tolist() +
                      chi2.pdf(x[4], df).tolist() + chi2.pdf(x[5], df).tolist())
    fig, ax = plt.subplots(1, 1)
    ax.plot(x[0], chi2.pdf(x[0], df), 'b-', lw=3, alpha=0.7)
    ax.plot(x[1], chi2.pdf(x[1], df), 'b-', lw=3, alpha=0.7)
    ax.plot(x[2], chi2.pdf(x[2], df), 'b-', lw=3, alpha=0.7)
    ax.plot(x[3], chi2.pdf(x[3], df), 'b-', lw=3, alpha=0.7)
    ax.plot(x[4], chi2.pdf(x[4], df), 'b-', lw=3, alpha=0.7)
    ax.plot(x[5], chi2.pdf(x[5], df), 'b-', lw=3, alpha=0.7)
    ax.plot(x[6], chi2.pdf(x[6], df), 'b-', lw=3, alpha=0.7)

    ax.fill_between(x[0], 0, maxY, facecolor='red', alpha=0.8)
    ax.fill_between(x[1], 0, maxY, facecolor='yellow', alpha=0.6)
    ax.fill_between(x[2], 0, maxY, facecolor='green', alpha=0.6)
    ax.fill_between(x[2], 0, maxY, facecolor='yellow', alpha=0.6)
    ax.fill_between(x[3], 0, maxY, facecolor='green', alpha=0.6)
    ax.fill_between(x[4], 0, maxY, facecolor='green', alpha=0.6)
    ax.fill_between(x[4], 0, maxY, facecolor='yellow', alpha=0.6)
    ax.fill_between(x[5], 0, maxY, facecolor='yellow', alpha=0.6)
    ax.fill_between(x[6], 0, maxY, facecolor='red', alpha=0.8)

    plt.axvline(quicalc, color='k', linewidth='2')

    if df ==1:
        limit = [0, 6, 0, maxY]
    else:
        limit = [0, chi2.ppf(0.99, df), 0, maxY]
    plt.axis(limit)
    plt.grid(True)
    plt.xlabel('Significância')
    plt.ylabel('Chi^2(signif, %s gl)' %df)
    #path2 =  os.path.join(os.getcwd(),'ajunivel','static','images','fdpqui.png')
    #print(path2)
    #plt.savefig(path2)
    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='jpg')
    plt.close()
    my_stringIObytes.seek(0)
    my_base64_jpgData = base64.b64encode(my_stringIObytes.read())
    #print(my_base64_jpgData)
    return my_base64_jpgData.decode("utf-8")
