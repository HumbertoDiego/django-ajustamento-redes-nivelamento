# -*- coding: utf-8 -*-
from numpy import array , zeros, size
from numpy.linalg import inv , det
from math import sqrt
from pandas import DataFrame

def txt2matrix(filename):
    f=open(filename, 'r')
    c=[]
    for line in f:
        c.append(line.split())
    d = array(c, float)
    return d

def montSigmaLb(dist, X, dpinjuc):
    P = zeros((size(dist, 0), size(dist, 0)), float)
    dp = []
    for i in range(size(dist, 0)):
        if dist[i] == 0:
            dp.append(dpinjuc[i])
        else:
            dp.append(X*sqrt(dist[i])/1000) # dp em m
    for i in range(size(dist, 0)):
        P[i, i] = 1/(dp[i]*dp[i]) # sigmaprio convertido pra metro^2
    return P, dp

def montSigmaLb_dp_na_4col(dist, dpinjuc):
    P = zeros((size(dist, 0), size(dist, 0)), float)
    dp = dist + dpinjuc
    for i in range(size(dp, 0)):
        P[i, i] = 1/(dp[i]*dp[i]) # sigmaprio convertido pra metro^2
    return P, dp

def montA(vante, re):
    re =array(re,int)
    vante=array(vante,int)
    qtPontos = int(max(vante.tolist() + re.tolist()))
    qtEq = len(re)
    print("aqui",qtPontos,qtEq)
    print("aqui",int(qtPontos),qtEq)
    A= zeros((qtEq,qtPontos),float)
    for i in range(0,qtEq):
        if re[i]!=0:
            print(re[i])
            A[i][re[i] - 1]=-1
    for i in range(0,qtEq):
        if vante[i]!=0:
            A[i][vante[i] - 1]=1
    return A

def Xa_parametrico(A,P,Lb):
    # Retorna o resultado de Xa = inv(A'*P*A)*A'*P*Lb
    print("A = ", DataFrame(A))
    x = A.transpose().dot(P).dot(A)
    print("A'PA = ", DataFrame(x))
    x = inv(x)
    print("inv(A'PA) = ",DataFrame(x))
    x = x.dot(A.transpose().dot(P).dot(Lb))
    print("inv(A'PA)A'PLb = ",DataFrame(x))
    return x

def estatistics_sigmaXa(sigma2prio,A,P):
    # SigmaXa - MVC do valores de X
    # x = A.transpose().dot(P).dot(A)
    # print DataFrame(A.transpose().dot(P).dot(A))
    # print det(A.transpose().dot(P).dot(A))
    # x = inv(x)
    return sigma2prio*inv(A.transpose().dot(P).dot(A))

def estatistics_sigmaLa(sigma2,A,P):
    # SimgaLa - MVC dos valores de La
    N = inv(A.transpose().dot(P).dot(A))
    return (A.dot(N).dot(A.transpose()))

def estatistics_sigmaV(sigma2,A,P):
    # SimgaV - MVC dos residuos
    N = inv(A.transpose().dot(P).dot(A))
    return sigma2*(inv(P) - A.dot(N).dot(A.transpose()))

def wi(V, desvio_vi):
    wi = []
    try:
        for i in range(0,len(V)):
            wi.append(V[i]/desvio_vi[i])
    except:
        for i in range(0, len(V)):
            wi.append(None)
    return wi

def get_dp_hi(SigmaXa):
    desvio_hi=[]
    try:
        for i in range(0,len(SigmaXa)):
            desvio_hi.append(sqrt(SigmaXa[i][i]))
    except ValueError:
        for i in range(0, len(SigmaXa)):
            desvio_hi.append(None)
    return desvio_hi

def get_dp_vi(SigmaV):
    desvio_vi=[]
    try:
        for i in range(0,len(SigmaV)):
            desvio_vi.append(sqrt(SigmaV[i][i]))
    except ValueError:
        for i in range(0, len(SigmaV)):
            desvio_vi.append(None)
    return desvio_vi
