# Sa4CPS: Plano do 3.º Ano (rascunho)

**Contexto:** revisão do 2.º ano com a ITEA. Mensagem principal: passar de dados simulados para produtos/ambientes reais.
**Problema:** a implementação da rede é demasiado instável para atuar sobre ela e os parceiros responsáveis pela rede não são fiáveis.
**Última atualização:** 2026-11-05

---

## Dados de partida

- **Fim do projeto:** outubro 2027 (3.º ano ≈ nov 2026 – out 2027)
- **Ativos ISEP:** baterias e algumas cargas controláveis no laboratório GECAD
- **Locais reais:** 2–3 habitações acessíveis
- **Parceiro da rede:** CEL

---

## Mudança principal: deixar de construir o UC4 sobre o parceiro da rede

Os revisores querem dados reais. O parceiro da rede não é fiável. A solução para ambos é a mesma: **colocar a parte real do UC4 sobre ativos que o ISEP controla e tratar a rede como um sinal de entrada, não como algo sobre o qual atuamos.**

- **Real:** edifício(s) GECAD, nós edge Raspberry Pi 5, monitores de secretária, sensores ambientais, banco de baterias e BMS do laboratório, dispositivos Home Assistant (HAGecad). A atuação acontece aqui, em hardware real, com ocupantes reais.
- **Lado da rede:** reduzido a uma interface. Pedidos de flexibilidade entram, respostas saem. Alimentado por um emulador até a rede do parceiro estar estável (e pode ficar emulado).

Narrativa para a ITEA: *"Dispositivos reais, utilizadores reais, atuação real. Os eventos de stress da rede são emulados por um gémeo digital alimentado por injeções reais medidas."* É um argumento sólido para TRL 5–6 em ambiente relevante, e muito melhor do que tudo simulado.

---

## Três níveis de dados

| Nível | Fonte | Estado | Papel |
|---|---|---|---|
| **A** Real, nosso | Contadores GECAD, Pis, sensores, bateria do laboratório, cargas HA | Obrigatório | Demonstração principal. Atuação real |
| **B** Real, parceiros | Dados de contadores CEL / Digitalmente / ENERIM | Desejável | Só leitura, em lote é aceitável, o sistema funciona sem eles |
| **C** Emulado | Estado da rede, eventos de tensão, pedidos do DSO | Aceite | Gémeo pandapower alimentado por A+B. HIL se houver OPAL-RT |

**Sinais externos reais que não dependem de parceiros:** preços diários do OMIE, tarifas ERSE, dados abertos da E-Redes. A flexibilidade acionada por preço é um gatilho do mundo real, por isso nem todas as ativações dependem de um pedido emulado do DSO.

---

## Adaptador da rede (alteração pequena à arquitetura)

O `UC4_Architecture.md` já tem os tópicos `voltage-events` e `flexibility-requests` separados, por isso o lado da rede já está isolado. Acrescentar um único **Grid Adapter** que publica nesses tópicos, com três backends:

- `emulator`: gémeo digital + cenários de stress gerados
- `replay`: dados gravados do parceiro
- `live`: ligação direta ao parceiro

Mudar de backend é uma alteração de configuração. A instabilidade do parceiro deixa de bloquear o trabalho a jusante.

---

## KPIs prometidos: o problema central

| KPI | Inicial | Alvo | Atual | Depende da rede CEL? |
|---|---|---|---|---|
| Consumidores inscritos no programa de flexibilidade | 0 | 10 | 0 | Parcialmente (inscrição, não a rede) |
| Energia transacionada (kWh) | 0 | 20 | 0 | Não |
| N.º de eventos de tensão | 20 | 2 | 20 | Sim |
| Duração média dos problemas de tensão (min) | 30 | 10 | 30 | Sim |
| Tempo médio para resolver problemas de tensão (min) | N/A | 10 | N/A | Não (é o tempo de resposta do nosso sistema) |
| N.º de eventos de capacidade de linha | 45 | 5 | 45 | Sim |
| Duração média dos problemas de capacidade de linha (min) | 45 | 10 | 45 | Sim |
| Tempo médio para resolver problemas de capacidade de linha (min) | N/A | 10 | N/A | Não (é o tempo de resposta do nosso sistema) |

**Leitura:** 4 dos 8 KPIs são alcançáveis só com ativos nossos. Os outros 4 (contagem e duração de eventos) medem o estado de uma rede onde não podemos atuar. A estratégia é manter os nomes e os alvos dos KPIs e **definir explicitamente o método de medição**, em vez de os abandonar.

### Grupo 1: KPIs alcançáveis com ativos reais (garantir)

**Energia transacionada: 0 → 20 kWh**
- O alvo é baixo. As baterias do laboratório chegam lá com poucas ativações.
- Definir "transacionada" = flexibilidade ativada e liquidada no registo da comunidade (pedido → ativação → medição → liquidação).
- Somar ativações por preço (OMIE) e por pedido emulado do DSO, mais deslocamento de cargas nas 2–3 habitações.
- Meta interna: 20 kWh até ao fim do T2, para ter margem; registo contínuo no T3.

**Consumidores inscritos: 0 → 10**
- ISEP: 2–3 habitações + edifício(s)/zonas GECAD como participantes ≈ 4–5.
- CEL: os consumidores potenciais já identificados. Inscrever é um processo administrativo e de consentimento, **não depende da estabilidade da rede**. É um pedido muito mais simples à CEL do que a rede.
- Nós fornecemos o fluxo de inscrição e consentimento (Consent Router, WP5) para retirar trabalho à CEL.
- Prazo limite: inscrições CEL até ao M30. Se falhar, documentar e reportar o valor real (honesto, com justificação).

**Tempo para resolver problemas de tensão / capacidade: N/A → 10 min**
- Isto é a latência da nossa cadeia: deteção → decisão → comando → resposta física → confirmação.
- Medível de ponta a ponta com hardware real: deteção no gémeo (alimentado por injeções reais), comando à bateria real, resposta medida no BMS, confirmação no gémeo.
- 10 min é folgado; a cadeia deve ficar na ordem de segundos a 1–2 min (ciclo de 1 min do gémeo). Instrumentar cada etapa com timestamps.

### Grupo 2: KPIs da rede (contagem e duração de eventos)

**Problema:** reduzir eventos de 20 → 2 e de 45 → 5 exige atuar na rede da CEL, o que não é viável. Além disso, o "valor atual" é igual ao inicial: a linha de base ainda não foi realmente medida.

**Estratégia:**
1. **Linha de base a partir de dados históricos da CEL** (exportação única, ver gestão do parceiro). Fixa os 20 e 45 eventos num período definido (p. ex., por mês) e numa topologia concreta.
2. **Gémeo digital da rede CEL** (pandapower com a topologia e parâmetros da CEL), alimentado por medições reais (habitações + GECAD) e pelo histórico CEL em `replay`.
3. **Avaliação em ciclo fechado:** a atuação é real (baterias, cargas) e o efeito na rede é quantificado no gémeo, com a flexibilidade real escalada ao nível do alimentador. Comparar a operação com e sem Sa4CPS sobre os mesmos dados históricos (contrafactual).
4. **Implementar o cálculo de capacidade de linha** (loading das linhas no pandapower) no T1; está marcado como "por implementar".
5. **Reportar com transparência:** "redução de eventos avaliada sobre gémeo validado com dados reais da CEL e atuação real", não "redução medida na rede".

**Plano B se a CEL não entregar nem dados históricos:** linha de base gerada por cenários no gémeo, com uma topologia de referência (p. ex., rede de teste BT/MT) calibrada com os perfis reais das habitações e do GECAD. Mais fraco, mas defensável se o risco estiver registado.

### Ação formal sobre os KPIs
- Propor ao coordenador, no plano do 3.º ano (D6.5/D6.6), uma **nota de metodologia** para os KPIs do Grupo 2: mantêm-se os alvos, define-se o ambiente de medição (gémeo + replay + atuação real).
- Acrescentar KPIs complementares mensuráveis no ambiente real (disponibilidade, latência, MAPE, redução de pico, taxa de bloqueio das salvaguardas). Não substituem os prometidos, mas reforçam a evidência.

---

## Plano trimestral (M25–M36, ajustar ao calendário real)

### T1: Base de dados reais (nov–jan)
- [ ] Inventariar os ativos reais: número de Pis, circuitos medidos, cargas controláveis, kWh/kW da bateria
- [ ] Concluir a instalação dos sensores e criar um dashboard de qualidade de dados e disponibilidade
- [ ] **Começar já a acumular histórico.** FL, previsão e GNN precisam de meses de dados reais; é o item com maior tempo de espera do plano
- [ ] Implementar o Grid Adapter com o backend `emulator`
- [ ] Fechar os itens pendentes da Demo 2: salvaguardas (C10), ativação de flexibilidade, aprendizagem no edge, modelos pessoais
- [ ] Enviar ao coordenador um memorando de risco sobre o parceiro da rede (ver abaixo)
- [ ] Pedir à CEL: topologia da rede, histórico de eventos (tensão e capacidade) e inscrição dos consumidores identificados
- [ ] Implementar o cálculo de capacidade de linha no gémeo
- [ ] Instrumentar a cadeia de atuação com timestamps (KPI "tempo para resolver")
- [ ] Fluxo de inscrição/consentimento pronto para habitações e consumidores CEL

### T2: Fechar o ciclo sobre ativos reais (fev–abr)
- [ ] Ativação de flexibilidade na bateria real e em cargas HA (AVAC, tomadas), acionada por pedidos emulados do DSO e por sinais de preço reais
- [ ] FL nos Pis reais com dados reais do edifício. Manter as habitações virtuais apenas para escala, claramente identificadas como virtuais
- [ ] Modelação de preferências com feedback real dos ocupantes, usando os monitores de secretária como canal de feedback (alimenta também a parte GNN da tese)
- [ ] Estudo com utilizadores n.º 1: resumos XAI testados com ocupantes reais e com o gestor da comunidade
- [ ] Atingir os 20 kWh transacionados (meta interna)
- [ ] Inscrever as 2–3 habitações e as zonas GECAD no programa de flexibilidade
- [ ] Gémeo da rede CEL com linha de base de eventos (ou plano B com rede de referência)

### T3: Validação (mai–jul)
- [ ] Operação contínua sem supervisão durante 4–8 semanas, com KPIs registados automaticamente (evidência para os entregáveis finais)
- [ ] Testes de segurança no caminho de atuação real: tentar comandos maliciosos e verificar que as salvaguardas os bloqueiam
- [ ] Se os dados do parceiro chegarem, usá-los através do backend `replay`. HIL se houver OPAL-RT
- [ ] Estudo com utilizadores n.º 2
- [ ] Avaliação contrafactual dos eventos de tensão/capacidade (com vs. sem Sa4CPS) no gémeo
- [ ] M30: ponto de decisão sobre inscrições CEL e feed em tempo real

### T4: Demonstração final e entregáveis (ago–out)
- [ ] Demonstração final ao vivo no edifício real, com o nível da rede declarado abertamente como emulado
- [ ] Versões finais dos entregáveis: D3.3v2/D3.4, D4.3v2/D4.4, D5.3v2/D5.4, D6.5/D6.6, D7.5 (confirmar os meses de entrega no anexo FPP)

---

## KPIs medidos no ambiente real

- Disponibilidade (uptime) dos nós e do pipeline
- Latência ponta a ponta
- MAPE da previsão face ao consumo real
- kWh deslocados / redução de pico na bateria e cargas reais
- Taxa de sucesso da atuação
- Taxa de bloqueio das salvaguardas
- Pontuações de compreensão dos utilizadores (XAI)

Evitar KPIs que dependam da rede do parceiro.

---

## Gestão do parceiro da rede

- **Formalizar.** Levantar a questão ao nível do consórcio e registá-la no registo de riscos, com a mitigação (nível de rede emulado). Os revisores penalizam muito menos uma mudança declarada do que um entregável que derrapa sem explicação.
- **Pedir o mínimo:** uma exportação única de dados históricos até ao fim do T1, não um feed em tempo real. É mais fácil para eles entregarem e continua a contar como dados reais.
- **Definir um prazo limite:** se o feed em tempo real não estiver estável por volta do M30, retirar a rede em tempo real do âmbito da demonstração final e registar essa decisão.

---

## Questões em aberto

1. De onde vêm as linhas de base de 20 eventos de tensão e 45 de capacidade? (que rede, que período)
2. Os KPIs de eventos são por mês, por ano, ou no período da demonstração?
3. Capacidade (kWh/kW) das baterias e que cargas exatamente são controláveis
4. O que conta como "consumidor" para a ITEA: habitação, ponto de medição, ou ocupante?
