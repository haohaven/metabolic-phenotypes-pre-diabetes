# Methodological Decisions

## Feature Scaling Method Selection
**Choice:** RobustScaler selected as primary scaling method

**Alternatives Considered:**
- StandardScaler
- PowerTransformer

**Reasoning:**
- RobustScaler handles outliers using median and interquartile range
- Preserves the natural spacing of points
- Performs comparably to StandardScaler for near-normal data
- Especially suitable for skewed metabolic variables like triglycerides
- Power transformation corrected skewness effectively, but our goal wasn't normality - it was robust comparability across variables while maintaining interpretability

**Implementation Plan:**
- Primary analysis: RobustScaler
- Sensitivity test: StandardScaler

## PCA Usage Strategy
**Choice:** Use PCA for exploration only, keep all 3 original variables for clustering

**Reasoning:**
- Only 3 variables (already low dimensional)
- Correlations are low: r_max = 0.315
- All variables have clear clinical meaning
- Low VIF for core variables (acceptable multicollinearity)

**PCA Purpose:**
1. Understand data structure
2. Visualize in 2D space
3. Assess how variance is distributed
4. Confirm that all 3 variables contribute unique information

**Note:** PCA is NOT used for dimensionality reduction here - all 3 variables are kept for clustering.

## Loading Plot Interpretation Methodology
**Approach:** Standardized interpretation of PCA loading plots

**Interpretation Rules:**
- **Arrow length:** Strength of contribution to PC1-PC2 space
- **Arrow direction:** Correlation between variables
  - Same direction = positively correlated
  - Opposite direction = negatively correlated  
  - 90° angle = uncorrelated
- **Arrows close to unit circle:** Well-represented in PC1-PC2 space
- **Short arrows:** Poorly represented (variance primarily in PC3)

**Reasoning:**
- Provides consistent framework for analyzing variable relationships
- Helps identify which variables drive each principal component
- Allows assessment of how well 2D visualization represents 3D data structure
