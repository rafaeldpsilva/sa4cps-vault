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

- `emulator`: gémeo digital + cenários de stress gerados
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
- Meta interna: 20 kWh até ao fim do T2, para ter margem; registo contínuo no T3.

**Consumidores inscritos: 0 → 10**
- 2–3 habitações + edifício(s)/zonas GECAD como participantes ≈ 4–5.
- Consumidores potenciais já identificados na comunidade CEL. A inscrição é um processo de consentimento e **não depende da estabilidade da rede**, por isso pode avançar já.
- O fluxo de inscrição e consentimento (Consent Router, WP5) é disponibilizado pela plataforma, simplificando o processo para todos os parceiros.
- Ponto de controlo: M30.

**Tempo para resolver problemas de tensão / capacidade: N/A → 10 min**
- Corresponde à latência da cadeia: deteção → decisão → comando → resposta física → confirmação.
- Medível de ponta a ponta com hardware real: deteção no gémeo (alimentado por injeções reais), comando à bateria real, resposta medida no BMS, confirmação no gémeo.
- A cadeia deve ficar na ordem de segundos a 1–2 min (ciclo de 1 min do gémeo). Instrumentar cada etapa com timestamps.

### Grupo 2: KPIs da rede (contagem e duração de eventos)

**Desafio:** reduzir eventos de 20 → 2 e de 45 → 5 exige atuar sobre a rede, o que a instabilidade atual não permite. Além disso, o "valor atual" é igual ao inicial, pelo que a linha de base precisa de ser consolidada.

**Estratégia:**
1. **Linha de base a partir de dados históricos da rede** (exportação única). Fixa os 20 e 45 eventos num período definido (p. ex., por mês) e numa topologia concreta.
2. **Gémeo digital da rede** (pandapower com a topologia e parâmetros reais), alimentado por medições reais (habitações + GECAD) e pelo histórico em `replay`.
3. **Avaliação em ciclo fechado:** a atuação é real (baterias, cargas) e o efeito na rede é quantificado no gémeo, com a flexibilidade real escalada ao nível do alimentador. Comparar a operação com e sem Sa4CPS sobre os mesmos dados históricos (contrafactual).
4. **Implementar o cálculo de capacidade de linha** (loading das linhas no pandapower) no T1.
5. **Reportar com transparência:** "redução de eventos avaliada sobre gémeo validado com dados reais da rede e atuação real".

**Alternativa caso os dados históricos não estejam disponíveis a tempo:** linha de base gerada por cenários no gémeo, com uma topologia de referência (p. ex., rede de teste BT/MT) calibrada com os perfis reais das habitações e do GECAD.

### Ação formal sobre os KPIs
- Incluir no plano do 3.º ano (D6.5/D6.6) uma **nota de metodologia** para os KPIs do Grupo 2: mantêm-se os alvos, define-se o ambiente de medição (gémeo + replay + atuação real).
- Acrescentar KPIs complementares mensuráveis no ambiente real (disponibilidade, latência, MAPE, redução de pico, taxa de bloqueio das salvaguardas). Não substituem os prometidos, mas reforçam a evidência.

---

## Plano trimestral (M25–M36)

### T1: Base de dados reais (nov–jan)
- [ ] Inventariar os ativos reais: número de Pis, circuitos medidos, cargas controláveis, kWh/kW das baterias
- [ ] Concluir a instalação dos sensores e criar um dashboard de qualidade de dados e disponibilidade
- [ ] **Começar já a acumular histórico.** FL, previsão e modelação de preferências precisam de meses de dados reais; é o item com maior tempo de espera do plano
- [ ] Implementar o Grid Adapter com o backend `emulator`
- [ ] Fechar os itens pendentes da Demo 2: salvaguardas (C10), ativação de flexibilidade, aprendizagem no edge, modelos pessoais
- [ ] Registar a instabilidade da rede no registo de riscos do projeto, com a mitigação proposta
- [ ] Reunir topologia da rede, histórico de eventos (tensão e capacidade) e lista de consumidores a inscrever
- [ ] Implementar o cálculo de capacidade de linha no gémeo
- [ ] Instrumentar a cadeia de atuação com timestamps (KPI "tempo para resolver")
- [ ] Fluxo de inscrição/consentimento pronto para habitações e consumidores da comunidade

### T2: Fechar o ciclo sobre ativos reais (fev–abr)
- [ ] Ativação de flexibilidade nas baterias e cargas controláveis, acionada por pedidos emulados do DSO e por sinais de preço reais
- [ ] FL nos Pis reais com dados reais. Manter as habitações virtuais apenas para escala, claramente identificadas como virtuais
- [ ] Modelação de preferências com feedback real dos ocupantes, usando os monitores de secretária como canal de feedback
- [ ] Estudo com utilizadores n.º 1: resumos XAI testados com ocupantes reais e com o gestor da comunidade
- [ ] Atingir os 20 kWh transacionados (meta interna)
- [ ] Inscrever as habitações participantes e as zonas GECAD no programa de flexibilidade
- [ ] Gémeo da rede com linha de base de eventos (ou alternativa com rede de referência)

### T3: Validação (mai–jul)
- [ ] Operação contínua sem supervisão durante 4–8 semanas, com KPIs registados automaticamente (evidência para os entregáveis finais)
- [ ] Testes de segurança no caminho de atuação real: tentar comandos maliciosos e verificar que as salvaguardas os bloqueiam
- [ ] Integrar dados históricos da rede através do backend `replay`
- [ ] Estudo com utilizadores n.º 2
- [ ] Avaliação contrafactual dos eventos de tensão/capacidade (com vs. sem Sa4CPS) no gémeo
- [ ] M30: ponto de decisão sobre inscrições e sobre a viabilidade da ligação `live` à rede na demonstração final

### T4: Demonstração final e entregáveis (ago–out)
- [ ] Demonstração final ao vivo sobre ativos reais, com o ambiente de avaliação da rede claramente descrito
- [ ] Versões finais dos entregáveis: D3.3v2/D3.4, D4.3v2/D4.4, D5.3v2/D5.4, D6.5/D6.6, D7.5 (confirmar os meses de entrega no anexo FPP)

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
| Instabilidade da rede impede atuação direta | KPIs de eventos não mensuráveis na rede | Gémeo digital + `replay` + atuação real em ativos controláveis |
| Dados em tempo real da rede indisponíveis | Sem backend `live` | Exportação única de dados históricos; backend `replay` |
| Dados históricos indisponíveis a tempo | Linha de base fraca | Topologia de referência calibrada com perfis reais |
| Inscrições abaixo do alvo | KPI de consumidores incompleto | Fluxo de consentimento disponibilizado pela plataforma; ponto de controlo no M30 |

---

## Questões em aberto

1. De onde vêm as linhas de base de 20 eventos de tensão e 45 de capacidade? (que rede, que período)
2. Os KPIs de eventos são por mês, por ano, ou no período da demonstração?
3. Capacidade (kWh/kW) das baterias e que cargas exatamente são controláveis
4. O que conta como "consumidor" para a ITEA: habitação, ponto de medição, ou ocupante?
