# Logbook - Testes de Fontes do Sirius

- senha do usuário fac: a mesma que da sala de controle.
- não fechar laptop de aquisição pelo labview! (se fechar, comunicar com gabriel)
- os dados da aquisição deverão ser gravados no centaurus/Troce e acessados como
  um recurso samba do domínio. para montar:
  sudo mount -t cifs -o username=ximenes.resende //centaurus/Repositorio/Troca/testes_fontes_sirius /home/fac/troca/
- o script de aquisição e análise é o 'lnls-ramp-test.py'
- para rodar o IOC de timing:
  cd /home/fac/Desktop/lnls105-controle/sirius-timing-ioc; make clean; make uninstall; make install
  cd iocBoot/ioctiming/; ./st.cmd
- IOC das fontes é iniciado automaticamente com o BBB (root@10.0.21.89)
- o script de aquisição e análise é o 'lnls-ramp-test.py', instalado no sistema.
- os dados brutos se enontram lnls449-linux:/home/fac_files/lnls-sirius/ps-tests/data/

Para rodar o IOC de Timing:

- cd /home/fac_files/lnls-sirius/ps-tests/sinap-timing-epics-ioc/iocBoot/ioctiming/
- ./runEVG.sh -i 10.0.21.97 -p 50118 -P AS-Glob:TI- -R EVG: -d EVG
- ./runEVR.sh -i 10.0.21.96 -p 50114 -P AS-Glob:TI- -R EVR-1: -d EVR-1 

# 2017-11-28 - ENTREGA VERSÂO IOC PARA TESTES DO FIRWARE DOS CONTROLADORES DAS FONTES

programado.

# 2017-11-24 - ENTREGA PRIMEIRA VERSÃO DO FIRMWARE DOS CONTROLADORES DAS FONTES

programado.

Foi gerado o gráfico comparando um trecho da rampa up de aquisição com a versão original do setup (data/test1_17-09-19_1459.txt) com dados da versão atual (data/test8_17-11-13_1005.txt):

 [ramp_comparison.png](analysis/2017-11-24/ramp_comparison.png)

# 2017-11-13 - TESTES TRACKING

> dados: test8_17-11-13_1005.txt
> dados: test9_17-11-13_1006.txt
> dados: test10_17-11-13_1037.txt
> dados: test11_17-11-13_1038.txt

> script: [run_analysis.py](analysis/run_analysis.py)

Após exaustivos testes de perda de pontos da ramp fizemos mais uma digitalização do sinal de rampa das corretoras 3 e 4. O firmware dos controladores das fontes não se alterou. O software de comunicação do BBB com as fontes é um software temporário que não implementa servidor EPICS.

Primeiramente fizemos testes digitalizando apenas as correntes das fontes  3 e 4 (test8 e test9) e, depois, com as fontes 1 e 2 (test10 e test11).

A tabela abaixo compara o erro de tracking residual destes últimos quatro testes com os anteriores. O erro de tracking foi calculado no intervalo de ramp que corresponden ao intervalo com feixe. A corrente de cada fonte, em cada umas das 19 rampas, foi subtraída da reta mediana e expressa em unidades de ppm. Além disto foi subtraído um error lento ao longo da rampa através de fitting the uma polinômio de grau 3. Este erro lento pode ser corrigido alterando as waveforms das fontes.

TESTE  | Erro Max | Erro Std | Observação
------ | -------- | -------- | -----------------------------------------------------------------
test01 | 246      | 129      | setup original (3 fontes)
test02 | 261      | 128      | setup original (3 fontes)
test03 | 227      | 128      | setup original (3 fontes)
------ | -------- | -------- | -----------------------------------------------------------------
test04 | 201      | 70       | PI do controlador alterado (3 fontes)
test05 | 196      | 70       | PI do controlador alterado (3 fontes)
test06 | 196      | 70       | PI do controlador alterado (3 fontes)
------ | -------- | -------- | -----------------------------------------------------------------
test07 | 124      | 35       | Primeiro teste com novo firmware (IOC controla rampa)
------ | -------- | -------- | -----------------------------------------------------------------
test08 | 109      | 31       | Testes após correção de perdas de pontos rampa (corretoras 1 e 2)
test09 | 112      | 31       | Testes após correção de perdas de pontos rampa (corretoras 1 e 2)
test10 | 109      | 29       | Testes após correção de perdas de pontos rampa (corretoras 3 e 4)
test11 | 107      | 29       | Testes após correção de perdas de pontos rampa (corretoras 3 e 4)
------ | -------- | -------- | -----------------------------------------------------------------

As figuras correspondentes são:

* [test01.png](analysis/2017-11-13/test01.png)
* [test02.png](analysis/2017-11-13/test02.png)
* [test03.png](analysis/2017-11-13/test03.png)
* [test04.png](analysis/2017-11-13/test04.png)
* [test05.png](analysis/2017-11-13/test05.png)
* [test06.png](analysis/2017-11-13/test06.png)
* [test07.png](analysis/2017-11-13/test07.png)
* [test08.png](analysis/2017-11-13/test08.png)
* [test09.png](analysis/2017-11-13/test09.png)
* [test10.png](analysis/2017-11-13/test10.png)
* [test11.png](analysis/2017-11-13/test11.png)

Situação atual:

* No novo esquema das fontes o BBB irá comandar a rampa, enviando pela serial os setpoint das 4 fontes, a cada passo recebido do sincronismo.
* Nos primeiros testes com o novo esquema foi detectada perda de pontos de rampa. Aparentemente existia um bug do código enviava dados pela serial. As stats eram as seguintes (Patricia): 71 falhas em 235h10min de testes: 0.01ppm ou 0.3 falha/hora. Após a correção do bug: 0 falhas em 166h50min de testes.
* No momento o firmware rodando nos controladores das fontes é temporário. Também o software de comunicação do BBB com os controladores pela serial é temporário e não responde à rede EPICS.
* O erro de tracking linear caiu de ~130 ppm (std) para 30 ppm, no novo esquema com 4000 pontos.


# 2017-11-13 - TESTES PERDA DE PONTOS DE RAMPA

Agora a cada sinal de sincronismo interceptado pelo BBB o IOC ajusta os setpoints das 4 fontes no bastidor. Agora serão 4000 pontos de ramp em 0.5s, ou uma taxa de 8kHz. Inicialmente aconteciam perdas de pontos da rampa após a nova versão do software. Testes de 235h10m apresentaram 71 falhas (0.01 ppm ou 0.3 falha/hora). Descubriu-se um erro na programação da serial que foi corrigido. Após correção nenhuma falha de ramp foi observada em 166h50m de testes.

# 2017-10-06 - TESTE NOVO FIRMWARE FONTES

Uma versão inicial do novo firmware foi testado. Nesta versão um comando de setpoint envia automaticamente setpoints para todas as fontes do bastidor.

> dados: data/test7_17-10-06_1055


# 2017-09-29 - TESTE ENVIO RAMPA COM 4K PONTOS

> dados: data/test_4k.txt


# 2017-09-27 - REPETIBILIDADE DAS MEDIDAS

> dados: data/test5_17-09-27_1442.txt

> dados: data/test6_17-09-27_1442.txt


# 2017-09-27 - REPETIBILIDADE DA RAMPA

> dados: data/test4_17-09-27_1441.txt

> script: [analysis.ipynb](analysis/2017-09-27/analysis.ipynb)

Os parâmetros PI do controlador da fonte foram alterados de ??? (heitor?) para:

<code>P = 3.56</code> (unidades, heitor?)
<code>I = 73.304</code> (unidades, heitor?)

e três novas aquisições de rampa foram realizadas e analisadas. As análises foram  feitas analogamenente àquelas dos dados do dia 2017-09-20. Em resumo houve o seguinte:

* em escala rápida, na região de interesse rampa onde o feixe é acelerado de 150 MeV a 3 GeV, o erro de não linearidade que era de **+/- 200 ppm** caiu para **+/- 135 um**. (ver [Figure_6.png](analysis/2017-09-20/Figure_6.png) de antes e [Figure_6.png](analysis/2017-09-27/test4/Figure_6.png) com novos valores de PI)

* em escala lenta o mesmo comportamento de antes foi observado.

- Figuras:
>  [Figure_1.png](analysis/2017-09-27/test4/Figure_1.png)

>  [Figure_2.png](analysis/2017-09-27/test4/Figure_2.png)

>  [Figure_3.png](analysis/2017-09-27/test4/Figure_3.png)

>  [Figure_4.png](analysis/2017-09-27/test4/Figure_4.png)

>  [Figure_5.png](analysis/2017-09-27/test4/Figure_5.png)

>  [Figure_6.png](analysis/2017-09-27/test4/Figure_6.png)

>  [Figure_7.png](analysis/2017-09-27/test4/Figure_4.png)

>  [Figure_8.png](analysis/2017-09-27/test4/Figure_5.png)

>  [Figure_9.png](analysis/2017-09-27/test4/Figure_6.png)


# 2017-09-22 - REPETIBILIDADE DAS MEDIDAS

> dados: data/test2_17-09-19_1501.txt

> dados: data/test3_17-09-19_1502.txt

> script: [analysis.ipynb](analysis/2017-09-20/analysis.ipynb)

- repetimos as análises de 2017-09-20 dos dados 'teste1' para os dados referentes aos testes 'test2' e 'test3', que foram obtidos minutos após os dados do primeiro teste.
- os resultados se mostraram muito parecidos aos do teste1. a repetibilidade está dentro das variações observadas entre rampas e fontes já do teste1.


# 2017-09-20 - REPETIBILIDADE DA RAMPA

> dados: data/test1_17-09-19_1459.txt

> script: [analysis.ipynb](analysis/2017-09-20/analysis.ipynb)

## Introdução

- No setup experimental atual, no mesmo bastidor de fontes, existem quatro fontes: BO-01U-PS-CH, BO-01U-PS-CV, BO-03U-PS-CH e BO-03U-PS-CV. Para cada uma desta fontes existe um sinal de corrente que é entregue à corretora associada e que pode ser medido em DCCTs independentes e digitalizados. No bastidor existem apenas dois controladores ARM quem lêem a comunicação com o IOC rodando no black beagle bone (BBB). O primeiro controlador repassa os mesmos ajustes de setpoint às fontes  BO-01U-PS-CH e BO-01U-PS-CV enquanto que o segundo controlador o faz para as fontes BO-03U-PS-CH e BO-03U-PS-CV. Os loops de controle das quatro correntes são, no entanto, independentes. (ou apenas as leituras das correntes que são usadas no loop são independentes?)
- Os sinais das correntes de cada par fonte-imã foram digitalizados e salvos em arquivos. Os canais 0,1,2 do digitalizador correspondem respectivamente às correntes das fontes BO-01U-PS-CH, BO-01U-PS-CV e BO-03U-PS-CH.
- O sinal de sincronismo, como gerado pela eletrônica adicional do BBB que transforma pulsos óticos em elétricos, foi digitalizado no quarto canal do digitalizador, aquele de índice 3.
- A função 'add_sync_upborder' no módulo [analysis.py](ps_ramp_tests/analysis.py) identifica as bordas de subida do sinal de sincronismo e uma coluna que marca quando as referências das correntes são atualizadas é adicionada aos dados. Esta última coluna é usada na identificação do início e fim das rampas.


## Rampa completa

- [Figure_1.png](analysis/2017-09-20/Figure_1.png)

## Delay entre valor de referência e valor implementado nas corretoras.

- na região de aceleração do feixe, há uma defasagem temporal de 33 pontos de
  aquisição ([Figure_2.png](analysis/2017-09-20/Figure_2.png)), ou seja, de 660 us. Esta defasagem pode aparentemente
  ser corrigida também através de um aumento dos valores de referẽncia da ordem
  de 22 mA. **gabriel**: *ele diz que o termo 'delay' de 660 us não é exatamente o delay entre o sincronismo gerar o trigger e o DSP conseguir atingir o valor de referência, intervalo este que deve ser bem menor que o intervalo citado. Ele atribui esta diferença ao fato de que provavelmente há erro de offsets e/ou ganhos na leitura da corrente de saída e que vão ser investigados e corrigidos eventualmente.*

## Plateau em alta corrente

- há uma discrepância de 25 mA entre o valor de referência (10A) e o valor atingido pelas fontes, que é da ordem de 9.975A.  ([Figure_3.png](analysis/2017-09-20/Figure_3.png)). **cléber**: *aqui também há calibração de ganho que pode ser realizado para diminuir a discrepância.*
- parece haver um 'drift' quase linear dos valores de corrente na região em que a referência é constante (10A) de duração de 7 ms ([Figure_4.png](analysis/2017-09-20/Figure_4.png)). Este drift neste intervalo temporal é compatível com a constante de tempo dos imãs e ajustes do PI do controlador? **cléber**: *ele suspeita de que este drift seja de origem térmica. enviou um [gráfico](analysis/2017-09-20/PosBurninCorr10.png) mostrando que a estabilização térmica acontece*. **gabriel**: *desconfia de que esta não seja a explicação correta do drift. acha que é devido ao ajuste do PI.*

## Dispersão entre rampas de uma mesma fonte-imã

- Na região de subida da rampa, onde haverá feixe, a dispersão dos valores de corrente entre rampas é da ordem de 50 ppm, no sentido de desvio padrão, e de aproximadamente 400 ppm pico-a-pico. Estes valores são os mesmos, independentemente da fonte-imã. ([Figure_5.png](analysis/2017-09-20/Figure_5.png))
- vê-se que a dispersão é tanto maior quanto maior a derivada temporal do sinal de referência, como pode por ver pelos dois regimes de rampa com dispersões distintas: o de subida e o de descida.

## Erro de tracking linear de uma mesma fonte-imã

- Em seguida analisamos o erro de tracking, expresso em ppm, em relação a uma rampa linear ajustada dos dados na região de interesse, entre 150 MeV e 3 GeV (quando há feixe estocado no booster).
- Nota-se pela [Figure_6.png](analysis/2017-09-20/Figure_6.png) que o erro de tracking linear de cada fonte, definido como a diferença da leitura de uma dada rampa em relação à melhor reta que ajusta a leitura da primeira rampa na região com feixe (entre ~0.77A e ~9.52 no caso dos testes), tem duas escalas de variação: a mais rápida, que é dada pelo intervalo entre sinais de sincronismo, corresponde a uma oscilação com amplitude da ordem +/- 200 ppm ([Figure_7.png](analysis/2017-09-20/Figure_7.png)). A segunda, bem mais lenta,
é da ordem +/- 500 ppm e corresponde a um erro polinomial de ordem superior.

## Erro de tracking linear entre fontes-imãs.

- Em seguida consideramos o erro de tracking linear levando em conta as várias fontes. Este erro foi definido tomando-se a diferença dos valores medidas das correntes de rampa (3 fontes, 19 rampas cada) com relação à melhor reta ajustada a todos os pontos no intervalo.
- pela ([Figure_8.png](analysis/2017-09-20/Figure_8.png)) vê-se que a dispersão entre fontes não aumenta de forma significativa a dispersão de +/- 500 ppm que já existe devido ao comportamento não linear das correntes no intervalo de interesse. Na ([Figure_9.png](analysis/2017-09-20/Figure_9.png)), que é uma ampliação da anterior na região central da região de interesse da rampa, os dados das trẽs fontes já podem ser distinguidos e suas separações (~ 100 ppm) facilmente visualizadas.


## Pendências:

- Erros de tracking linear com escala lenta, do tipo do observado nas medidas com as corretoras do booster (+/- 500 ppm) podem ser mitigados adaptando-se a rampa de referência. Já os erros de escala rápida (+/- 200 ppm) deveriam ser corrigidos no controle da fonte, quer seja através de ajustes do PI, quer seja através de filtros adicionais. **gabriel**: *comentou que acha mais apropriado tentar antes corrigir as várias questões acima calibrando melhor os parâmetros e inputs do controle das fontes.*


# 2017-09-18

- [bug] Problemas ao iniciar o  IOCs
  1. ao rodar o st.cmd do timing o terminal reclama que não encontra uma biblioteca. (**ximenes**: *recompilação resolveu*).
  2. o IOC do BBB não responde aos cagets. (**ximenes**: *entendido e resolvido*)
  3. os problemas de perda de leitura entre IOC/controlador voltaram (**ximenes**: *enntendido e resolvido*).


# 2017-09-15

- [bug] IOC travou. reiniciamos salvando logs de stdout e stderr.
  provavelmente exception em python. **eduardo**: *a 'placa-mãe' com controlador da serial deixou de funcionar após queda de energia e o programa IOC não returnada do comando de inicialização da serial, ficando travado.*
- [bug] o WfmIndex nos controladores estava parado em um valor arbitrário. pq?
  será que interrompemos o sincronismo pelo EVR ao invés do EVG ? (entendido!) **gabriel**: *irá corrigir/rever na próxima versão de firmware*
- [bug?] ao iniciar o BBB lê o valor 2001 do WfmIndex do controlador. após conclusão da rampa com sucesso este valor passar a ser 2000. pq da diferença? **gabriel**: *não pe bug. é consequência do algoritmo de rampa atual.*
- [bug] firmware do controlador não zera WfmIndex durante boot? **gabriel**: *irá corrigir/rever na próxima versão de firmware*
  IOC não deveria ajustar estado do controlador durante o boot.
- [bug] Current-SP e Current-RB, quando escolhido SlowRef após MigWfm ou
  RmpWfm deveria espelhar o CurrentRef-Mon. Mudar spec das PVs. **ximenes**: *será atualizado.*
- enviamos ao IOC/controlador as rampas de acordo com a spec e implementadas em
  siriuspy.magnet.util
- criei repositorio ps-tests no lnls-sirius.
