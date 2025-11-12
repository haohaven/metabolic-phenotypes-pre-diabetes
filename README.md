# Uncovering Hidden Metabolic Phenotypes in Adults Using Clustering of Glucose, Lipids, and Adiposity

This project explores whether hidden subtypes of metabolic risk exist within the general population; beyond traditional diagnostic labels like "prediabetes." Using large scale public health data (NHANES 2021–2023), I apply unsupervised learning to identify groups of individuals with distinct metabolic signatures, each potentially suggesting different intervention priorities (such as focusing on lipid management versus weight loss strategies).

## Project Motivation

Current clinical thresholds treat metabolic health as a binary state: normal or abnormal. But physiology rarely works that simply. I aim to uncover whether combinations of common clinical measures; fasting glucose, triglycerides, and waist circumference; reveal latent metabolic phenotypes.

Unlike supervised methods that require predefined disease labels, clustering lets the _data_ reveal natural groupings that may not align with current diagnostic categories. If successful, this approach could help move beyond one-size-fits-all prediabetes management toward more personalized prevention strategies.

## Hypotheses & Expected Outcomes

I hypothesize that 3 to 5 distinct clusters will emerge, potentially including:

*   **Lipid-driven risk**: High triglycerides with normal glucose
*   **Glucose-centric**: Elevated fasting glucose with moderate lipids
*   **Adiposity-dominant**: High waist circumference with variable metabolic markers
*   **Low-risk baseline**: Normal across all three measures

**Success criteria**: Clusters are clinically interpretable, stable across validation methods, and reveal patterns not captured by conventional metabolic syndrome definitions.

## Methods Overview

**Data Source**: NHANES 2021–2023  
Files: `GLU_L.xpt`, `TRIGLY_L.xpt`, `BMX_L.xpt`, `DEMO_L.xpt`

**Core Variables**:

*   Fasting Glucose (LBXGLU) — glycemic control
*   Triglycerides (LBDTRIG) — lipid metabolism
*   Waist Circumference (BMXWAIST) — central adiposity

**Analytical Approach**: Using modern clustering methods (KMeans, Agglomerative Clustering, DBSCAN) on these three readily available clinical measures, combined with demographic covariates, to reveal underlying metabolic subtypes.
## Repository Structure

    data/
      raw/          # Original NHANES XPT files
      processed/    # Cleaned, merged datasets
    docs/           # Project charter, methods, and meeting notes
    notebooks/      # Exploration, method development, results generation
    src/
      data/         # load.py, preprocess.py, clean.py
      analysis/     # clustering.py, validation.py
      visualization/# plotting scripts
    results/        # figures, tables, and supplementary outputs

## Quick Start

**Requirements**: Python 3.9+

1.  Clone the repository:

bash

    git clone https://github.com/haohaven/metabolic-phenotypes-pre-diabetes.git
    cd metabolic-phenotypes-pre-diabetes

2.  Install dependencies:

bash

    pip install -r requirements.txt

3.  Test data loading:

bash

    python src/data/load.py

4.  Build the analysis dataset (coming soon):

bash

    python src/data/preprocess.py  # merges and cleans raw NHANES files

5.  Run clustering analysis (coming soon):

bash

    python src/analysis/clustering.py

## Implementation Progress

###  Phase 1: Data Infrastructure

*   [x]  Repository setup and folder structure
*   [x] Data loading module (`src/data/load.py`)
    *   Loads all 4 NHANES 2021-2023 XPT files
    *   Validates presence of key variables
    *   Provides data summary and integrity checks
    *   Test: `python src/data/load.py`
*   [x]  Missing data exploration notebook (`notebooks/explore_data/missing_data_analysis.ipynb`)
 - Comprehensive missingness analysis across all datasets
  - Key findings:
    - Total participants: 11,933
    - Fasting subsample: 3,996 (all in glucose/triglycerides files)
    - Complete core variables: ~3,996 adults (33.5% of total)
  - Core variable completeness: LBXGLU, LBXTLG, BMXWAIST
  - Note: All participants in lab files are pre-screened fasting subsample
  - Outputs: 3 figures + summary table in `results/`
*   [x]  Data preprocessing module (`src/data/preprocess.py`)
  - Merges all 4 NHANES datasets on SEQN
  - Filters to adults ≥18 with complete core variables
  - Creates 6 derived variables (age groups, clinical categories)
  - Final sample: ~3,996 participants
  - Run: `python src/data/preprocess.py`
  - Output: `data/processed/nhanes_metabolic_analysis_ready.csv`
*   [ ]  Fasting sample filtering
*   [ ]  Missingness handling strategy
*   [ ]  Create analysis-ready dataset
*   [ ]  Data quality report
*   [ ]  Demographic distribution analysis
*   [ ]  Variable distribution plots

###  Phase 2: Exploratory Analysis 

*   [ ]  Correlation analysis
*   [ ]  PCA and dimensionality assessment
*   [ ]  Outlier detection
*   [ ]  Clinical threshold comparisons

###  Phase 3: Clustering Implementation
*   [ ]  Feature scaling and preprocessing
*   [ ]  Optimal cluster number determination
*   [ ]  KMeans clustering
*   [ ]  Agglomerative clustering
*   [ ]  DBSCAN clustering

###  Phase 4: Validation & Interpretation

*   [ ]  Silhouette analysis
*   [ ]  Cluster stability testing
*   [ ]  Clinical interpretation
*   [ ]  ATP III comparison

###  Phase 5: Visualization & Reporting 

*   [ ]  Cluster visualizations
*   [ ]  Summary statistics tables
*   [ ]  Final report generation
*   [ ]  Documentation completion

## Planned Deliverables

*   Clean, merged NHANES dataset (`processed/`)
*   Exploratory notebooks (correlation analysis, PCA)
*   Cluster visualizations (PCA plots, dendrograms, silhouette analysis)
*   Summary report interpreting each cluster's clinical significance
*   Comparison with ATP III metabolic syndrome criteria

## Validation Strategy

**Cluster robustness** will be assessed through:

*   Multiple algorithms (KMeans, Agglomerative, DBSCAN)
*   Silhouette scores and Davies-Bouldin index
*   Stability testing via bootstrapping
*   Clinical interpretability against established metabolic syndrome definitions

## Known Limitations

*   Cross-sectional data (cannot establish causality)
*   Fasting sample requirement reduces available population
*   Cluster assignments are descriptive patterns, not diagnostic categories
*   Results reflect 2021–2023 U.S. population and may not generalize globally

## Citation

Data derived from the National Health and Nutrition Examination Survey (NHANES), U.S. Centers for Disease Control and Prevention (CDC).

## License

Academic research project. Data usage complies with NHANES public use data policies.

## Contact

**Author**: Hajar Cherrouk  
**Email**: [cherroukhajar@gmail.com](mailto:cherroukhajar@gmail.com)  
**GitHub**: [@haohaven](https://github.com/haohaven)

* * *

**Last Updated**: 12 November 2025
