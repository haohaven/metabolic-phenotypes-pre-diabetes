# **1\. Data Acquisition & Preprocessing**

For this project, I used the **NHANES 2021–2023 datasets**, which provide detailed population-level health data. After downloading the raw files (3048 participants), I focused on three main types of variables:

**Biochemical Data:**

·       Fasting glucose (mg/dL & mmol/L)

·       Triglycerides (mg/dL & mmol/L)

·       Sample weights for fasting subsamples

**Anthropometric Data:**

·       Waist circumference (cm)

·       Body Mass Index (BMI, kg/m²)

·       Height and weight

**Demographics:**

·       Age, sex, and race/ethnicity

·       Education level

# **Preprocessing Steps (Code Narrative):**

⋆   **Data Loading (**`**[Github: load.py](mailto:https://github.com/haohaven/metabolic-phenotypes-pre-diabetes/blob/main/src/data/load.py)**`**)** : Loads NHANES files, checks for key variables, prints summary statistics.

o   prints all 4 datasets with row/column counts.

o   All key variables (`LBXGLU`, `LBDTRIG`, `BMXWAIST`, `SEQN`) are present

o   can import and use the function in notebooks

⋆    **Explore missing data patterns (Github:** [missing\_data\_analysis.ipynb](mailto:https://github.com/haohaven/metabolic-phenotypes-pre-diabetes/blob/main/notebooks/explore_data/missing_data_analysis.ipynb)**)****:** Create a comprehensive notebook that visualizes missing data across all datasets to inform preprocessing decisions.

o   Created a missing data summary function

o  Analyzed each dataset (**Github**: [key\_variable\_missingness)](mailto:https://github.com/haohaven/metabolic-phenotypes-pre-diabetes/blob/main/results/figures/key_variables_missingness.png)
<img width="763" height="393" alt="image" src="https://github.com/user-attachments/assets/16ebf45a-6b07-4cc9-b848-dc886a21cd0d" />

o	Overlap Analysis: Analyze how many participants have complete data across all key variables.

o	Visualize Complete Cases Flow (Github: Sample_selection_flowshart)

o	Missing data heatmap: (Github: missing_data_heatmap)
<img width="828" height="536" alt="image" src="https://github.com/user-attachments/assets/62dd7e0a-22d6-44e3-8aec-309a2519baeb" />

o	Create comprehensive summary table: (Github: missing_data_summary)

⋆   **Create Data Merging and Preprocessing Module** **(Github:** `[preprocess.py](mailto:https://github.com/haohaven/metabolic-phenotypes-pre-diabetes/blob/main/src/data/preprocess.py)`**)**: Build a preprocessing module that merges all 4 datasets, filters to eligible participants, and creates an analysis-ready dataset.

**o**   CSV file created in **(Github:** **[data/processed](mailto:https://github.com/haohaven/metabolic-phenotypes-pre-diabetes/blob/main/data/processed/nhanes_metabolic_analysis_ready.csv)****)**

**o**   Preprocessing report created in **(Github:** **[preprocessing\_table](mailto:https://github.com/haohaven/metabolic-phenotypes-pre-diabetes/blob/main/results/tables/preprocessing_report.txt)****)**

⋆   **Exploratory Data Analysis** (**Github:** [variable\_distributions](mailto:https://github.com/haohaven/metabolic-phenotypes-pre-diabetes/blob/main/notebooks/explore_data/variable_distributions.ipynb)): Create a comprehensive notebook visualizing distributions of all core variables, derived categories, and demographic characteristics to understand the data before clustering.

o   Descriptive Statistics: (**Github:** [descriptive\_statistics](mailto:https://github.com/haohaven/metabolic-phenotypes-pre-diabetes/blob/main/results/tables/descriptive_statistics.csv))

o   Individual histograms for core clustering variables (**Github:** [core\_variable\_distribution](mailto:https://github.com/haohaven/metabolic-phenotypes-pre-diabetes/blob/main/results/figures/core_variables_distributions.png))

o   Box plots to identify outliers (**Github:** [core\_variables\_boxplots](mailto:https://github.com/haohaven/metabolic-phenotypes-pre-diabetes/blob/main/results/figures/core_variables_boxplots.png))

o   Q-Q plots to assess normality (**Github:** [normality\_qqplots](mailto:https://github.com/haohaven/metabolic-phenotypes-pre-diabetes/blob/main/results/figures/normality_qqplots.png))

o   Clinical Categories Distribution (**Github:** [clinical\_categories\_distribution](mailto:https://github.com/haohaven/metabolic-phenotypes-pre-diabetes/blob/main/results/figures/clinical_categories_distribution.png))
<img width="736" height="550" alt="image" src="https://github.com/user-attachments/assets/c3029fdd-9886-4119-a99b-f6f05de88cf7" />

o	Demographics Distribution (Github:  demographic_distribution)
<img width="838" height="629" alt="image" src="https://github.com/user-attachments/assets/4d24fc6d-806c-4e1e-a2dc-299896e403c2" />

o	Core Variables by d emographics (Github: core_variables_by_sex)
<img width="975" height="321" alt="image" src="https://github.com/user-attachments/assets/916dda54-cc79-4394-a796-007fa6b45ec9" />

⋆   **Correlation analysis** (**Github:** [correlation\_analysis](mailto:https://github.com/haohaven/metabolic-phenotypes-pre-diabetes/blob/main/notebooks/explore_data/correlation_analysis.ipynb)) : Analyze relationships between core variables, identify multicollinearity, and understand which variables contribute independent information for clustering.

o   Correlation Matrix (**Github:** [correlation\_matrix](mailto:https://github.com/haohaven/metabolic-phenotypes-pre-diabetes/blob/main/results/tables/correlation_matrix.csv))

o   Correlation Heatmap (**Github:**  [correlation\_heatmap](mailto:https://github.com/haohaven/metabolic-phenotypes-pre-diabetes/blob/main/results/figures/correlation_heatmap.png))

o   Scatterplot Matrix (**Github:**   [scatterplot\_matrix\_core\_variables](mailto:https://github.com/haohaven/metabolic-phenotypes-pre-diabetes/blob/main/results/figures/scatterplot_matrix_core_variables.png))
<img width="870" height="890" alt="image" src="https://github.com/user-attachments/assets/d69cb6c6-2b10-4977-857b-18f4ddfb8083" />

o	Correlation by Age Groups (Github:   correlation_by_age_group)
o	Partial correlations: (Github:   partial_correlations)
⋆  **Outlier Detection and Handling Strategy** (**Github:**   outlier\_detection)

o   All outlier detection methods implemented

o   Mahalanobis distance calculated

o   Comprehensive visualization showing outliers from different methods (**Github:**   [outlier\_detction\_methods](mailto:https://github.com/haohaven/metabolic-phenotypes-pre-diabetes/blob/main/results/figures/outlier_detection_methods.png))
<img width="975" height="336" alt="image" src="https://github.com/user-attachments/assets/ff9aadba-994c-43b3-a990-db9efd1c934f" />

o	Mahalanobis distance (detects multivariate outliers) (Github:   Mahalanobis_distance_outliers)
<img width="975" height="363" alt="image" src="https://github.com/user-attachments/assets/a98e5d2d-d587-47ae-a7cb-1706c81707b1" />

o	Side by side comparison of distributions (Github:    outlier_removal_impact)

⋆  **Feature Scaling and Standardization:** Prepare the three core clustering variables for analysis by applying appropriate scaling methods. Compare different scaling approaches and select the optimal one for clustering. (**Github:**    [feature\_scaling](mailto:https://github.com/haohaven/metabolic-phenotypes-pre-diabetes/blob/main/notebooks/explore_data/feature_scaling.ipynb))
o	Compare Variable Scales to show that scalling is necessary

o	Apply Different Scaling Methods

o	Apply Different Scaling Methods 

o	Visualize all scaling methods side by side
<img width="975" height="871" alt="image" src="https://github.com/user-attachments/assets/93a4ebae-be5a-4404-a4d0-2b369790d348" />

o	Compare statistical properties before and after scalling

o	Compare correlations before and after scalling

o	Compare Euclidian distances before and after scalling
<img width="839" height="242" alt="image" src="https://github.com/user-attachments/assets/2ee44521-62a3-4966-ab51-8429bdb8b2bc" />

o	Scalling method recommendation (RobustScaler)

