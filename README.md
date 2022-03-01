# django-ajustamento-redes-nivelamento - Ajunivel
IMPLEMENTAÇÃO DE SISTEMA PARA CÁLCULOS GEODÉSICOS EM AMBIENTE COMPUTACIONAL LIVRE: AJUSTAMENTO DE REDE DE NIVELAMENTO GEOMÉTRICO 

Trabalho de conclusão de curso de Engenharia Cartográfica no Instituto Militar de Engenharia.

![r1](imgs/res.jpg "Tela do Resolutado do ajustamento")

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


## 1. Requisitos

    Python >=3.8
    Django >= 4.0 
    matplotlib==3.4.3
    numpy==1.21.3
    pandas==1.3.3
    scipy==1.7.1

## 2. Instalação
1. Download e install 
    `python -m pip install --user django-ajunivel-0.1.tar.gz`

2. Add "ajunivel" to your INSTALLED_APPS setting like this::
```
    INSTALLED_APPS = [
        ...
        'ajunivel',
    ]
```
3. Include the ajunivel URLconf in your project urls.py like this::
```
    path('ajunivel/', include('ajunivel.urls')),
```
4. Run `python manage.py migrate` to create the ajunivel models.

5. Start the development server (`python manage.py runserver`) and visit http://127.0.0.1:8000/admin/ (
    you'll need the Admin app enabled).

6. Visit http://127.0.0.1:8000/ajunivel/ to execute the ajunivel calculator.

## 2. Utilização

No formulário, envie um arquivo texto formatado contendo as equações e as variáveis a serem ajsutadas. Deixe o checkbox `automático==True` para testar os desvios-padrões que passam no Teste-Chi Quadrado.

Siga as instruções das imagens abaixo para formatar adequadamente o arquivo texto:

![d1](imgs/demo1.jpg "Demonstração")

![d2](imgs/demo2.jpg "Demonstração")

![d3](imgs/demo3.jpg "Demonstração")

![d4](imgs/demo4.jpg "Demonstração")

![d5](imgs/demo5.jpg "Demonstração")
