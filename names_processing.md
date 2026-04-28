Dataset:
https://www.kaggle.com/datasets/jamescalvinmeaders/gender-and-race-data-for-names 


Each entry in these datasets gives P(Name|Gender,Race) for first or middle names.
Last names have only race data each entry is P(Name|Race).
We also have counts for each name, which we can use to filter out names that are too rare to be meaningful.



```python
import pandas as pd

first_df = pd.read_csv('data/first_name_probabilities.csv')
first_counts_df = pd.read_csv('data/first_name_counts.csv')
last_df = pd.read_csv('data/last_name_probabilities.csv')
last_counts_df = pd.read_csv('data/last_name_counts.csv')

# Normalize names
first_df["name"] = first_df["name"].str.upper()
first_counts_df["name"] = first_counts_df["name"].str.upper()
last_df["name"] = last_df["name"].str.upper()
last_counts_df["name"] = last_counts_df["name"].str.upper()
```

We will only be using firt names which have at least 10000 occurrences and last names with at least 100000 occurrences in the dataset, to ensure that we are working with names that are common enough to be meaningful in our analysis. This will help us avoid noise and outliers in our data, and focus on names that are more likely to be encountered in real-world hiring scenarios.


```python
# Only keep last names that appear at least 10000 times in the dataset
# Counts columns name	white	black	api	aian	hispanic

first_counts_df = first_counts_df[
    (
        first_counts_df["fwhite"] + 
        first_counts_df["fblack"] + 
        first_counts_df["fapi"] + 
        first_counts_df["faian"] + 
        first_counts_df["fhispanic"] +
        first_counts_df["mwhite"] + 
        first_counts_df["mblack"] + 
        first_counts_df["mapi"] + 
        first_counts_df["maian"] + 
        first_counts_df["mhispanic"]
    ) >= 10000]

last_counts_df = last_counts_df[
    (
        last_counts_df["white"] + 
        last_counts_df["black"] + 
        last_counts_df["api"] + 
        last_counts_df["aian"] + 
        last_counts_df["hispanic"]
    ) >= 100000]

first_df = first_df.merge(first_counts_df[["name"]], on="name", how="inner")
print(len(first_df))

last_df = last_df.merge(last_counts_df[["name"]], on="name", how="inner")
print(len(last_df))
```

    413
    307
    

We calculate gender for first names by comparing the probabilities of the name being associated with male or female, and assigning the gender based on which probability is higher. We also calculate a confidence score for the gender assignment, which is based on the difference between the probabilities of the name being associated with male or female, normalized by the total probability of the name being associated with either gender. This confidence score gives us an indication of how strongly a name is associated with a particular gender.


```python
first_df_cols = set(first_df.columns)
last_df_cols = set(last_df.columns)

# Columns in first_df: {'faian', 'fhispanic', 'api', 'mhispanic', 'mapi', 'mblack', 'maian', 'name', 'black', 'mwhite', 'white'}
# Columns in last_df: {'api', 'hispanic', 'aian', 'name', 'black', 'white'}
new_first_df = pd.DataFrame({
    "name": first_df["name"],
    "hispanic": first_df["fhispanic"] + first_df["mhispanic"],
    "black": first_df["fblack"] + first_df["mblack"],
    "api": first_df["fapi"] + first_df["mapi"],
    "white": first_df["fwhite"] + first_df["mwhite"],
    "aian": first_df["faian"] + first_df["maian"],
    "gender": first_df.apply(lambda row: "female" if row["fhispanic"] + row["fblack"] + row["fapi"] + row["faian"] + row["fwhite"] > row["mhispanic"] + row["mblack"] + row["mapi"] + row["maian"] + row["mwhite"] else "male", axis=1),
    "gender_confidence": abs((first_df["fhispanic"] + first_df["fblack"] + first_df["fapi"] + first_df["faian"] + first_df["fwhite"]) - (first_df["mhispanic"] + first_df["mblack"] + first_df["mapi"] + first_df["maian"] + first_df["mwhite"])) / (first_df["fhispanic"] + first_df["fblack"] + first_df["fapi"] + first_df["faian"] + first_df["fwhite"] + first_df["mhispanic"] + first_df["mblack"] + first_df["mapi"] + first_df["maian"] + first_df["mwhite"])
})

print("Old First Name Probabilities:")
print(first_df.head())
print("\nNew First Name Probabilities:")
print(new_first_df.head())

first_df = new_first_df

```


    ---------------------------------------------------------------------------

    KeyError                                  Traceback (most recent call last)

    File c:\Users\josep\Documents\ethics\LLM-Bias-In-Hiring\.venv\Lib\site-packages\pandas\core\indexes\base.py:3641, in Index.get_loc(self, key)
       3640 try:
    -> 3641     return self._engine.get_loc(casted_key)
       3642 except KeyError as err:
    

    File pandas/_libs/index.pyx:168, in pandas._libs.index.IndexEngine.get_loc()
    --> 168 'Could not get source, probably due dynamically evaluated source code.'
    

    File pandas/_libs/index.pyx:197, in pandas._libs.index.IndexEngine.get_loc()
    --> 197 'Could not get source, probably due dynamically evaluated source code.'
    

    File pandas/_libs/hashtable_class_helper.pxi:7668, in pandas._libs.hashtable.PyObjectHashTable.get_item()
    -> 7668 'Could not get source, probably due dynamically evaluated source code.'
    

    File pandas/_libs/hashtable_class_helper.pxi:7676, in pandas._libs.hashtable.PyObjectHashTable.get_item()
    -> 7676 'Could not get source, probably due dynamically evaluated source code.'
    

    KeyError: 'fhispanic'

    
    The above exception was the direct cause of the following exception:
    

    KeyError                                  Traceback (most recent call last)

    Cell In[106], line 8
          4 # Columns in first_df: {'faian', 'fhispanic', 'api', 'mhispanic', 'mapi', 'mblack', 'maian', 'name', 'black', 'mwhite', 'white'}
          5 # Columns in last_df: {'api', 'hispanic', 'aian', 'name', 'black', 'white'}
          6 new_first_df = pd.DataFrame({
          7     "name": first_df["name"],
    ----> 8     "hispanic": first_df["fhispanic"] + first_df["mhispanic"],
          9     "black": first_df["fblack"] + first_df["mblack"],
         10     "api": first_df["fapi"] + first_df["mapi"],
         11     "white": first_df["fwhite"] + first_df["mwhite"],
    

    File c:\Users\josep\Documents\ethics\LLM-Bias-In-Hiring\.venv\Lib\site-packages\pandas\core\frame.py:4378, in DataFrame.__getitem__(self, key)
       4374 
       4375         if is_single_key:
       4376             if self.columns.nlevels > 1:
       4377                 return self._getitem_multilevel(key)
    -> 4378             indexer = self.columns.get_loc(key)
       4379             if is_integer(indexer):
       4380                 indexer = [indexer]
       4381         else:
    

    File c:\Users\josep\Documents\ethics\LLM-Bias-In-Hiring\.venv\Lib\site-packages\pandas\core\indexes\base.py:3648, in Index.get_loc(self, key)
       3643     if isinstance(casted_key, slice) or (
       3644         isinstance(casted_key, abc.Iterable)
       3645         and any(isinstance(x, slice) for x in casted_key)
       3646     ):
       3647         raise InvalidIndexError(key) from err
    -> 3648     raise KeyError(key) from err
       3649 except TypeError:
       3650     # If we have a listlike key, _check_indexing_error will raise
       3651     #  InvalidIndexError. Otherwise we fall through and re-raise
       3652     #  the TypeError.
       3653     self._check_indexing_error(key)
    

    KeyError: 'fhispanic'


To better understand the probabilities, P(Name|Race), we can look at an example of the last name Nguyen. The dataset gives us the following probabilities for the last name Nguyen:

- P(Name=Nguyen|Race=White) = 0.000036
- P(Name=Nguyen|Race=Black) = 0.000018
- P(Name=Nguyen|Race=API) = 0.052077
- P(Name=Nguyen|Race=AIAN) = 0.000087
- P(Name=Nguyen|Race=Hispanic) = 0.000073

Looking at API (Asian/Pacific Islander), we see that P(Name=Nguyen|Race=API) is 0.052077. This means that among all asian/Pacific Islander individuals in the dataset, approximately 5.2% have the last name Nguyen. This must not be confused with P(Race=API|Name=Nguyen), which would be the probability that a person with the last name Nguyen is Asian/Pacific Islander. 

As such, a probability of 0.05 is actually quite high/significant. In order to provide more intuitive understanding of the probabilities, we can calculate probabilities using an understanding of entropy and seperation.

Beginning with entropy, we can calculate the entropy of the distribution of probabilities for a given name. The formula for entropy is:
Entropy = -Σ P(Name|Race) * log(P(Name|Race))

This will help us identify names which are strongly associated with a particular race.

High entropy → name is ambiguous across races
Low entropy → name is strongly tied to one race

Looking at separation, we can calculate the separation between the most probable race and the second most probable race. 

Separation= p_top / p_second

This tells us how dominant the top signal is. 

High separation → strong identity signal
Low separation → weak/ambiguous identity signal

This helps us answer the question: Is one race clearly dominant or not?


With this in mind, we can analyze the dataset to identify names that are strongly associated with a particular race and those that are more ambiguous. This analysis can be useful in understanding potential biases in hiring practices and how names may influence perceptions of candidates.


```python
import numpy as np

# Calculate entropy for each name
def calculate_entropy(row):
    probabilities = np.array(row[["white","black","hispanic","api", "aian"]], dtype=float)
    probabilities = probabilities[probabilities > 0]  # Filter out zero probabilities
    if len(probabilities) == 0:
        return 0.0
    probabilities = probabilities / np.sum(probabilities)  # Normalize to sum to 1
    entropy = -np.sum(probabilities * np.log(probabilities))
    return entropy

first_df["entropy"] = first_df.apply(calculate_entropy, axis=1)
last_df["entropy"] = last_df.apply(calculate_entropy, axis=1)
```


```python
# Calculate the seperation between the highest and second highest probabilities
def calculate_separation(row):
    probabilities = np.array(row[["white","black","hispanic","api", "aian"]], dtype=float)
    sorted_probs = np.sort(probabilities)[::-1]  # Sort in descending order
    if len(sorted_probs) < 2:
        return 0.0
    separation = sorted_probs[0] / sorted_probs[1]
    return separation

first_df["separation"] = first_df.apply(calculate_separation, axis=1)
last_df["separation"] = last_df.apply(calculate_separation, axis=1)
```


```python
first_df.sort_values("entropy", inplace=True, ascending=True)
last_df.sort_values("entropy", inplace=True, ascending=True)
print("First Names with Lowest Entropy:")
print(first_df[["name", "entropy", "separation"]].head())
print("\nLast Names with Lowest Entropy:")
print(last_df[["name", "entropy", "separation" ]].head())
```

    First Names with Lowest Entropy:
              name   entropy  separation
    153      JORGE  0.739433    6.851358
    262     HECTOR  0.785557    6.345265
    210  ALEJANDRO  0.791053    4.343773
    156  FRANCISCO  0.833607    3.958246
    273     RAFAEL  0.836482    4.630681
    
    Last Names with Lowest Entropy:
          name   entropy  separation
    39    YANG  0.027347  906.441432
    0   NGUYEN  0.031624  597.515499
    33      LI  0.032047  718.107205
    19    CHEN  0.032632  863.594562
    37    WANG  0.035693  529.248655
    

We find that there is very little separation and higher entropy in first names, but there are some last names with very high separation and low entropy. This suggests that while first names may not be strongly associated with a particular race, some last names can be strong indicators. As such, we will be moving forward with the last name dataset for our analysis of bias in hiring practices. 

For assignment of first names, we will be using low separation and high entropy names, which are more ambiguous and less likely to be strongly associated with a particular race.


```python
# Find 5 last names with lowest entropy and highest separation for each ethnicity
if "max_race" not in last_df.columns:
    last_df["max_race"] = last_df[["white","black","hispanic","api", "aian"]].idxmax(axis=1)

if "confidence" not in last_df.columns:
    last_df["confidence"] = last_df[["white","black","hispanic","api", "aian"]].max(axis=1)

if "entropy" not in last_df.columns:
    last_df["entropy"] = last_df.apply(calculate_entropy, axis=1)

if "separation" not in last_df.columns:
    last_df["separation"] = last_df.apply(calculate_separation, axis=1)

races = ["white", "black", "hispanic", "api", "aian"]
last_names_by_race = {}
for race in races:
    subset = last_df[last_df["max_race"] == race]
    # Sort by entropy ascending (lowest first), then separation descending (highest first)
    top5 = subset.sort_values(["entropy", "separation"], ascending=[True, False]).head(5)
    last_names_by_race[race] = top5
    print(f"\nTop 5 {race} last names (lowest entropy, highest separation):")
    print(top5[["name", "entropy", "separation", "confidence"]])

# Combine all selected last names into one dataframe
selected_last_df = pd.concat(last_names_by_race.values(), ignore_index=True)
```

    
    Top 5 white last names (lowest entropy, highest separation):
              name   entropy  separation  confidence
    306  SCHNEIDER  0.911703    4.558033    0.000828
    298    SCHMIDT  0.951419    3.605038    0.001199
    297      MEYER  0.961095    4.209647    0.001227
    305      WALSH  0.964940    5.285608    0.000851
    304    SCHULTZ  0.997397    2.979635    0.000852
    
    Top 5 black last names (lowest entropy, highest separation):
               name   entropy  separation  confidence
    86   WASHINGTON  0.586018    6.671947    0.005353
    229       BANKS  0.903929    5.583226    0.001989
    18      JACKSON  1.040020    2.593061    0.012949
    107     COLEMAN  1.044179    3.629235    0.003369
    38     ROBINSON  1.058140    3.710894    0.008208
    
    Top 5 hispanic last names (lowest entropy, highest separation):
              name   entropy  separation  confidence
    168    VAZQUEZ  0.218712   63.322186    0.003497
    222     JUAREZ  0.331536   23.742633    0.002575
    15    GONZALEZ  0.333707   26.929210    0.021088
    212      ROJAS  0.379687   26.597526    0.002704
    192  MALDONADO  0.396517   19.563569    0.003007
    
    Top 5 api last names (lowest entropy, highest separation):
          name   entropy  separation  confidence
    39    YANG  0.027347  906.441432    0.012664
    0   NGUYEN  0.031624  597.515499    0.052077
    33      LI  0.032047  718.107205    0.013347
    19    CHEN  0.032632  863.594562    0.020110
    37    WANG  0.035693  529.248655    0.012911
    
    Top 5 aian last names (lowest entropy, highest separation):
           name   entropy  separation  confidence
    87     HUNT  0.960478    4.462461    0.004458
    136  JACOBS  1.008154    3.918379    0.002959
    58    JAMES  1.193945    1.281131    0.004281
    209  HARVEY  1.238540    1.319971    0.001316
    272  BREWER  1.241424    1.288998    0.000928
    


```python
# Find 10 male and 10 female first names with highest entropy and lowest separation
if "entropy" not in first_df.columns:
    first_df["entropy"] = first_df.apply(calculate_entropy, axis=1)

if "separation" not in first_df.columns:
    first_df["separation"] = first_df.apply(calculate_separation, axis=1)

# Male names
male_subset = first_df[first_df["gender"] == "male"]
top10_male = male_subset.sort_values(["entropy", "separation"], ascending=[False, True]).head(10)
selected_male_df = top10_male
print("\nTop 10 male first names (highest entropy, lowest separation):")
print(top10_male[["name", "entropy", "separation", "gender_confidence"]])

# Female names
female_subset = first_df[first_df["gender"] == "female"]
top10_female = female_subset.sort_values(["entropy", "separation"], ascending=[False, True]).head(10)
selected_female_df = top10_female
print("\nTop 10 female first names (highest entropy, lowest separation):")
print(top10_female[["name", "entropy", "separation", "gender_confidence"]])

# Combine selected first names
selected_first_df = pd.concat([selected_male_df, selected_female_df], ignore_index=True)
```

    
    Top 10 male first names (highest entropy, lowest separation):
             name   entropy  separation  gender_confidence
    58     EDWARD  1.606156    1.069134           0.869287
    32   BENJAMIN  1.604486    1.030511           0.883557
    118   RAYMOND  1.604037    1.080275           0.858842
    23       ERIC  1.600918    1.035747           0.842707
    59     GEORGE  1.600230    1.024395           0.855428
    7      JOSEPH  1.599505    1.104059           0.864834
    1       DAVID  1.599350    1.062802           0.857211
    19    RICHARD  1.599264    1.232689           0.847267
    31   JONATHAN  1.596479    1.057125           0.853736
    72      AARON  1.596311    1.022855           0.820821
    
    Top 10 female first names (highest entropy, lowest separation):
             name   entropy  separation  gender_confidence
    301      GINA  1.605512    1.045539           0.929374
    71    CYNTHIA  1.601838    1.157484           0.901646
    24   MICHELLE  1.601007    1.153465           0.906370
    225  VIRGINIA  1.599836    1.265671           0.935363
    199      RUTH  1.599310    1.054146           0.928772
    105     LINDA  1.598050    1.103459           0.911867
    83   SAMANTHA  1.597416    1.198297           0.936157
    285   FRANCES  1.597271    1.179887           0.835381
    208   THERESA  1.596343    1.257881           0.920022
    56       LISA  1.594945    1.036229           0.917748
    

We will now match all first names with all last names in all possible combinations. Each name combination will just cary its last name entropy and separation, as the first name is more ambiguous and less likely to be strongly associated with a particular race. Gender from first name will be attached as well. 


```python
# create our final dataframe with all combinations of first and last names, and their associated probabilities, entropy, and separation
final_df = pd.DataFrame(columns=["first_name", "last_name", "race", "separation", "entropy", "gender", "gender_confidence"])

import itertools

data = []
for first, last in itertools.product(selected_first_df.itertuples(), selected_last_df.itertuples()):
    data.append({
        "first_name": first.name,
        "last_name": last.name,
        "race": last.max_race,
        "separation": last.separation,
        "entropy": last.entropy,
        "gender": first.gender,
        "gender_confidence": first.gender_confidence
    })

final_df = pd.DataFrame(data)
print(f"Final dataframe shape: {final_df.shape}")
print(final_df.head(30))

# save final dataframe to csv
final_df.to_csv("data/final_name_combinations.csv", index=False)

```

    Final dataframe shape: (500, 7)
       first_name   last_name      race  separation   entropy gender  \
    0      EDWARD   SCHNEIDER     white    4.558033  0.911703   male   
    1      EDWARD     SCHMIDT     white    3.605038  0.951419   male   
    2      EDWARD       MEYER     white    4.209647  0.961095   male   
    3      EDWARD       WALSH     white    5.285608  0.964940   male   
    4      EDWARD     SCHULTZ     white    2.979635  0.997397   male   
    5      EDWARD  WASHINGTON     black    6.671947  0.586018   male   
    6      EDWARD       BANKS     black    5.583226  0.903929   male   
    7      EDWARD     JACKSON     black    2.593061  1.040020   male   
    8      EDWARD     COLEMAN     black    3.629235  1.044179   male   
    9      EDWARD    ROBINSON     black    3.710894  1.058140   male   
    10     EDWARD     VAZQUEZ  hispanic   63.322186  0.218712   male   
    11     EDWARD      JUAREZ  hispanic   23.742633  0.331536   male   
    12     EDWARD    GONZALEZ  hispanic   26.929210  0.333707   male   
    13     EDWARD       ROJAS  hispanic   26.597526  0.379687   male   
    14     EDWARD   MALDONADO  hispanic   19.563569  0.396517   male   
    15     EDWARD        YANG       api  906.441432  0.027347   male   
    16     EDWARD      NGUYEN       api  597.515499  0.031624   male   
    17     EDWARD          LI       api  718.107205  0.032047   male   
    18     EDWARD        CHEN       api  863.594562  0.032632   male   
    19     EDWARD        WANG       api  529.248655  0.035693   male   
    20     EDWARD        HUNT      aian    4.462461  0.960478   male   
    21     EDWARD      JACOBS      aian    3.918379  1.008154   male   
    22     EDWARD       JAMES      aian    1.281131  1.193945   male   
    23     EDWARD      HARVEY      aian    1.319971  1.238540   male   
    24     EDWARD      BREWER      aian    1.288998  1.241424   male   
    25   BENJAMIN   SCHNEIDER     white    4.558033  0.911703   male   
    26   BENJAMIN     SCHMIDT     white    3.605038  0.951419   male   
    27   BENJAMIN       MEYER     white    4.209647  0.961095   male   
    28   BENJAMIN       WALSH     white    5.285608  0.964940   male   
    29   BENJAMIN     SCHULTZ     white    2.979635  0.997397   male   
    
        gender_confidence  
    0            0.869287  
    1            0.869287  
    2            0.869287  
    3            0.869287  
    4            0.869287  
    5            0.869287  
    6            0.869287  
    7            0.869287  
    8            0.869287  
    9            0.869287  
    10           0.869287  
    11           0.869287  
    12           0.869287  
    13           0.869287  
    14           0.869287  
    15           0.869287  
    16           0.869287  
    17           0.869287  
    18           0.869287  
    19           0.869287  
    20           0.869287  
    21           0.869287  
    22           0.869287  
    23           0.869287  
    24           0.869287  
    25           0.883557  
    26           0.883557  
    27           0.883557  
    28           0.883557  
    29           0.883557  
    
