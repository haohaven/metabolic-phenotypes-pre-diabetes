#data preproccessing
"""
This module merges the four core NHANES datasets (glucose, triglycerides, 
body measures, demographics) and applies filtering criteria to create the 
final analysis ready dataset for clustering.

Author: Hajar Cherrouk
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Tuple
import warnings

from src.data.load import load_nhanes_data


def merge_nhanes_datasets(data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """ merge  all NHANES datasets on participant id (SEQN) by preforming a series of left joins starting 
    to preserve all demographic records, then progressively merges lab and examination data.
    """
    print("merging nhanes datasets")
    
    # start with demographics
    merged = data['demographics'].copy()
    print(f"Starting with demographics: {len(merged):>6,} participants")
    
    # merge glucose data
    merged = merged.merge(
        data['glucose'][['SEQN', 'LBXGLU', 'LBDGLUSI', 'WTSAF2YR']],
        on='SEQN',
        how='left',
        suffixes=('', '_glucose')
    )
    n_with_glucose = merged['LBXGLU'].notna().sum()
    print(f"After glucose merge:        {n_with_glucose:>6,} with glucose data")
    
    # merge triglycerides data
    merged = merged.merge(
        data['triglycerides'][['SEQN', 'LBXTLG', 'LBDTRSI']],
        on='SEQN',
        how='left',
        suffixes=('', '_triglycerides')
    )
    n_with_trig = merged['LBXTLG'].notna().sum()
    print(f"After triglycerides merge:  {n_with_trig:>6,} with triglyceride data")
    
    # merge body measures
    merged = merged.merge(
        data['body_measures'][['SEQN', 'BMXWAIST', 'BMXBMI', 'BMXWT', 'BMXHT']],
        on='SEQN',
        how='left',
        suffixes=('', '_body')
    )
    n_with_waist = merged['BMXWAIST'].notna().sum()
    print(f"After body measures merge:  {n_with_waist:>6,} with body measure data")
    
    print(f"\nFinal merged dataset:       {len(merged):>6,} participants")
    print(f"                            {len(merged.columns):>6,} variables")
    print("="*80)
    
    return merged


def filter_to_eligible_sample(df: pd.DataFrame, min_age: int = 18, require_core_vars: bool = True) -> Tuple[pd.DataFrame, Dict]:
    
    """
    merged dataset to eligible participants for clustering analysis
    All participants in the glucose/triglycerides files are from the
    morning fasting subsample, so no additional fasting filter is needed.
    """
    
    print("\n Filtering to eligible sample")
    
    n_start = len(df)
    exclusion_stats = {'n_start': n_start}
    
    # create a copy to avoid modifying original 
    filtered = df.copy()
    
    # filter 1: age >= min_age
    age_filter = filtered['RIDAGEYR'] >= min_age
    n_under_age = (~age_filter).sum()
    filtered = filtered[age_filter]
    exclusion_stats['n_under_age'] = n_under_age
    
    print(f"\nStarting sample:           {n_start:>6,} participants")
    print(f"Age < {min_age} years excluded:     {n_under_age:>6,} participants")
    print(f"Remaining after age filter: {len(filtered):>6,} participants")
    
    #filter 2: complete core variables
    if require_core_vars:
        core_vars = ['LBXGLU', 'LBXTLG', 'BMXWAIST']
        
        # check completeness for each variable
        print(f"\nCore variable completeness:")
        for var in core_vars:
            n_missing = filtered[var].isna().sum()
            pct_missing = (n_missing / len(filtered)) * 100
            print(f"  {var:12s}: {n_missing:>6,} missing ({pct_missing:>5.1f}%)")
        
        # filter to complete cases
        complete_core = filtered[core_vars].notna().all(axis=1)
        n_incomplete = (~complete_core).sum()
        filtered = filtered[complete_core]
        exclusion_stats['n_incomplete_core'] = n_incomplete
        
        print(f"\nMissing core variables:     {n_incomplete:>6,} participants excluded")
        print(f"Final eligible sample:      {len(filtered):>6,} participants")
    
    # calculate final retention rate
    retention_rate = (len(filtered) / n_start) * 100
    exclusion_stats['n_final'] = len(filtered)
    exclusion_stats['retention_rate'] = retention_rate
    
    print(f"\n{'*'*80}")
    print(f"RETENTION RATE: {retention_rate:.1f}% ({len(filtered):,} / {n_start:,})")
    print(f"{'*'*80}")
    
    return filtered, exclusion_stats


def create_derived_variables(df: pd.DataFrame) -> pd.DataFrame:
    #create derived variables useful for clustering and analysis
    
    
    print("\n creating derived variables" )
    df = df.copy()
    
    # age groups
    df['age_group'] = pd.cut(
        df['RIDAGEYR'],
        bins=[18, 30, 45, 60, 120],
        labels=['18-29', '30-44', '45-59', '60+'],
        right=False
    )
    print(" Created age_group (18-29, 30-44, 45-59, 60+)")
    
    # sex labels
    df['sex_label'] = df['RIAGENDR'].map({1: 'Male', 2: 'Female'})
    print(" Created sex_label (Male/Female)")
    
    # BMI categories (made by WHO classification)
    df['bmi_category'] = pd.cut(
        df['BMXBMI'],
        bins=[0, 18.5, 25, 30, 100],
        labels=['Underweight', 'Normal', 'Overweight', 'Obese'],
        right=False
    )
    print(" Created bmi_category (WHO classification)")
    
    # Glucose categories (ADA criteria)
    # Normal: <100 mg/dL
    # Prediabetes: 100-125 mg/dL
    # Diabetes: ≥126 mg/dL
    df['glucose_category'] = pd.cut(
        df['LBXGLU'],
        bins=[0, 100, 126, 500],
        labels=['Normal', 'Prediabetes', 'Diabetes'],
        right=False
    )
    print(" Created glucose_category (ADA criteria)")
    
    # Triglycerides categories (ATP 3 criteria)
    # Normal: <150 mg/dL
    # Borderline high: 150-199 mg/dL
    # High: 200-499 mg/dL
    # Very high: ≥500 mg/dL
    df['triglycerides_category'] = pd.cut(
        df['LBXTLG'],
        bins=[0, 150, 200, 500, 5000],
        labels=['Normal', 'Borderline', 'High', 'Very High'],
        right=False
    )
    print(" Created triglycerides_category (ATP 3 criteria)")
    
    # Waist circumference risk (sex-specific, ATP 3 criteria)
    # Men: >102 cm = high risk
    # Women: >88 cm = high risk
    df['waist_risk'] = 'Normal'
    df.loc[(df['RIAGENDR'] == 1) & (df['BMXWAIST'] > 102), 'waist_risk'] = 'High Risk'
    df.loc[(df['RIAGENDR'] == 2) & (df['BMXWAIST'] > 88), 'waist_risk'] = 'High Risk'
    print("✓ Created waist_risk (ATP III sex-specific criteria)")
    
    print(f"\nTotal derived variables created: 6")
   
    return df


def save_processed_data(df: pd.DataFrame,  output_dir: str = "data/processed",filename: str = "nhanes_metabolic_analysis_ready.csv") -> None:
    #save processed dataset to csb
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    filepath = output_path / filename
    df.to_csv(filepath, index=False)
    
    print(f"\n✓ Processed data saved to: {filepath}")
    print(f"  Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"  File size: {filepath.stat().st_size / 1024:.1f} KB")


def generate_preprocessing_report(df: pd.DataFrame,  exclusion_stats: Dict, output_dir: str = "results/tables") -> None:
    # genereate asummary report of the preprocessing steps
        
    report_lines = []
    report_lines.append("NHANES metabolic phenotypes preprocessing report ")
    report_lines.append("")
    
    # Sample size information
    report_lines.append("sample size summary")
    report_lines.append(f"Starting sample (all demographics):  {exclusion_stats['n_start']:>7,}")
    report_lines.append(f"Excluded - Age <18:                   {exclusion_stats['n_under_age']:>7,}")
    report_lines.append(f"Excluded - Missing core variables:    {exclusion_stats['n_incomplete_core']:>7,}")
    report_lines.append(f"Final analysis sample:                {exclusion_stats['n_final']:>7,}")
    report_lines.append(f"Retention rate:                       {exclusion_stats['retention_rate']:>6.1f}%")
    report_lines.append("")
    
    # variable summary
    report_lines.append("Variables in final dataset")
    report_lines.append(f"Total variables: {len(df.columns)}")
    report_lines.append("")
    report_lines.append("Core clustering variables:")
    for var in ['LBXGLU', 'LBXTLG', 'BMXWAIST']:
        report_lines.append(f"  • {var}")
    report_lines.append("")
    report_lines.append("Demographic variables:")
    for var in ['RIDAGEYR', 'RIAGENDR', 'RIDRETH3', 'DMDEDUC2']:
        report_lines.append(f"  • {var}")
    report_lines.append("")
    report_lines.append("Derived variables:")
    for var in ['age_group', 'sex_label', 'bmi_category', 'glucose_category', 
                'triglycerides_category', 'waist_risk']:
        report_lines.append(f"  • {var}")
    report_lines.append("")
    
    # descriptive statistics
    report_lines.append("descriptive statistics: core variable")
    
    core_stats = df[['LBXGLU', 'LBXTLG', 'BMXWAIST', 'RIDAGEYR']].describe()
    report_lines.append(core_stats.to_string())
    report_lines.append("")
    
    # category distributions
    report_lines.append("Clinical category distribution")
    
    # glucose categories
    if 'glucose_category' in df.columns:
        report_lines.append("\nGlucose Status:")
        glucose_dist = df['glucose_category'].value_counts().sort_index()
        for cat, count in glucose_dist.items():
            pct = count / len(df) * 100
            report_lines.append(f"  {cat:15s}: {count:>5,} ({pct:>5.1f}%)")
    
    # triglycerides categories
    if 'triglycerides_category' in df.columns:
        report_lines.append("\nTriglycerides Status:")
        trig_dist = df['triglycerides_category'].value_counts().sort_index()
        for cat, count in trig_dist.items():
            pct = count / len(df) * 100
            report_lines.append(f"  {cat:15s}: {count:>5,} ({pct:>5.1f}%)")
    
    # waist risk
    if 'waist_risk' in df.columns:
        report_lines.append("\nWaist Circumference Risk:")
        waist_dist = df['waist_risk'].value_counts().sort_index()
        for cat, count in waist_dist.items():
            pct = count / len(df) * 100
            report_lines.append(f"  {cat:15s}: {count:>5,} ({pct:>5.1f}%)")
    
    report_lines.append("")
    report_lines.append(f"Report generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
    # print to console
    report_text = "\n".join(report_lines)
    print("\n" + report_text)
    
    # save to file
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    report_file = output_path / "preprocessing_report.txt"
    with open(report_file, 'w') as f:
        f.write(report_text)
    
    print(f"\nReport saved to: {report_file}")


def preprocess_nhanes_data(min_age: int = 18,
                            save_output: bool = True) -> pd.DataFrame:
    #main preprocesing pipeline:load, merge, filter and prep data
        
    print("\n NHANES METABOLIC PHENOTYPES PREPROCESSING PIPELINE" )
    print("\nStep 1: Loading NHANES data files...")
    data = load_nhanes_data()
    print("\nStep 2: Merging datasets...")
    merged_df = merge_nhanes_datasets(data)
    print("\nStep 3: Filtering to eligible participants...")
    filtered_df, exclusion_stats = filter_to_eligible_sample(
        merged_df, 
        min_age=min_age,
        require_core_vars=True
    )
    
    print("\nStep 4: Creating derived variables...")
    processed_df = create_derived_variables(filtered_df)
    if save_output:
        print("\nStep 5: Saving processed data and report...")
        save_processed_data(processed_df)
        generate_preprocessing_report(processed_df, exclusion_stats)
    
    print("\n" + "="*80)
    print(" PREPROCESSING COMPLETE")
    print(f"Final dataset: {processed_df.shape[0]:,} participants × {processed_df.shape[1]} variables")
    
    return processed_df


if __name__ == "__main__":
    # Run preprocessing
    df = preprocess_nhanes_data(min_age=18, save_output=True)
    
    print("\n Preprocessing pipeline completed successfully!") #pleaseeeee work
    print(f"  Access processed data at: data/processed/nhanes_metabolic_analysis_ready.csv")
    print(f"  View report at: results/tables/preprocessing_report.txt")

