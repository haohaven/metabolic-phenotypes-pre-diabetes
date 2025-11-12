"""
Data loading utilities for NHANES 2021-2023 metabolic phenotypes project.

This module provides functions to load and validate NHANES XPT files
for the metabolic clustering analysis.

Author: Hajar (haohaven)
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Optional
import warnings
REPO_ROOT = Path(__file__).resolve().parents[2]

def load_nhanes_data(data_dir: Optional[str] = None) -> Dict[str, pd.DataFrame]:
    if data_dir is None:
        data_dir = REPO_ROOT / "data" / "raw"
    else:
        data_dir = Path(data_dir)

    #load all required NHANES XPT files 
    data_path = Path(data_dir)
    
    #here we define the files and their respective directories 
    files = {
        "glucose": "GLU_L.xpt",
        "triglycerides": "TRIGLY_L.xpt",
        "body_measures": "BMX_L.xpt",
        "demographics": "DEMO_L.xpt"
    }
    # load (with validation) each files 
    datasets = {}
    print("Loading NHANES data files...")
    print("=" * 60)
    
    for key, filename in files.items():
        filepath = data_path / filename
        print(f"Looking for {filename} in {filepath.resolve()}")#added a debug print here to make sure file rlly exists

        #just to be sure, checking if the file exists

        if not filepath.exists():
            raise FileNotFoundError(
                f"Missing required file: {filepath}\n"
                f"Please ensure all NHANES XPT files are downloaded to {data_dir}/\n"
                f"Expected files: {list(files.values())}"
            )
        #loaad the files
        try:
            df = pd.read_sas(filepath, format='xport', encoding='utf-8')
            datasets[key] = df
            #print to comfirm that the files are loading
            print(f"{key:15s} | {df.shape[0]:>6,} rows × {df.shape[1]:>3} columns | {filename}")
            
        except Exception as e:
            raise RuntimeError(
                f"failed to load {filename}. "
                f"Filee may be corrupted or in wrong format.\n"
                f"error: {str(e)}"
            )
    
    print("=" * 60)
    print(f"Successfully loaded {len(datasets)} datasets\n")
    
    return datasets


def get_key_variables() -> Dict[str, list]:
    '''return dictionary mapping datasets to their key analysis variabless (this function documents which 
    variables from each NHANES file are essential fot the metabolic clustering analysis
    '''
    
    return {
        "glucose": [
            "SEQN",      # Respondent ID
            "LBXGLU",    # Fasting glucose (mg/dL)
            "LBDGLUSI",  # Fasting glucose (mmol/L)
            "WTSAF2YR"   # Fasting sample 2-year weight
        ],
        "triglycerides": [
            "SEQN",      # Respondent ID
            "LBXTLG",    # Triglycerides (mg/dL) 
            "LBDTRSI",   # Triglycerides (mmol/L)
            "WTSAF2YR"   # Fasting sample 2-year weight
        ],
        "body_measures": [
            "SEQN",      # Respondent ID
            "BMXWAIST",  # Waist circumference (cm)
            "BMXBMI",    # Body mass index
            "BMXWT",     # Weight (kg)
            "BMXHT"      # Height (cm)
        ],
        "demographics": [
            "SEQN",      # Respondent ID
            "RIDAGEYR",  # Age (years)
            "RIAGENDR",  # Gender
            "RIDRETH3",  # Race/ethnicity
            "DMDEDUC2",  # Education level
            "WTINT2YR",  # Interview weight
            "WTMEC2YR"   # Examination weight
        ]
    }


def validate_key_variables(datasets: Dict[str, pd.DataFrame]) -> bool:
    #check if all variables exist in the datasets loaded 
    
    key_vars = get_key_variables()
    all_valid = True
    
    print("validating key variables...")
    print("=" * 60)
    
    for dataset_name, var_list in key_vars.items():
        if dataset_name not in datasets:
            print(f"{dataset_name}: dataset not loaded")
            all_valid = False
            continue
            
        df = datasets[dataset_name]
        missing_vars = [v for v in var_list if v not in df.columns]
        
        if missing_vars:
            print(f"{dataset_name:15s} | missing: {missing_vars}")
            all_valid = False
        else:
            print(f"{dataset_name:15s} | All {len(var_list)} key variables present")
    
    print("=" * 60)
    if all_valid:
        print("All key variables validated\n")
    else:
        warnings.warn("Some key variables are missing, check their names.")
    
    return all_valid


def print_data_summary(datasets: Dict[str, pd.DataFrame]) -> None:
    #print detailed summary statisics
    
    print("\nDATASET SUMMARY")
    print("=" * 80)
    
    for name, df in datasets.items():
        memory_mb = df.memory_usage(deep=True).sum() / (1024 ** 2)
        
        print(f"\n{name.upper()}")
        print(f"  Shape:        {df.shape[0]:>7,} rows × {df.shape[1]:>3} columns")
        print(f"  Memory:       {memory_mb:>7.2f} MB")
        print(f"  Unique IDs:   {df['SEQN'].nunique():>7,}")
        print(f"  Columns:      {', '.join(df.columns[:8].tolist())}...")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    #test the data loading func when script is run directly 
    print("NHANES Data Loading Test")
    print("=" * 80)
    print()
    
    try:
        # load all (4) datasets
        data = load_nhanes_data()
        
        # validate key variables
        validate_key_variables(data)
        
        # print summary
        print_data_summary(data)
        
        print("\n All tests passed! Data loading module is ready.\n")
        
    except FileNotFoundError as e:
        print(f"\n File Error: {e}\n")
    except RuntimeError as e:
        print(f"\n Loading Error: {e}\n")
    except Exception as e:
        print(f"\n Unexpected Error: {e}\n")