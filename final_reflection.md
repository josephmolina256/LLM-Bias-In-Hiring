# Final Project Reflection

## 1. Assessment

In my proposal, I set out to investigate whether large language models (LLMs) exhibit racial bias in hiring decisions by analyzing how they evaluate identical resumes with different candidate names. The core goal was to empirically test if LLMs, when acting as hiring managers, would show discriminatory patterns based on racial/ethnic name associations.

I believe we largely achieved this objective, though with some important nuances. The project successfully created a comprehensive dataset of 500 name combinations representing five racial/ethnic groups (White, Black, Hispanic, Asian/Pacific Islander, and American Indian/Alaska Native), as detailed in our `names_processing.md` methodology. We used entropy and separation metrics to select names that ranged from highly stereotypical (like "Nguyen" for Asian names) to more ambiguous, ensuring a realistic distribution.

The execution went well in several areas: our modular code structure (split across `config.py`, `utils.py`, and `main.py`) allowed for robust batch processing of LLM evaluations via the Groq API. We implemented comprehensive error handling and partial saving, ensuring we never lost progress even when API calls failed. The data analysis in `data_analysis.ipynb` provided clear statistical insights, showing that resume quality overwhelmingly determined hiring outcomes—strong resumes got 100% hire rates across all racial groups, while weak resumes got near 0%.

However, some aspects didn't go exactly as planned. Our initial expectation was that we'd find clear evidence of racial bias, but the results showed minimal discrimination. Instead of strong anti-Black bias, we found slight favoritism toward Hispanic names and no significant bias against other groups. This suggests LLMs may be more "fair" than anticipated, though it raises questions about whether our experimental design was sensitive enough to detect subtle biases.

What didn't work as anticipated was the API reliability—we encountered occasional failures that required implementing retry logic and batch processing. Additionally, our name selection methodology, while statistically sound, may have been too conservative in choosing highly stereotypical names, potentially masking real-world bias patterns.

## 2. Self-Critique

If I could approach one aspect differently, I'd revise our name selection strategy. While our entropy-based approach was mathematically rigorous, it prioritized statistical ambiguity over real-world relevance. For instance, we selected names like "Edward" and "Michelle" for their high entropy (meaning they're common across races), but these might not trigger the same unconscious biases that more distinctive names would. 

I'd instead incorporate real-world hiring data or conduct preliminary surveys to identify names that actually correlate with hiring discrimination in practice. This would make our experiment more ecologically valid and potentially reveal biases that our current approach missed. The statistical purity of our method, while academically sound, may have created an artificial scenario that doesn't reflect how bias actually manifests in hiring contexts.

## 3. Connection to Course Material

This project deeply engaged with the course's theme of algorithmic fairness and the hidden assumptions embedded in AI systems. Throughout the semester, we discussed how seemingly neutral algorithms can perpetuate societal biases through training data and design choices. My project brought this abstract concept into concrete practice.

Initially, I approached bias as something obvious and detectable—assuming LLMs would clearly favor certain names. But the results challenged this assumption, showing that when given clear evaluation criteria, the LLM focused on resume content rather than demographic signals. This shifted my perspective from viewing AI bias as inevitable to understanding it as contingent on system design and prompting.

The project reinforced Crawford's argument about the "myth of neutrality" in AI, but also highlighted the potential for mitigation through careful engineering. Our findings suggest that explicit instructions and structured evaluation frameworks can reduce, though not eliminate, biased outcomes. This experience made me more optimistic about addressing AI ethics through technical solutions, while remaining vigilant about the limitations of any single approach.

(Word count: 587)</content>
<parameter name="filePath">c:\Users\josep\Documents\ethics\LLM-Bias-In-Hiring\final_reflection.md