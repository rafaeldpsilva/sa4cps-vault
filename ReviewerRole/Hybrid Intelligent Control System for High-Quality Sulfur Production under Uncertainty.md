# Review: ICSC26_0042 "Hybrid Intelligent Control System for High-Quality Sulfur Production under Uncertainty"

The manuscript proposes a hybrid intelligent system for a Claus-type sulfur production unit (Atyrau refinery). An adaptive neuro-fuzzy inference system (ANFIS) predicts sulfur yield, sulfur recovery degree and SO₂ concentration from six process variables, and a genetic algorithm (GA) then searches for operating conditions that maximize a weighted combination of these outputs. The authors report a coefficient of determination of 0.992 on test data, a 1.3% increase in sulfur yield, a 36% reduction in SO₂ concentration, and better performance than a PID controller and a standalone ANFIS model. The topic is relevant to industry and the manuscript is generally easy to follow. However, the origin of the dataset, the way the evaluation was set up, and the link between the claimed contributions (control, uncertainty handling, fuzzy multi-criteria decision making, Pareto analysis) and what is actually presented all need substantial clarification. The state of the art is also thin, and several references appear unrelated to the topic or have incorrect publication years.

## Title and abstract

- The title refers to a "Control System", but the manuscript describes a steady-state prediction model combined with offline optimization of operating points. No closed-loop structure, process dynamics, time delays or control-action trajectories are presented, even though time delays are listed in the Introduction as a key difficulty. Please either justify the term "control system" or consider a title closer to the content (e.g., "ANFIS–GA-based modeling and optimization of ...").
- Similarly, "under Uncertainty" suggests an explicit treatment of uncertainty (fuzzy or stochastic). Apart from one sentence about 15% disturbances in the Discussion, uncertainty is not modeled or evaluated. Please clarify how uncertainty is handled in the formulation, or revise the title.
- The abstract uses the acronym "ANFIS" ("The ANFIS model was trained...") after spelling it out only in an earlier sentence in a different form. Please avoid acronyms in the abstract.
- The abstract lists a "Sugeno fuzzy inference module" as a component separate from ANFIS. ANFIS as described in Section II is itself a Sugeno-type system. Please clarify whether a third, separate module exists and, if so, describe it in the methodology.
- The abstract states that results "improve the prediction accuracy", "reduce the model mean squared error" and are "robust to uncertainty" without quantitative values or a baseline. Please add the main numerical results and what they are compared against.
- The abstract describes the data as "a set of process data reflecting the actual operating ranges". Please state clearly whether these are real plant measurements or synthetically generated samples (see also the comments on the case study).

## Introduction and state of the art

- The manuscript has no dedicated related-work section. The Introduction cites broad textbooks on fuzzy systems, neural networks and evolutionary algorithms, but it does not review existing data-driven modeling, soft sensing and optimization work for sulfur recovery / Claus units (e.g., neural-network soft sensors for sulfur recovery units, artificial intelligence surrogate models such as [12], or ANFIS–GA hybrids for chemical processes). Without this review, the novelty claim ("integrates ANFIS, a genetic algorithm, and fuzzy multi-criteria decision making") cannot be assessed. Please add a state-of-the-art section and explicitly position the contribution against the closest existing approaches.
- The statement that conventional PID-based systems "are unable to account for uncertainty ... or adapt in real time" is strong and has no citation. Advanced process control and model predictive control are widely used in sulfur recovery units. Please support this statement with references or soften it.
- The claim that combining ANFIS and GA "provides high prediction accuracy and high-quality control decisions" is presented as established fact in the Introduction, before any evidence. Please support it with citations or reframe it as a hypothesis of the study.
- "Fuzzy multi-criteria decision making" is claimed as part of the novelty in both the Introduction and the Conclusions, but the optimization uses a plain weighted sum of the outputs. Please describe the fuzzy multi-criteria decision-making component, or remove it from the contribution statement.
- Section II lists expert-assessment methods [24, 25] and a "fuzzy knowledge base" as part of the methodology, but neither is used later in the manuscript. Please clarify where expert knowledge enters the model.

## Methodology

- The architecture lists four modules (pre-processing, ANFIS, GA, control-action generation). Only ANFIS and GA are described. Please describe the pre-processing module (beyond min–max normalization) and the control-action generation module, ideally with a block diagram of the whole system.
- ANFIS as written produces a single output, while the system has three outputs (y₁, y₂, y₃). Please clarify whether three separate ANFIS models were trained, or a multi-output variant was used.
- With 6 inputs, 3 Gaussian membership functions per input and grid partitioning, the model has 729 rules and 729 × 7 = 5103 linear consequent parameters, plus 36 premise parameters. This is far more than the 750 training samples reported. Please explain how this underdetermined least-squares problem was solved (regularization, rule pruning, subtractive clustering, etc.) and how overfitting was avoided.
- The linguistic terms are given in Russian ("Низкий, Средний, Высокий"). Please translate them (Low, Medium, High).
- The role of the GA is described inconsistently. Section II says the GA searches for optimal operating modes after training, while Section III says "the model parameters were optimized using the proposed genetic algorithm" and the Introduction says the GA tunes membership functions and the rule base. Please clarify whether the GA is used for model training, for operating-point optimization, or for both.
- The chromosome includes the H₂S content (x₃) and the acid gas feed flow rate (x₆). These are usually disturbances or upstream conditions, not variables the operator can manipulate. Please clarify which variables are manipulated, and give the lower/upper bounds and process constraints used during optimization.
- The weights α₁, α₂, α₃ are not reported, and the outputs have different units and scales (% and ppm). Please report the weight values and explain whether the outputs were normalized before being combined in the fitness function.
- The symbol λ is used both for the excess air ratio (x₅) and for the crossover coefficient. Please use a different symbol for one of them.
- Several parameters are not reported: the mutation variance σ², the tolerance ε, the learning rate η, the number of generations, and the range of the crossover coefficient. Please add them for reproducibility.
- In Section III the root mean square error (RMSE) is defined as the quantity being minimized, while Section II defines the objective J as the mean squared error (MSE). Please make the definitions consistent. Also note that "MSE" is used in Section III before being spelled out.
- Equations are not numbered. Please number them so they can be referenced.

## Case study and data

- The dataset is described as "formed from the process-parameter ranges specified by the operating conditions of the SPU", which suggests synthetic samples. However, Table 1 refers to "actual sulfur-yield values obtained experimentally". Please state clearly whether the 1000 observations are plant measurements, laboratory measurements, or simulated data. If simulated, please describe the model that generated the output values (y₁, y₂, y₃), since this strongly affects how the reported accuracy should be interpreted.
- Please describe the dataset in more detail: sampling period, ranges and distributions of each variable, how missing or faulty measurements were handled, and whether the train/test split was random or chronological. A random split of time-series plant data can overestimate accuracy.
- If possible, please make the dataset (or an anonymized version) publicly available, or validate the approach on a public benchmark (e.g., the publicly available sulfur recovery unit dataset by Fortuna et al.), to allow comparison with other methods.

## Results and discussion

- Figure 1 shows only the training curve. The statement that there are "no signs of overfitting" cannot be supported without the validation/test error over epochs. Please add the test curve. Also, the plotted MSE drops from about 0.48 to about 0.025 (roughly 19-fold), not 17-fold as stated. Please check this value.
- Table 1 and Figure 2 show only 8 test samples out of the 250 reported. Please explain how these samples were selected, and show the scatter plot for the whole test set and for each of the three outputs.
- Table 2 does not say which output the metrics refer to, or whether RMSE and MAE are in normalized or physical units. In addition, the mean relative error in Table 1 (0.11%) differs from the MAPE in Table 2 (0.23%). Please clarify.
- The "before optimization" values in Table 3 (97.8% yield, 295 ppm SO₂) differ from the PID baseline in Table 4 (97.2%, 326 ppm). Please explain where each baseline comes from (historical plant average, a specific operating point, a simulation, etc.).
- The improvements in yield and recovery (97.8% to 99.1%, 98.3% to 99.6%) are increases of 1.3 percentage points, not 1.3%. Please correct the wording.
- The optimized values in Table 3 are ANFIS predictions at the GA-selected operating point, so they are evaluated by the same model that was optimized. Please clarify whether any of these optimal operating points were checked independently (plant trial, first-principles simulator, or held-out data near the suggested point). Otherwise, please present the results as model-predicted improvements and discuss the risk of the optimizer exploiting model errors, especially outside the training data range.
- Table 4 reports an RMSE for a PID controller. RMSE is a prediction-accuracy metric, and a PID controller does not produce predictions. Please explain how the PID controller was implemented and simulated (plant model, tuning, setpoints, controlled and manipulated variables), and what the RMSE refers to in this case.
- The Pareto front in Figure 3 shows sulfur yield decreasing as SO₂ concentration increases. Since the goal is to maximize yield and minimize SO₂, the point at about 188 ppm / 99.2% dominates all other points, so the curve does not represent a trade-off. Please check this figure. In addition, a weighted-sum single-objective GA does not directly produce a Pareto front. Please explain how the front was obtained (weight sweep, NSGA-II, etc.).
- The Pareto analysis states that increasing yield above 99.2% "is accompanied by higher energy consumption". Energy consumption is not an input, output or objective of the model. Please explain how this conclusion was reached or remove it.
- The robustness claim ("when the level of random disturbances was increased to 15%, the deterioration in prediction accuracy was insignificant") is not supported by any result, and the test is not described in the methodology. Please describe the experiment (how noise was added, to which variables) and report the quantitative results.
- The discussion would benefit from a comparison with other data-driven models commonly used for this type of problem (e.g., multilayer perceptron, Gaussian process regression, gradient boosting) and other optimizers (e.g., particle swarm optimization, NSGA-II), rather than only PID control and a standalone ANFIS.
- The Discussion repeats the Pareto-front paragraph almost word for word from earlier in Section III. Please remove the duplicate.
- The Conclusions state that the system "improves the quality of the sulfur production process and reduces the environmental burden". Given the comments above (data origin, self-evaluation by the same model, missing robustness results), please temper these conclusions so they reflect what was actually shown.

## References

- Several citations group many references together (e.g., [4–14], [2, 7–9, 20, 21], [4–6, 22, 23]). Please avoid lumping references and explain what each cited work contributes.
- Several references seem unrelated to the statements they support: [5] (selenium adsorption on biochar), [13] (foreign exchange rate risk), [18] (axial-flow compressor aerodynamics, cited for "experimental research methods"), [24] (smart contract security), [25] (social network analysis) and [28] (error estimates for a parabolic equation, cited for the RMSE definition). Please replace them with references relevant to sulfur recovery, process modeling and the specific methods used.
- Several publication years appear incorrect: [9] (Munakata, published 2008), [11] (Journal of Bionic Engineering vol. 7, 2010), [13] (IFAC Proceedings vol. 28, 1995), [25] (AISC vol. 128, 2012) and [29] (PPSN XI, LNCS 6238, 2010). Please verify all reference details. Once corrected, several of these references are older than they appear.
- Five of the 30 references (about 17%) are by the authors ([2], [3], [8], [17], [27]), and most address other refinery units (hydrotreating, delayed coking, catalytic reforming). Please make sure each self-citation is directly relevant.
- References [19] and [26] (a textbook and the plant's internal technological regulations) are not easily accessible to readers. Please add accessible sources where possible.

## Formatting and language

- "INTDUCTION" should be "INTRODUCTION".
- The axis labels of Figure 3 are in Russian ("Выход серы, %", "Концентрация SO₂, ppm"). Please translate them into English.
- In the variable definitions after the crossover equation, the Russian conjunction "и" appears instead of "and".
- Decimal commas and decimal points are mixed in Tables 1, 3 and 4. Please use decimal points throughout.
- There are repeated punctuation marks and stray dashes in many places (e.g., "𝑅𝑖 ,,", "𝑥1 ,,", "(𝑅2 )..", "𝑦1 ;,", "− [0; 1], ,"). Please proofread the whole manuscript.
- The stopping criterion is introduced as "condition [29]". This reads as if [29] were an equation number. Please rephrase.
- Please make the table caption style consistent with the conference template (e.g., "TABLE I. ...").
- Acknowledgment: "This research was supported the Science Committee" should be "supported by the Science Committee", and "Higer" should be "Higher". There is also a misplaced quotation mark before "Kazakhstan".
