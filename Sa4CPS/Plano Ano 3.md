# Sa4CPS: Plano do 3.º Ano (rascunho)

**Contexto:** revisão do 2.º ano com a ITEA. Mensagem principal: passar de dados simulados para produtos/ambientes reais.
**Problema:** a implementação da rede é demasiado instável para atuar sobre ela e os parceiros responsáveis pela rede não são fiáveis.
**Última atualização:** 2026-11-05

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

## Plano trimestral (M25–M36, ajustar ao calendário real)

### T1: Base de dados reais (nov–jan)
- [ ] Inventariar os ativos reais: número de Pis, circuitos medidos, cargas controláveis, kWh/kW da bateria
- [ ] Concluir a instalação dos sensores e criar um dashboard de qualidade de dados e disponibilidade
- [ ] **Começar já a acumular histórico.** FL, previsão e GNN precisam de meses de dados reais; é o item com maior tempo de espera do plano
- [ ] Implementar o Grid Adapter com o backend `emulator`
- [ ] Fechar os itens pendentes da Demo 2: salvaguardas (C10), ativação de flexibilidade, aprendizagem no edge, modelos pessoais
- [ ] Enviar ao coordenador um memorando de risco sobre o parceiro da rede (ver abaixo)

### T2: Fechar o ciclo sobre ativos reais (fev–abr)
- [ ] Ativação de flexibilidade na bateria real e em cargas HA (AVAC, tomadas), acionada por pedidos emulados do DSO e por sinais de preço reais
- [ ] FL nos Pis reais com dados reais do edifício. Manter as habitações virtuais apenas para escala, claramente identificadas como virtuais
- [ ] Modelação de preferências com feedback real dos ocupantes, usando os monitores de secretária como canal de feedback (alimenta também a parte GNN da tese)
- [ ] Estudo com utilizadores n.º 1: resumos XAI testados com ocupantes reais e com o gestor da comunidade

### T3: Validação (mai–jul)
- [ ] Operação contínua sem supervisão durante 4–8 semanas, com KPIs registados automaticamente (evidência para os entregáveis finais)
- [ ] Testes de segurança no caminho de atuação real: tentar comandos maliciosos e verificar que as salvaguardas os bloqueiam
- [ ] Se os dados do parceiro chegarem, usá-los através do backend `replay`. HIL se houver OPAL-RT
- [ ] Estudo com utilizadores n.º 2

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

1. Data de fim do projeto? (assumido: 3.º ano ≈ nov 2026 – out 2027)
2. O que existe no laboratório GECAD? Capacidade da bateria, disponibilidade de OPAL-RT, que AVAC/cargas são realmente controláveis
3. Quantos locais reais estão acessíveis além do GECAD? Mesmo 2–3 habitações reais reforçam muito os resultados de FL
4. Que parceiro é responsável pela rede? (CEL como DSO?) Isto define o nível de escalamento necessário
