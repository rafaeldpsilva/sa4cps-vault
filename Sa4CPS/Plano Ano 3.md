# Sa4CPS: Plano do 3.º Ano (rascunho)

**Contexto:** revisão do 2.º ano com a ITEA. Mensagem principal: passar de dados simulados para produtos/ambientes reais.
**Desafio:** a infraestrutura da rede apresenta instabilidade que, de momento, não permite atuar sobre ela com segurança nem garantir a disponibilidade de dados em tempo real.
**Última atualização:** 2026-11-05

---

## Dados de partida

- **Fim do projeto:** outubro 2027 (3.º ano ≈ nov 2026 – out 2027)
- **Ativos disponíveis no laboratório GECAD:** baterias e algumas cargas controláveis
- **Locais reais:** 2–3 habitações acessíveis

---

## Abordagem principal: atuação real sobre ativos controláveis, rede como sinal

Os revisores pedem dados reais. A rede, no estado atual, não permite atuação estável. A resposta a ambos é a mesma: **assentar a parte real do UC4 em ativos controláveis e estáveis, e tratar a rede como um sinal de entrada em vez de um alvo de atuação direta.**

- **Real:** edifício(s) GECAD, nós edge Raspberry Pi 5, monitores de secretária, sensores ambiente, banco de baterias e BMS do laboratório, dispositivos Home Assistant, habitações participantes. A atuação acontece aqui, em hardware real, com ocupantes reais.
- **Lado da rede:** tratado como interface. Pedidos de flexibilidade entram, respostas saem. Alimentado por um emulador enquanto a rede não estiver estável, com ligação aos dados reais assim que possível.

Narrativa para a ITEA: *"Dispositivos reais, utilizadores reais, atuação real. Os eventos de stress da rede são avaliados num digital twin alimentado por injeções reais medidas."*

---

## Três níveis de dados

| Nível                           | Fonte                                                                                                   | Estado                      | Papel                                                               |
| ------------------------------- | ------------------------------------------------------------------------------------------------------- | --------------------------- | ------------------------------------------------------------------- |
| **A** Ativos controláveis       | Contadores GECAD, Pis, sensores, baterias do laboratório, cargas controláveis, habitações participantes | Obrigatório                 | Demonstração principal. Atuação real                                |
| **B** Dados reais da comunidade | Dados de contadores disponibilizados por CEL / Digitalmente / ENERIM                                    | Integrado quando disponível | Só leitura, em lote é aceitável, o sistema funciona com ou sem eles |
| **C** Rede emulada              | Estado da rede, eventos de tensão, pedidos do DSO                                                       | Aceite                      | Digital Twin pandapower alimentado por A+B                          |

**Sinais externos reais adicionais:** preços diários do OMIE, tarifas ERSE, dados abertos da E-Redes. A flexibilidade acionada por preço é um gatilho do mundo real, por isso nem todas as ativações dependem de um pedido emulado do DSO.

---

## Adaptador da rede (alteração pequena à arquitetura)

O `UC4_Architecture.md` já tem os tópicos `voltage-events` e `flexibility-requests` separados, por isso o lado da rede já está isolado. Acrescentar um único **Grid Adapter** que publica nesses tópicos, com três backends:

- `emulator`: digital twin + cenários de stress gerados
- `replay`: dados históricos reais da rede
- `live`: ligação em tempo real à rede

Mudar de backend é uma alteração de configuração. A instabilidade da rede deixa de bloquear o trabalho a jusante, e a passagem para `replay` ou `live` faz-se sem alterações ao resto do sistema.

---

## KPIs prometidos

| KPI | Inicial | Alvo | Atual | Depende da rede? |
|---|---|---|---|---|
| Consumidores inscritos no programa de flexibilidade | 0 | 10 | 0 | Parcialmente (inscrição, não a rede) |
| Energia transacionada (kWh) | 0 | 20 | 0 | Não |
| N.º de eventos de tensão | 20 | 2 | 20 | Sim |
| Duração média dos problemas de tensão (min) | 30 | 10 | 30 | Sim |
| Tempo médio para resolver problemas de tensão (min) | N/A | 10 | N/A | Não (é o tempo de resposta do sistema) |
| N.º de eventos de capacidade de linha | 45 | 5 | 45 | Sim |
| Duração média dos problemas de capacidade de linha (min) | 45 | 10 | 45 | Sim |
| Tempo médio para resolver problemas de capacidade de linha (min) | N/A | 10 | N/A | Não (é o tempo de resposta do sistema) |

**Leitura:** 4 dos 8 KPIs são alcançáveis com os ativos controláveis. Os outros 4 (contagem e duração de eventos) medem o estado da rede, onde a atuação direta ainda não é possível. A estratégia é manter os nomes e os alvos dos KPIs e **definir explicitamente o método de medição**.

### Grupo 1: KPIs alcançáveis com ativos reais

**Energia transacionada: 0 → 20 kWh**
- As baterias do laboratório permitem atingir o alvo com poucas ativações.
- Definir "transacionada" = flexibilidade ativada e liquidada no registo da comunidade (pedido → ativação → medição → liquidação).
- Somar ativações por preço (OMIE) e por pedido emulado do DSO, mais deslocamento de cargas nas habitações participantes.
- Meta interna: 20 kWh até meados de maio (avaliação no D4.4); registo contínuo até julho (D6.6).

**Consumidores inscritos: 0 → 10**
- 2–3 habitações + edifício(s)/zonas GECAD como participantes ≈ 4–5.
- Consumidores potenciais já identificados na comunidade CEL. A inscrição é um processo de consentimento e **não depende da estabilidade da rede**, por isso pode avançar já.
- O fluxo de inscrição e consentimento (Consent Router, WP5) é disponibilizado pela plataforma, simplificando o processo para todos os parceiros.
- Ponto de controlo: M30.

**Tempo para resolver problemas de tensão / capacidade: N/A → 10 min**
- Corresponde à latência da cadeia: deteção → decisão → comando → resposta física → confirmação.
- Medível de ponta a ponta com hardware real: deteção no digital twin (alimentado por injeções reais), comando à bateria real, resposta medida no BMS, confirmação no digital twin.
- A cadeia deve ficar na ordem de segundos a 1–2 min (ciclo de 1 min do digital twin). Instrumentar cada etapa com timestamps.

### Grupo 2: KPIs da rede (contagem e duração de eventos)

**Desafio:** reduzir eventos de 20 → 2 e de 45 → 5 exige atuar sobre a rede, o que a instabilidade atual não permite. Além disso, o "valor atual" é igual ao inicial, pelo que a linha de base precisa de ser consolidada.

**Estratégia:**
1. **Linha de base a partir de dados históricos da rede** (exportação única). Fixa os 20 e 45 eventos num período definido (p. ex., por mês) e numa topologia concreta.
2. **Digital twin da rede** (pandapower com a topologia e parâmetros reais), alimentado por medições reais (habitações + GECAD) e pelo histórico em `replay`.
3. **Avaliação em ciclo fechado:** a atuação é real (baterias, cargas) e o efeito na rede é quantificado no digital twin, com a flexibilidade real escalada ao nível do alimentador. Comparar a operação com e sem Sa4CPS sobre os mesmos dados históricos (contrafactual).
4. **Implementar o cálculo de capacidade de linha** (loading das linhas no pandapower) no T1.
5. **Reportar com transparência:** "redução de eventos avaliada sobre digital twin validado com dados reais da rede e atuação real".

**Alternativa caso os dados históricos não estejam disponíveis a tempo:** linha de base gerada por cenários no digital twin, com uma topologia de referência (p. ex., rede de teste BT/MT) calibrada com os perfis reais das habitações e do GECAD.

### Ação formal sobre os KPIs
- **D1.3v2 (jan 2027):** primeiro veículo formal. Os requisitos revistos refletem a abordagem (ativos reais, rede como sinal) e o método de medição dos KPIs do Grupo 2.
- **D6.5 (abr 2027):** **nota de metodologia** detalhada para os KPIs do Grupo 2: mantêm-se os alvos, define-se o ambiente de medição (digital twin + replay + atuação real).
- **D6.6 (set 2027):** resultados finais de todos os KPIs, com o método declarado.
- Acrescentar KPIs complementares mensuráveis no ambiente real (disponibilidade, latência, MAPE, redução de pico, taxa de bloqueio das salvaguardas). Não substituem os prometidos, mas reforçam a evidência.

---

## Entregáveis do 3.º ano

| Entregável | Data | Tarefas | O que tem de conter deste plano | Evidência necessária até |
|---|---|---|---|---|
| **D1.3v2** Revised Requirements | jan 2027 | T1.3 | Requisitos revistos: ativos reais como base, rede como sinal de entrada, método de medição dos KPIs, requisitos de inscrição/consentimento | Inventário de ativos (dez) |
| **D3.3v2** Designs perception & comprehension | abr 2027 | T3.3, T3.4 | Ingestão de dados reais (Pis, habitações, GECAD), qualidade de dados, deteção de eventos de tensão e capacidade de linha, FL/previsão, XAI | Pipeline real a funcionar (mar) |
| **D4.3v2** Designs status, projections & actions | abr 2027 | T4.1, T4.3, T4.4 | Grid Adapter (3 backends), digital twin com topologia real/referência, ativação de flexibilidade em baterias e cargas reais, dashboard | Ciclo fechado com bateria real (mar) |
| **D5.3v2** Designs trust, security & privacy | abr 2027 | T5.1–T5.4 | Fluxo de inscrição/consentimento, salvaguardas na atuação real, trust scoring em dados reais | Salvaguardas ativas (mar) |
| **D6.5** Plan final experiments & demos | abr 2027 | T6.3, T6.4 | Experiências finais sobre ativos reais, nota de metodologia dos KPIs do Grupo 2, plano da demonstração final | Linha de base dos KPIs fixada (mar) |
| **D3.4** Final solutions & evaluations perception & comprehension | jun 2027 | T3.3, T3.4 | Avaliação com dados reais: MAPE da previsão, FL (real vs. centralizado), deteção de eventos, estudo XAI n.º 1 | Resultados (meados de mai) |
| **D4.4** Final solutions & evaluations status, projections & actions | jun 2027 | T4.1, T4.3, T4.4 | kWh transacionados, tempo para resolver (latência medida), avaliação contrafactual no digital twin | Resultados (meados de mai) |
| **D5.4** Final solutions & evaluations trust, security & privacy | jun 2027 | T5.1–T5.4 | Testes de segurança na atuação real, taxa de bloqueio das salvaguardas, inscrições/consentimentos | Resultados (meados de mai) |
| **D6.6** Final experiments & demonstrations | set 2027 | T6.3, T6.4 | Resultados finais de todos os KPIs, operação contínua, demonstração final, estudo XAI n.º 2 | Operação contínua concluída (jul) |
| **D7.5** Dissemination & exploitation | set 2027 | T7.1 | Publicações (FL com dados reais, estudo XAI, modelação de preferências), demonstrações, exploração | Submissões (jul–ago) |

**Consequências para o calendário:**
- **Abril é o pico:** 4 entregáveis de design/plano no mesmo mês. Os rascunhos devem estar prontos no início de março, por isso o essencial da arquitetura (Grid Adapter, digital twin, consentimento, salvaguardas) tem de estar decidido e implementado em fevereiro.
- **Junho exige avaliações, não só implementação.** D3.4/D4.4/D5.4 precisam de resultados com dados reais até meados de maio. A operação contínua começa em abril, não em maio.
- **D6.6 em setembro fecha os KPIs.** A demonstração final e o registo contínuo de KPIs ficam concluídos até ao fim de julho; agosto serve para redação.
- **M30 = abril 2027**, coincide com o pacote de abril. É o momento natural para o ponto de decisão sobre inscrições e sobre a ligação `live` à rede.
- Outubro fica como margem para revisões e para a revisão final.

---

## Plano trimestral (M25–M36)

### T1: Base de dados reais (nov–jan) → D1.3v2
- [ ] Inventariar os ativos reais: número de Pis, circuitos medidos, cargas controláveis, kWh/kW das baterias (até dez)
- [ ] Concluir a instalação dos sensores e criar um dashboard de qualidade de dados e disponibilidade
- [ ] **Começar já a acumular histórico.** FL, previsão e modelação de preferências precisam de meses de dados reais; é o item com maior tempo de espera do plano
- [ ] Registar a instabilidade da rede no registo de riscos do projeto, com a mitigação proposta
- [ ] Reunir topologia da rede, histórico de eventos (tensão e capacidade) e lista de consumidores a inscrever
- [ ] Implementar o Grid Adapter com o backend `emulator`
- [ ] Implementar o cálculo de capacidade de linha no digital twin
- [ ] Fechar os itens pendentes da Demo 2: salvaguardas (C10), ativação de flexibilidade, aprendizagem no edge, modelos pessoais
- [ ] Fluxo de inscrição/consentimento pronto para habitações e consumidores da comunidade
- [ ] **Entregar D1.3v2** (jan)

### T2: Fechar o ciclo sobre ativos reais (fev–abr) → D3.3v2, D4.3v2, D5.3v2, D6.5
- [ ] Ativação de flexibilidade nas baterias e cargas controláveis, acionada por pedidos emulados do DSO e por sinais de preço reais (fev)
- [ ] Instrumentar a cadeia de atuação com timestamps (KPI "tempo para resolver")
- [ ] FL nos Pis reais com dados reais. Manter as habitações virtuais apenas para escala, claramente identificadas como virtuais
- [ ] Modelação de preferências com feedback real dos ocupantes, usando os monitores de secretária como canal de feedback
- [ ] Inscrever as habitações participantes e as zonas GECAD no programa de flexibilidade
- [ ] Digital twin da rede com linha de base de eventos fixada (ou alternativa com rede de referência) (mar)
- [ ] Rascunhos D3.3v2, D4.3v2, D5.3v2, D6.5 (início de mar)
- [ ] **Iniciar a operação contínua** com registo automático de KPIs (abr)
- [ ] M30: ponto de decisão sobre inscrições e sobre a viabilidade da ligação `live` à rede na demonstração final
- [ ] **Entregar D3.3v2, D4.3v2, D5.3v2, D6.5** (abr)

### T3: Avaliação e validação (mai–jul) → D3.4, D4.4, D5.4
- [ ] Estudo com utilizadores n.º 1: resumos XAI testados com ocupantes reais e com o gestor da comunidade (até meados de mai)
- [ ] Testes de segurança no caminho de atuação real: tentar comandos maliciosos e verificar que as salvaguardas os bloqueiam (até meados de mai)
- [ ] Atingir os 20 kWh transacionados (até meados de mai)
- [ ] Avaliação contrafactual dos eventos de tensão/capacidade (com vs. sem Sa4CPS) no digital twin (até meados de mai)
- [ ] Integrar dados históricos da rede através do backend `replay`
- [ ] **Entregar D3.4, D4.4, D5.4** (jun)
- [ ] Continuar a operação contínua até ao fim de jul (evidência para D6.6)
- [ ] Estudo com utilizadores n.º 2 (jul)
- [ ] Demonstração final (jul)
- [ ] Submeter publicações para D7.5

### T4: Fecho (ago–out) → D6.6, D7.5
- [ ] Consolidar os resultados finais de todos os KPIs (ago)
- [ ] **Entregar D6.6 e D7.5** (set)
- [ ] Preparar a revisão final; out como margem

---

## KPIs complementares medidos no ambiente real

- Disponibilidade (uptime) dos nós e do pipeline
- Latência ponta a ponta
- MAPE da previsão face ao consumo real
- kWh deslocados / redução de pico nas baterias e cargas reais
- Taxa de sucesso da atuação
- Taxa de bloqueio das salvaguardas
- Pontuações de compreensão dos utilizadores (XAI)

---

## Riscos e mitigação

| Risco | Impacto | Mitigação |
|---|---|---|
| Instabilidade da rede impede atuação direta | KPIs de eventos não mensuráveis na rede | digital twin + `replay` + atuação real em ativos controláveis |
| Dados em tempo real da rede indisponíveis | Sem backend `live` | Exportação única de dados históricos; backend `replay` |
| Dados históricos indisponíveis a tempo | Linha de base fraca | Topologia de referência calibrada com perfis reais |
| Inscrições abaixo do alvo | KPI de consumidores incompleto | Fluxo de consentimento disponibilizado pela plataforma; ponto de controlo no M30 |

---

## Questões em aberto

1. De onde vêm as linhas de base de 20 eventos de tensão e 45 de capacidade? (que rede, que período)
2. Os KPIs de eventos são por mês, por ano, ou no período da demonstração?
3. Capacidade (kWh/kW) das baterias e que cargas exatamente são controláveis
4. O que conta como "consumidor" para a ITEA: habitação, ponto de medição, ou ocupante?
