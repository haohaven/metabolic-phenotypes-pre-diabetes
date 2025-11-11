**Hidden Flavors of Metabolic Risk: Clustering Patterns in Glucose, Lipids, and Adiposity**

This project explores whether hidden subtypes of metabolic risk exist within the general population; beyond traditional diagnostic labels like "pre-diabetes." Using large scale public health data (NHANES 2021–2023), I will apply unsupervised learning to identify groups of individuals with distinct metabolic signatures, each potentially suggesting different intervention priorities (such as focusing on lipid management versus weight loss strategies).

**Project Motivation**

Current clinical thresholds treat metabolic health as a binary state: normal or abnormal. But physiology rarely works that simply. We aim to uncover whether combinations of common clinical measures; fasting glucose, triglycerides, and waist circumference, reveal latent metabolic phenotypes.

Unlike supervised methods that require predefined disease labels, clustering lets the _data_ reveal natural groupings that may not align with current diagnostic categories. If successful, this approach could help move beyond one-size-fits-all pre-diabetes management toward more personalized prevention strategies.

**Hypotheses & Expected Outcomes**

We hypothesize that 3–5 distinct clusters will emerge, potentially including:

*   **Lipid-driven risk**: High triglycerides with normal glucose
*   **Glucose-centric**: Elevated fasting glucose with moderate lipids
*   **Adiposity-dominant**: High waist circumference with variable metabolic markers
*   **Low-risk baseline**: Normal across all three measures

**Success criteria**: Clusters are clinically interpretable, stable across validation methods, and reveal patterns not captured by conventional metabolic syndrome definitions.

**Methods Overview**

**Data Source**: NHANES 2021–2023  
Files: GLU\_L.xpt, TRIGLY\_L.xpt, BMX\_L.xpt, DEMO\_L.xpt

**Core Variables**:

*   Fasting Glucose (LBXGLU) — glycemic control
*   Triglycerides (LBDTRIG) — lipid metabolism
*   Waist Circumference (BMXWAIST) — central adiposity

**Analytical Approach**: Using modern clustering methods (KMeans, Agglomerative Clustering, DBSCAN) on these three readily available clinical measures, combined with demographic covariates, to reveal underlying metabolic subtypes.

**Population**: Adults aged 18+ from NHANES 2021–2023 with complete fasting laboratory data.

**Repository Structure**

data/

  raw/          # Original NHANES XPT files

  processed/    # Cleaned, merged datasets

docs/           # Project charter, methods, and meeting notes

notebooks/      # Exploration, method development, results generation

src/

  data/         # load.py, preprocess.py, clean.py

  analysis/     # clustering.py, validation.py

  visualization/# plotting scripts

results/        # figures, tables, and supplementary outputs

**Quick Start**

**Requirements**: Python 3.9+

1.  Clone the repository:

bash

git clone https://github.com/<your-username\>/metabolic-flavors.git

cd metabolic-flavors

2.  Install dependencies:

bash

pip install -r requirements.txt

3.  Build the analysis dataset:

bash

python src/data/preprocess.py  _\# merges and cleans raw NHANES files_

4.  Run clustering analysis:

bash

python src/analysis/clustering.py

**Planned Deliverables**

*   Clean, merged NHANES dataset (processed/)
*   Exploratory notebooks (correlation analysis, PCA)
*   Cluster visualizations (PCA plots, dendrograms, silhouette analysis)
*   Summary report interpreting each cluster's clinical significance
*   Comparison with ATP III metabolic syndrome criteria

**Validation Strategy**

**Cluster robustness** will be assessed through:

*   Multiple algorithms (KMeans, Agglomerative, DBSCAN)
*   Silhouette scores and Davies-Bouldin index
*   Stability testing via bootstrapping
*   Clinical interpretability against established metabolic syndrome definitions

**Known Limitations**

*   Cross-sectional data (cannot establish causality)
*   Fasting sample requirement reduces available population
*   Cluster assignments are descriptive patterns, not diagnostic categories
*   Results reflect 2021–2023 U.S. population and may not generalize globally

**Citation**

Data derived from the National Health and Nutrition Examination Survey (NHANES), U.S. Centers for Disease Control and Prevention (CDC).

**Contact**

cherroukhajar@gmail.com
