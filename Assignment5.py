Assignment5
KIRTI KHATRI , 2501201005 , BCA(AI/DS) , SEM 1


Student Performance Analysis Pipeline

import argparse
import os
import sys
from dataclasses import dataclass, field
from typing import List, Dict, Any

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ---------------------------
# OOP Student model
# ---------------------------
@dataclass
class Student:
    student_id: str
    name: str
    klass: str
    marks: Dict[str, float] = field(default_factory=dict)

    def total(self) -> float:
        return float(sum(self.marks.values()))

    def average(self) -> float:
        if not self.marks:
            return 0.0
        return float(np.mean(list(self.marks.values())))

    def grade(self) -> str:
        avg = self.average()
        if avg >= 90:
            return 'A+'
        if avg >= 80:
            return 'A'
        if avg >= 70:
            return 'B'
        if avg >= 60:
            return 'C'
        if avg >= 50:
            return 'D'
        return 'F'


# ---------------------------
# Data ingestion & validation
# ---------------------------

def load_csv(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path)
    except Exception as e:
        raise RuntimeError(f"Failed to read CSV at {path}: {e}")
    return df


def validate_and_clean(df: pd.DataFrame, mark_min=0, mark_max=100) -> pd.DataFrame:
    # Minimal required columns
    required = {'student_id', 'name'}
    if not required.issubset(set(df.columns)):
        missing = required - set(df.columns)
        raise ValueError(f"Missing required columns: {missing}")

    # Identify subject columns as numeric columns excluding student_id, name, class
    non_subjects = {'student_id', 'name', 'class'}
    subject_cols = [c for c in df.columns if c not in non_subjects]

    if not subject_cols:
        raise ValueError("No subject columns detected. Include at least one subject column (e.g., Math, English).")

    # Trim whitespace from string columns
    df['student_id'] = df['student_id'].astype(str).str.strip()
    df['name'] = df['name'].astype(str).str.strip()
    if 'class' in df.columns:
        df['class'] = df['class'].astype(str).str.strip()
    else:
        df['class'] = 'Unknown'

    # Drop duplicate student_id rows, keep first
    before = len(df)
    df = df.drop_duplicates(subset=['student_id'], keep='first')
    if len(df) != before:
        print(f"Dropped {before - len(df)} duplicate student rows based on student_id.")

    # Convert subject columns to numeric, coerce errors to NaN
    for col in subject_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Flag rows with all subject marks missing -> drop
    all_missing = df[subject_cols].isna().all(axis=1)
    if all_missing.any():
        count = all_missing.sum()
        print(f"Dropping {count} rows where all subject marks are missing.")
        df = df.loc[~all_missing].copy()

    # Impute missing marks per subject with median of that subject
    for col in subject_cols:
        median = df[col].median(skipna=True)
        if np.isnan(median):
            median = 0.0
        df[col] = df[col].fillna(median)

    # Clip marks to allowed range
    for col in subject_cols:
        df[col] = df[col].clip(lower=mark_min, upper=mark_max)

    # Reset index
    df = df.reset_index(drop=True)
    return df


# ---------------------------
# Analysis & statistics
# ---------------------------

def compute_student_summary(df: pd.DataFrame) -> pd.DataFrame:
    non_subjects = {'student_id', 'name', 'class'}
    subjects = [c for c in df.columns if c not in non_subjects]

    summary = df.copy()
    summary['total'] = summary[subjects].sum(axis=1)
    summary['average'] = summary[subjects].mean(axis=1)

    # Percentiles
    summary['percentile'] = summary['average'].rank(pct=True) * 100
    summary['grade'] = summary['average'].apply(lambda x: _grade_from_avg(x))

    # Round some columns
    summary['average'] = summary['average'].round(2)
    summary['percentile'] = summary['percentile'].round(2)

    return summary[['student_id', 'name', 'class'] + subjects + ['total', 'average', 'percentile', 'grade']]


def _grade_from_avg(avg: float) -> str:
    if avg >= 90:
        return 'A+'
    if avg >= 80:
        return 'A'
    if avg >= 70:
        return 'B'
    if avg >= 60:
        return 'C'
    if avg >= 50:
        return 'D'
    return 'F'


def compute_class_stats(df: pd.DataFrame) -> pd.DataFrame:
    non_subjects = {'student_id', 'name', 'class'}
    subjects = [c for c in df.columns if c not in non_subjects]

    agg = df.groupby('class')[subjects].agg(['count', 'mean', 'median', 'std', 'min', 'max'])
    # Flatten columns
    agg.columns = ['_'.join(col).strip() for col in agg.columns.values]
    agg = agg.reset_index()
    return agg


# ---------------------------
# Visualizations
# ---------------------------

def plot_avg_histogram(summary_df: pd.DataFrame, outpath: str):
    plt.figure(figsize=(8, 5))
    plt.hist(summary_df['average'], bins=10)
    plt.xlabel('Average Marks')
    plt.ylabel('Number of Students')
    plt.title('Histogram of Student Averages')
    plt.grid(axis='y', alpha=0.6)
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()


def plot_subject_boxplot(df: pd.DataFrame, outpath: str):
    non_subjects = {'student_id', 'name', 'class'}
    subjects = [c for c in df.columns if c not in non_subjects]
    plt.figure(figsize=(10, 6))
    data = [df[s].values for s in subjects]
    plt.boxplot(data, labels=subjects, showmeans=True)
    plt.xlabel('Subject')
    plt.ylabel('Marks')
    plt.title('Boxplot of Marks by Subject')
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()


def plot_subject_corr_heatmap(df: pd.DataFrame, outpath: str):
    non_subjects = {'student_id', 'name', 'class'}
    subjects = [c for c in df.columns if c not in non_subjects]
    corr = df[subjects].corr()

    plt.figure(figsize=(8, 6))
    plt.imshow(corr.values, interpolation='nearest', aspect='auto')
    plt.colorbar()
    plt.xticks(range(len(subjects)), subjects, rotation=45, ha='right')
    plt.yticks(range(len(subjects)), subjects)
    plt.title('Correlation Matrix of Subjects')
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()


# ---------------------------
# Pipeline orchestration
# ---------------------------

def pipeline(input_csv: str, outdir: str):
    os.makedirs(outdir, exist_ok=True)

    print(f"Loading data from: {input_csv}")
    df = load_csv(input_csv)

    print("Validating and cleaning data...")
    clean_df = validate_and_clean(df)

    cleaned_csv = os.path.join(outdir, 'cleaned_data.csv')
    clean_df.to_csv(cleaned_csv, index=False)
    print(f"Saved cleaned data -> {cleaned_csv}")

    print("Computing student summaries...")
    student_summary = compute_student_summary(clean_df)
    summary_csv = os.path.join(outdir, 'student_summary.csv')
    student_summary.to_csv(summary_csv, index=False)
    print(f"Saved student summary -> {summary_csv}")

    print("Computing class-level statistics...")
    class_stats = compute_class_stats(clean_df)
    class_csv = os.path.join(outdir, 'class_stats.csv')
    class_stats.to_csv(class_csv, index=False)
    print(f"Saved class stats -> {class_csv}")

    # Plots
    print("Creating plots...")
    plot_avg_histogram(student_summary, os.path.join(outdir, 'avg_histogram.png'))
    plot_subject_boxplot(clean_df, os.path.join(outdir, 'subject_boxplot.png'))
    plot_subject_corr_heatmap(clean_df, os.path.join(outdir, 'subject_correlation_heatmap.png'))
    print(f"Plots saved in {outdir}")

    # Return objects for further programmatic use
    return {
        'clean_df': clean_df,
        'student_summary': student_summary,
        'class_stats': class_stats,
        'outdir': outdir,
    }


# ---------------------------
# CLI
# ---------------------------

def parse_args(argv=None):
    parser = argparse.ArgumentParser(description='Student Performance Analysis Pipeline')
    parser.add_argument('--input', '-i', required=True, help='Path to input CSV file')
    parser.add_argument('--outdir', '-o', default='output', help='Directory to save outputs')
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    try:
        results = pipeline(args.input, args.outdir)
        print("Pipeline completed successfully.")
        print(f"Outputs written to: {results['outdir']}")
    except Exception as e:
        print(f"Pipeline failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
