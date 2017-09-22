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


# 2017-09-22

## REPETIBILIDADE DAS MEDIDAS
-----------------------------

> dados: data/test2_17-09-19_1501.txt

> dados: data/test3_17-09-19_1502.txt

> script: [analysis.ipynb](analysis/2017-09-20/analysis.ipynb)

- repetimos as análises de 2017-09-20 para os dados 'teste1' para os dados referêntes aos dados de 'test2' e 'test3', que foram obtidos minutos após os dados do primeiro teste.
- os resultados se mostraram muito parecidos aos do teste1. a repetibilidade está dentro das variações observadas entre rampas e fontes já do teste1.


# 2017-09-20

## REPETIBILIDADE DA RAMPA
--------------------------

> dados: data/test1_17-09-19_1459.txt

> script: [analysis.ipynb](analysis/2017-09-20/analysis.ipynb)

### Introdução

- No setup experimental atual, no mesmo bastidor de fontes, existem quatro fontes: BO-01U-PS-CH, BO-01U-PS-CV, BO-03U-PS-CH e BO-03U-PS-CV. Para cada uma desta fontes existe um sinal de corrente que é entregue à corretora associada e que pode ser medido em DCCTs independentes e digitalizados. No bastidor existem apenas dois controladores ARM quem lêem a comunicação com o IOC rodando no black beagle bone (BBB). O primeiro controlador repassa os mesmos ajustes de setpoint às fontes  BO-01U-PS-CH e BO-01U-PS-CV enquanto que o segundo controlador o faz para as fontes BO-03U-PS-CH e BO-03U-PS-CV. Os loops de controle das quatro correntes são, no entanto, independentes. (ou apenas as leituras das correntes que são usadas no loop são independentes?)
- Os sinais das correntes de cada par fonte-imã foram digitalizados e salvos em arquivos. Os canais 0,1,2 do digitalizador correspondem respectivamente às correntes das fontes BO-01U-PS-CH, BO-01U-PS-CV e BO-03U-PS-CH.
- O sinal de sincronismo, como gerado pela eletrônica adicional do BBB que transforma pulsos óticos em elétricos, foi digitalizado no quarto canal do digitalizador, aquele de índice 3.
- A função 'add_sync_upborder' no módulo [analysis.py](ps_ramp_tests/analysis.py) identifica as bordas de subida do sinal de sincronismo e uma coluna que marca quando as referências das correntes são atualizadas é adicionada aos dados. Esta última coluna é usada na identificação do início e fim das rampas.


### Rampa completa

- [Figure_1.png](analysis/2017-09-20/Figure_1.png)

### Delay entre valor de referência e valor implementado nas corretoras.

- na região de aceleração do feixe, há uma defasagem temporal de 33 pontos de
  aquisição ([Figure_2.png](analysis/2017-09-20/Figure_2.png)), ou seja, de 660 us. Esta defasagem pode aparentemente
  ser corrigida também através de um aumento dos valores de referẽncia da ordem
  de 22 mA. **gabriel**: *ele diz que o termo 'delay' de 660 us não é exatamente o delay entre o sincronismo gerar o trigger e o DSP conseguir atingir o valor de referência, intervalo este que deve ser bem menor que o intervalo citado. Ele atribui esta diferença ao fato de que provavelmente há erro de offsets e/ou ganhos na leitura da corrente de saída e que vão ser investigados e corrigidos eventualmente.*

### Plateau em alta corrente

- há uma discrepância de 25 mA entre o valor de referência (10A) e o valor atingido pelas fontes, que é da ordem de 9.975A.  ([Figure_3.png](analysis/2017-09-20/Figure_3.png)). **cléber**: *aqui também há calibração de ganho que pode ser realizado para diminuir a discrepância.*
- parece haver um 'drift' quase linear dos valores de corrente na região em que a referência é constante (10A) de duração de 7 ms ([Figure_4.png](analysis/2017-09-20/Figure_4.png)). Este drift neste intervalo temporal é compatível com a constante de tempo dos imãs e ajustes do PI do controlador? **cléber**: *ele suspeita de que este drift seja de origem térmica. enviou um [gráfico](analysis/2017-09-20/PosBurninCorr10.png) mostrando que a estabilização térmica acontece*. **gabriel**: *desconfia de que esta não seja a explicação correta do drift. acha que é devido ao ajuste do PI.*

### Dispersão entre rampas de uma mesma fonte-imã

- Na região de subida da rampa, onde haverá feixe, a dispersão dos valores de corrente entre rampas é da ordem de 50 ppm, no sentido de desvio padrão, e de aproximadamente 400 ppm pico-a-pico. Estes valores são os mesmos, independentemente da fonte-imã. ([Figure_5.png](analysis/2017-09-20/Figure_5.png))
- vê-se que a dispersão é tanto maior quanto maior a derivada temporal do sinal de referência, como pode por ver pelos dois regimes de rampa com dispersões distintas: o de subida e o de descida.

### Erro de tracking linear de uma mesma fonte-imã

- Em seguida analisamos o erro de tracking, expresso em ppm, em relação a uma rampa linear ajustada dos dados na região de interesse, entre 150 MeV e 3 GeV (quando há feixe estocado no booster).
- Nota-se pela [Figure_6.png](analysis/2017-09-20/Figure_6.png) que o erro de tracking linear de cada fonte, definido como a diferença da leitura de uma dada rampa em relação à melhor reta que ajusta a leitura da primeira rampa na região com feixe (entre ~0.77A e ~9.52 no caso dos testes), tem duas escalas de variação: a mais rápida, que é dada pelo intervalo entre sinais de sincronismo, corresponde a uma oscilação com amplitude da ordem +/- 200 ppm ([Figure_7.png](analysis/2017-09-20/Figure_7.png)). A segunda, bem mais lenta,
é da ordem +/- 500 ppm e corresponde a um erro polinomial de ordem superior.

### Erro de tracking linear entre fontes-imãs.

- Em seguida consideramos o erro de tracking linear levando em conta as várias fontes. Este erro foi definido tomando-se a diferença dos valores medidas das correntes de rampa (3 fontes, 19 rampas cada) com relação à melhor reta ajustada a todos os pontos no intervalo.
- pela ([Figure_8.png](analysis/2017-09-20/Figure_8.png)) vê-se que a dispersão entre fontes não aumenta de forma significativa a dispersão de +/- 500 ppm que já existe devido ao comportamento não linear das correntes no intervalo de interesse. Na ([Figure_9.png](analysis/2017-09-20/Figure_9.png)), que é uma ampliação da anterior na região central da região de interesse da rampa, os dados das trẽs fontes já podem ser distinguidos e suas separações (~ 100 ppm) facilmente visualizadas.


### Observações:

- Erros de tracking linear com escala lenta, do tipo do observado nas medidas com as corretoras do booster (+/- 500 ppm) podem ser mitigados adaptando-se a rampa de referência. Já os erros de escala rápida (+/- 200 ppm) deveriam ser corrigidos no controle da fonte, quer seja através de ajustes do PI, quer seja através de filtros adicionais. **gabriel**: *comentou que acha mais apropriado tentar antes corrigir as várias questões acima calibrando melhor os parâmetros e inputs do controle das fontes.*

# 2017-09-18

- [bug] Problemas ao iniciar o  IOCs
  1. ao rodar o st.cmd do timing o terminal reclama que não encontra uma biblioteca. recompilação resolveu.
  2. o IOC do BBB não responde aos cagets.
  3. os problemas de perda de leitura entre IOC/controlador voltaram.


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
