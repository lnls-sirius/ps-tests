Notas:

- senha do usuário fac: boo500mev
- não fechar laptop de aquisição pelo labview! (se fechar, comunicar com gabriel)
- os dados da aquisição deverão ser gravados no centaurus/Troce e acessados como
  um recurso samba do domínio. para montar:
  sudo mount -t cifs -o username=ximenes.resende //centaurus/Repositorio/Troca/testes_fontes_sirius /home/fac/troca/
- o script de aquisição e análise é o 'lnls-ramp-test.py'
- para rodar o IOC de timing:
  cd /home/fac/Desktop/lnls105-controle/sirius-timing-ioc; make clean; make uninstall; make install
  cd iocBoot/ioctiming/; ./st.cmd
- IOC das fontes é iniciado automaticamente com o BBB (root@10.0.21.89 senha root)
- o script de aquisição e análise é o 'lnls-ramp-test.py', instalado no sistema.


2017-09-20


Análise das Medidas
==================

REPETIBILIDADE DA RAMPA (para cada par fonte|imã)
-------------------------------------------------------

dados: data/test1_17-09-19_1459.txt
script: analysis/2017-09-20/analysis.ipynb

a) rampa completa

- [Figure_1.png]

b) delay entre valor de referẽncia e valor implementado nas corretoras.

- na região de aceleração do feixe, há uma defasagem temporal de 33 pontos de
  aquisição (Figure_2.png), ou seja, de 660 us. Esta defasagem pode aparentemente
  ser corrigida também através de um aumento dos valores de referẽncia da ordem
  de 22 mA.

c) plateau em alta corrente

- há uma discrepância de 25 mA entre o valor de referência (10A) e o valor atingido pelas
  fontes, que é da ordem de 9.975A. (Figure_3.png)

- parece haver um 'drift' quase linear dos valores de corrente na região em
  que a referência é constante (10A) de duração de 7 ms 9Figure_4.png).
  Este drift neste Intervalo temporal é compatível com a constante de tempo dos
  imãs e ajustes do PI do controlador?

  d) observações:

  - talvez para cada par fonte|imã deveríamos 'calibrar' a curva nominal de exci
  tação antes de utilizá-la na rampa, de forma a garantir que 1) fosse o mais linear
  possível durante o intervalo com feixe, 2) fossem o mais sincronizadas possível
  em relação ao pulso de início de rampa.






2017-09-18

- [bug] Problemas ao iniciar o  IOCs
  a) ao rodar o st.cmd do timing o terminal reclama que não encontra uma biblioteca. recompilação resolveu.
  b) o IOC do BBB não responde aos cagets.
  c) os problemas de perda de leitura entre IOC/controlador voltaram.


2017-09-15

- [bug] IOC travou. reiniciamos salvando logs de stdout e stderr.
  provavelmente exception em python.
- [bug] o WfmIndex nos controladores estava parado em um valor arbitrário. pq?
  será que interrompemos o sincronismo pelo EVR ao invés do EVG ?
- [bug] ao iniciar o BBB lê o valor 2001 do WfmIndex do controlador.
  após conclusão da rampa com sucesso este valor passar a ser 2000. pq da diferença?
- [bug] firmware do controlador não zera WfmIndex durante boot?
  IOC não deveria ajustar estado do controlador durante o boot.
- [bug] Current-SP e Current-RB, quando escolhido SlowRef após MigWfm ou
  RmpWfm deveria espelhar o CurrentRef-Mon. Mudar spec das PVs.
- enviamos ao IOC/controlador as rampas de acordo com a spec e implementadas em
  siriuspy.magnet.util
- criei repositorio ps-tests no lnls-sirius.
