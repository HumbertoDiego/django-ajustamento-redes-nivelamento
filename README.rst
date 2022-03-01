=====
Ajunivel
=====

SISTEMA DE CÁLCULO GEODÉSICO: 
IMPLEMENTAÇÃO DE AJUSTAMENTO DE REDES DE NIVELAMENTO GEOMÉTRICO EM 
AMBIENTES COMPUTACIONAIS LIVRES

Nenhuma medição é exata. Devido a necessidade de se realizar uma grande 
quantidade de medições para se obter uma média representativa do real 
valor da grandeza observada, que o ajustamento é uma ferramenta importante
entre os pesquisadores (especialistas em medições). Especialmente o 
ajustamento por mínimos quadrados (MMQ) vem ganhando espaço por ser o 
método de análise e ajustamento de dados mais rigoroso devido a sua 
abordagem probabilística dos erros, a sua capacidade de considerar a 
ponderação de cada observação e ainda pelo rompimento da barreira do 
custo computacional elevado. Neste trabalho será aplicada a modelagem 
paramétrica do MMQ para resolver problemas de ajustamento de redes 
altimétricas, bem como os testes de qualidade para detecção e identificação
de erros. Sob a premissa de apenas se utilizar de ambientes computacionais
livres, o produto usa a linguagem Python para realização dos cálculos, o 
webframework de código aberto Web2py para incorporação do resultados 
obtidos em Hyper Text Markup Language- HTML, além de módulos Python 
abertos de uso científico, incluirá o software, exemplos, documentação de 
apoio e a metainformação, tudo estará disponível on-line e gratuito.

Quick start
-----------

1. Add "ajunivel" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'ajunivel',
    ]

2. Include the ajunivel URLconf in your project urls.py like this::

    path('ajunivel/', include('ajunivel.urls')),

3. Run ``python manage.py migrate`` to create the ajunivel models.

4. Start the development server and visit http://127.0.0.1:8000/admin/ (
    you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/ajunivel/ to execute the ajunivel calculator.