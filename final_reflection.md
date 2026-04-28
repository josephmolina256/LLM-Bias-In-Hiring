# Final Project Reflection

## 1. Assessment

In my proposal, I set out to investigate whether large language models (LLMs) exhibit racial bias in hiring decisions by analyzing how they evaluate identical resumes with different candidate names. The main goal was to empirically test if LLMs, when acting as hiring managers, would show discriminatory patterns based on racial/ethnic name associations.

I believe we largely achieved this objective, though with some important nuances. The project successfully created a comprehensive dataset of 500 name combinations representing five racial/ethnic groups (White, Black, Hispanic, Asian/Pacific Islander, and American Indian/Alaska Native), as detailed in our `names_processing.md` methodology. We used entropy and separation metrics to select names that ranged from highly stereotypical (like "Nguyen" for Asian names) to more ambiguous, ensuring a realistic distribution.

The execution went well in several areas: our modular code structure (split across `config.py`, `utils.py`, and `main.py`) allowed for robust batch processing of LLM evaluations via the Groq API. We implemented comprehensive error handling and partial saving, ensuring we never lost progress even when API calls failed. The data analysis in `data_analysis.ipynb` provided clear statistical insights, showing that resume quality overwhelmingly determined hiring outcomes—strong resumes got 100% hire rates across all racial groups, while weak resumes got near 0%. Please see graphs in that notebook for referece.

However, some aspects didn't go exactly as planned. Our initial expectation was that we'd find clear evidence of racial bias, but the results showed minimal discrimination. Instead of strong anti-Black bias, we found slight favoritism toward Hispanic names (67.66 average score, 63.9% hire rate) compared to Black candidates (66.00 average score, 59.6% hire rate) and White candidates (66.39 average score, 59.3% hire rate). Gender differences were negligible, with male candidates at 60.7% hire rate and female candidates at 61.0% hire rate. This suggests LLMs may be more "fair" than anticipated, though it raises questions about whether our experimental design was sensitive enough to detect subtle biases or if the LLM's training data has already mitigated overt discriminatory patterns.

What didn't work as anticipated was the API reliability. We encountered occasional failures due to rate limits that required implementing retry logic and batch processing. 

## 2. Self-Critique

If I could approach one aspect differently, I'd revise our experimental design to better account for the finding that resume quality dominates hiring decisions. Our results showed that strong resumes received 100% hire rates across all racial and gender groups, while weak resumes received near 0% hire rates, suggesting that the LLM was primarily evaluating content rather than demographic signals. With more time, I would vary the experimental conditions to test whether bias emerges under different circumstances. For example, testing multiple LLMs (GPT-4, Claude, Gemini) could reveal if certain architectures are more prone to bias. Varying temperature settings could show if more creative responses lead to more biased outcomes. Additionally, I would experiment with different prompt structurs such as more ambiguous evaluation criteria or time pressure scenarios to see if bias emerges when the LLM has less clear guidance. The minimal bias we observed might be due to our structured prompts and clear evaluation criteria, so testing less constrained scenarios could provide a more comprehensive understanding of when and how bias manifests in AI hiring tools as well as how companies ought to design their prompts and evaluation criteria to mitigate bias.

## 3. Connection to Course Material

This project directly engages with course themes surrounding algorithmic bias, fairness in
automated decision making, and the ethical implications of AI systems in real world
applications.
A central concept this project explores is proxy variables in discrimination, where seemingly
neutral variables (such as names) act as stand ins for omitted attributes like race or gender. By
testing whether AI systems infer and act on these proxies, this project examines how bias can
persist even when explicit demographic information is removed.
Additionally, this project connects to discussions about the societal impact of deploying AI in
high stakes contexts such as hiring. If language models produce systematically different
outcomes based on names alone, this raises important concerns about equity, accountability,
and the responsible use of AI technologies.
