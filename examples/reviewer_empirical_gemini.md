# Reviewer Report - Empirical Identification & Methods Specialist

## Model: GEMINI
## Manuscript: Board Composition: Balancing Family Influence in S&P 500 Firms
## Agent: Empirical Identification & Methods Specialist
## Date: 2025-07-15 14:51:15

---

**Reviewer Report**

**To:** The Editor, Administrative Science Quarterly  
**From:** Reviewer #2 – Empirical Identification & Methods Specialist  
**Manuscript:** "Board Composition: Balancing Family Influence in S&P 500 Firms"  
**Authors:** Anderson and Reeb

---

This manuscript investigates the role of board composition in mitigating agency conflicts between founding-family shareholders and minority shareholders. The central thesis is that independent directors are particularly valuable in family firms, where they serve to balance the power of the founding family and limit potential expropriation. This contrasts with the mixed evidence on the value of independent directors in widely-held firms, where the primary agency conflict is between managers and shareholders. The authors leverage a panel dataset of S&P 500 firms from 1992-1999 to test their hypotheses.

The paper is well-written, addresses a theoretically important and novel question, and is executed with a high degree of care. The authors are to be commended for the significant effort in manually collecting detailed data on board structure and family involvement. The empirical strategy is thoughtful and includes a number of robustness checks that strengthen the credibility of the findings. However, I have significant concerns regarding the core identification strategy and the claims of causality, particularly concerning the use of instrumental variables. While the correlational evidence presented is compelling, the paper would be substantially improved by a more cautious interpretation of the results and a more rigorous treatment of endogeneity.

### **Brief Summary of the Empirical Approach**

The authors use a panel of 403 S&P 500 firms over the 1992-1999 period. The primary empirical specification is a two-way fixed-effects model (industry and year) regressing a measure of firm performance (Tobin's Q) on various measures of board composition and family influence, along with a standard set of control variables. Key independent variables include a binary indicator for a "family firm," the percentage of independent directors, interaction terms between these two, and a novel measure of the ratio of family directors to independent directors. The authors test for non-linearities using spline regressions. To distinguish between agency and stewardship theories, they examine the role of affiliated directors and the determinants of board independence, using OLS and a two-stage least squares (2SLS) model for the latter. Robustness is assessed using alternative performance measures (EVA), alternative definitions of family influence, outlier-robust regressions, and firm-level fixed effects.

### **Major Strengths**

1.  **Important and Novel Research Question:** The paper smartly shifts the focus from the classic manager-shareholder conflict to the less-studied but highly relevant conflict between large (family) and small (minority) shareholders. This provides a compelling explanation for why independent directors might matter in some contexts but not others, potentially resolving a puzzle in the corporate governance literature.
2.  **High-Quality, Hand-Collected Data:** The manual collection of data on director classification (independent, affiliate, insider), family board representation, and nominating committee composition from proxy statements is a significant undertaking. This detailed data allows for a more nuanced analysis than would be possible with standard databases and is a major contribution of the paper.
3.  **Thoughtful Empirical Tests:** The use of interaction terms (Table 2, Col 4) to test the contingent effect of board independence is the correct approach. The spline regression and corresponding figure (Table 3, Figure 1) provide a very clear and convincing illustration of the hypothesized non-linear relationship between the family/independent director ratio and performance.
4.  **Extensive Robustness Checks:** The authors conduct a battery of tests to show their results are not artifacts of specific choices. The use of firm-level fixed effects (Table 2, Col 5) is particularly important as it controls for time-invariant unobserved firm heterogeneity (e.g., a family's culture or quality), which is a major potential confounder. The fact that the key interaction effect holds in this demanding specification is a significant strength.

### **Major Weaknesses**

1.  **Causal Identification and Endogeneity:** The primary weakness of the manuscript lies in its handling of endogeneity and the resulting claims of causality. While the authors acknowledge the issue and employ techniques like 2SLS, the implementation is not convincing.
    *   **Invalid Instrumental Variables:** The 2SLS analyses described in the "Robustness of Model Specification" section and presented in Table 5 are methodologically flawed. For an instrument to be valid, it must satisfy the exclusion restriction: it can only affect the outcome variable (e.g., Tobin's Q) through its effect on the endogenous variable (e.g., Board Independence). The instruments listed for board independence ("firm age, officer and director ownership..., institutional investors, firm size, prior period performance, growth opportunities") are all standard control variables that are widely believed to have a direct effect on firm performance. They cannot be validly excluded from the second-stage regression. Similarly, in the Table 5 analysis of the nominating committee, instruments like `prior-period performance` and `firm size` almost certainly have a direct effect on the desired level of board independence, violating the exclusion restriction. The use of these instruments does not solve the endogeneity problem and may in fact be worse than the OLS estimates.
    *   **Reverse Causality:** The paper argues that board structure affects performance. However, it is equally plausible that performance affects board structure. For example, a well-performing family firm might feel more secure and thus be more willing to appoint independent directors. Conversely, a poorly performing family firm might face pressure from outside investors to increase board independence. While the firm fixed-effects model mitigates this concern to some extent by analyzing within-firm changes, it does not fully resolve issues of dynamic endogeneity. The authors mention a lagged variable analysis but do not present it; this would be a useful, albeit imperfect, addition.

2.  **Econometric Specification Details:** While generally strong, the econometrics could be updated. The standard in modern panel data analysis is to cluster standard errors at the firm level to account for serial correlation within firms over time. The authors use Huber-White standard errors, which are robust to heteroskedasticity but not to this intra-firm correlation. This could lead to understated standard errors and inflated t-statistics.

### **Specific Detailed Comments**

*   **Section: Method - Data (p. 219):** The definition of a "family firm" as one where the "family continues to have an ownership stake or maintain board seats" is quite broad. It would be helpful to know the minimum threshold for an "ownership stake." While the binary variable is useful for the main interaction tests, the analysis could be enriched by exploring the continuous nature of family influence (e.g., percentage of equity held, percentage of board seats) more directly in the main models, rather than just as a robustness check.

*   **Section: Method - Independent Variables (p. 220):** The use of a spline regression for the ratio of family-to-independent directors is clever. However, the breakpoints (0.50 and 1.00) appear arbitrary. The authors should provide a justification for these specific cutoffs. Were they chosen based on theory, visual inspection of the data, or to maximize fit? This should be clarified.

*   **Section: Results - Table 2 (p. 223):** The firm-level fixed effects model in Column 5 is a crucial test. However, the R-squared of 0.182 is substantially lower than the industry/year FE models (~0.48). This is expected, as firm FEs absorb a great deal of variation. The authors should briefly acknowledge and interpret this, noting that the model explains 18.2% of the *within-firm* variation in industry-adjusted Tobin's Q. The key takeaway—that the interaction term remains significant—is the most important point.

*   **Section: Results - Table 5 (p. 229) & Robustness (p. 231):** As noted in the Major Weaknesses, the 2SLS analysis here is unconvincing. The claim that this analysis "control[s] for possible endogenous effects" is too strong. The authors should either find a more credible, truly exogenous instrument (which is admittedly very difficult) or remove the 2SLS analysis. A more defensible alternative would be to present the results and explicitly discuss the likely violation of the exclusion restriction, framing the analysis as a sensitivity check under strong assumptions rather than a solution to endogeneity.

*   **Section: Results - Table 5 (p. 229):** The finding that institutional ownership is positively associated with board independence is an interesting and important result in its own right. It provides strong circumstantial evidence for the paper's core mechanism: outside shareholders (institutions) push for independent directors to monitor powerful insiders (families). This finding supports the agency interpretation and should be highlighted more prominently.

### **Recommendations for Improvement**

1.  **Re-frame Causal Claims:** The most critical change is to moderate the causal language throughout the manuscript. The evidence strongly supports a *correlation* between a balance of power on the board and firm performance in family firms. The authors should frame their findings in terms of association and consistency with an agency-theoretic framework, rather than definitive causal proof.
2.  **Address the 2SLS Issue:** The authors should remove the 2SLS analyses that rely on invalid instruments. Alternatively, they must provide a much more robust defense of their instruments or, at a minimum, heavily caveat the results and acknowledge the likely violation of the exclusion restriction. Simply stating that the results are "suggestive" would be an improvement.
3.  **Strengthen Econometric Reporting:** Re-run all regression analyses using standard errors clustered at the firm level. This is the current best practice and will provide more conservative and reliable statistical inference.
4.  **Justify Methodological Choices:** Provide a clear rationale for the choice of breakpoints in the spline regression analysis in Table 3.
5.  **Elaborate on Key Mechanisms:** The results in Table 5 regarding the determinants of board independence are very powerful for the paper's narrative. The contrast between families on the nominating committee *reducing* independence and institutional investors *increasing* it is a key piece of evidence. This "battle for the board" narrative could be further developed in the discussion section.

### **Overall Assessment and Recommendation**

This is a very good paper with the potential to be excellent. It asks a novel and important question, uses high-quality data, and presents a series of compelling correlations that are robust to many alternative specifications, including demanding firm fixed-effects models. The primary flaw is the over-reaching on causal claims, particularly through a methodologically weak 2SLS strategy.

This is a remediable issue. The core findings from the OLS and fixed-effects models are valuable and publishable on their own, provided they are interpreted with appropriate caution. The authors need to revise the manuscript to address the identification concerns, primarily by re-framing their claims and removing or heavily caveating the flawed 2SLS analysis.

**Recommendation: Major Revision**

---

*Generated by AI Reviewer System (GEMINI Model)*  
*Agent: Empirical Identification & Methods Specialist*
*Configuration: MAX_TOKENS=8000, TEMPERATURE=0.5*
