import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time

# Set Streamlit Page Configuration
st.set_page_config(layout="wide", page_title="Generic AI Data Profiler", initial_sidebar_state="expanded")

# --- 1. Utility Functions for Generic Analysis and Caching ---

# Constants
PALETTE_PRIMARY = '#1f77b4' # Deep Blue
PALETTE_SECONDARY = '#d7191c' # Deep Red

@st.cache_data
def generate_generic_plots(df):
    """Generates a diverse set of plots for data profiling based on column types."""
    # Set a professional plot style for better aesthetics
    plt.style.use('seaborn-v0_8-whitegrid') 
    plots = {}
    numeric_cols = df.select_dtypes(include=np.number).columns
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns

    # 1. Numeric Plots (Distribution, Outliers, Density)
    for i, col in enumerate(numeric_cols):
        data = df[col].dropna()
        if len(data) > 0 and data.nunique() > 10:
            
            # --- Histogram (Distribution) ---
            fig_hist, ax_hist = plt.subplots(figsize=(8, 4))
            sns.histplot(data, bins=30, kde=True, ax=ax_hist, color=PALETTE_PRIMARY)
            ax_hist.set_title(f'Distribution of {col.title()}', fontsize=12)
            plots[f'Dist_{col}'] = fig_hist
            
            # --- Box Plot (Outliers) ---
            fig_box, ax_box = plt.subplots(figsize=(8, 2))
            sns.boxplot(x=data, ax=ax_box, color=PALETTE_SECONDARY)
            ax_box.set_title(f'Box Plot of {col.title()} (Outliers)', fontsize=12)
            plots[f'Box_{col}'] = fig_box
            
            # --- Violin Plot (Density & Distribution) ---
            fig_violin, ax_violin = plt.subplots(figsize=(8, 4))
            sns.violinplot(x=data, y=[col] * len(data), ax=ax_violin, color='#fdae61', orient='h') # Orange/Peach
            ax_violin.set_title(f'Violin Plot of {col.title()} (Density)', fontsize=12)
            plots[f'Violin_{col}'] = fig_violin


    # 2. Categorical Plots (Counts, Proportion)
    for i, col in enumerate(categorical_cols):
        data = df[col].value_counts().dropna()
        if len(data) > 0:
            
            if data.nunique() <= 8:
                # --- Pie Chart (Proportion for low-cardinality) ---
                fig_pie, ax_pie = plt.subplots(figsize=(8, 8))
                ax_pie.pie(data, labels=data.index, autopct='%1.1f%%', startangle=90, 
                           colors=sns.color_palette("Set2"))
                ax_pie.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
                ax_pie.set_title(f'Proportion of {col.title()}', fontsize=14)
                plots[f'Pie_{col}'] = fig_pie
            
            # --- Count Plot (Top 10) ---
            fig_count, ax_count = plt.subplots(figsize=(8, 4))
            top_10 = data.nlargest(10)
            sns.barplot(x=top_10.index, y=top_10.values, ax=ax_count, palette="magma")
            ax_count.set_title(f'Top {len(top_10)} Counts for {col.title()}', fontsize=12)
            ax_count.set_xticklabels(ax_count.get_xticklabels(), rotation=45, ha='right')
            fig_count.tight_layout()
            plots[f'Count_{col}'] = fig_count
            
    return plots

@st.cache_data
def generate_missing_data_plot(df):
    """Generates a bar chart showing the percentage of missing values per column."""
    missing_data = df.isnull().sum()
    missing_data = missing_data[missing_data > 0]
    
    if missing_data.empty:
        return None
        
    missing_percentage = (missing_data / len(df)) * 100
    missing_df = pd.DataFrame({'Missing Count': missing_data, 'Missing Percentage': missing_percentage}).sort_values(by='Missing Percentage', ascending=False)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=missing_df.index, y='Missing Percentage', data=missing_df, ax=ax, palette='Reds_d')
    ax.set_title('Percentage of Missing Values Per Column', fontsize=14)
    ax.set_ylabel('Missing Percentage (%)')
    ax.set_xlabel('Columns')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    fig.tight_layout()
    return fig

@st.cache_data
def generate_correlation_matrix(df):
    """Generates a heatmap for correlation between all numeric features."""
    numeric_df = df.select_dtypes(include=np.number)
    if numeric_df.empty or len(numeric_df.columns) < 2:
        return None
        
    corr_matrix = numeric_df.corr()
    
    # Create the heatmap plot with enhanced aesthetics
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', 
                cbar_kws={'label': 'Correlation Coefficient'}, ax=ax, linewidths=.5, linecolor='black')
    ax.set_title('Global Feature Correlation Matrix (Numeric Features)', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    fig.tight_layout()
    return fig

@st.cache_data
def get_llm_reports_generic(df, file_identifier):
    """
    Simulates the AI call by generating dynamic, context-aware reports based on 
    the actual statistics of the DataFrame.
    """
    with st.spinner(f"Simulating AI analysis for {file_identifier}..."):
        # Simple simulated delay for better UX
        time.sleep(0.5)

        # --- Calculate Core Statistics ---
        total_rows = len(df)
        total_cols = len(df.columns)
        
        missing_count = df.isnull().sum().sum()
        missing_percentage = (missing_count / (total_rows * total_cols)) * 100
        
        numeric_cols = df.select_dtypes(include=np.number).columns
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns

        # --- Dynamic Report Generation Logic ---
        
        # 1. Data Quality Assessment based on Missing Data
        if missing_percentage == 0:
            quality_assessment = "Data quality is **excellent** with zero missing values across all fields, suggesting a very clean dataset for immediate use."
            quality_recommendation = "Due to high data quality, the focus shifts to advanced feature engineering."
        elif missing_percentage < 1:
            quality_assessment = f"Data quality is **high** with only {missing_percentage:.2f}% missing values. Imputation is likely only needed for critical modeling tasks."
            quality_recommendation = "Minor imputation (e.g., mean/median) for features with missing values is recommended."
        elif missing_percentage < 10:
            quality_assessment = f"**Moderate missing data** detected ({missing_percentage:.2f}%). Targeted investigation of missing columns is crucial."
            quality_recommendation = "Review the missing data structure. Consider dropping columns with >30% missingness or using advanced imputation (like MICE)."
        else:
            quality_assessment = f"**Significant data imputation** required ({missing_percentage:.2f}% missing). Priority should be placed on developing a robust strategy before modeling."
            quality_recommendation = "Begin with a data quality scrub: determine the source of missingness and apply aggressive imputation or feature removal."

        # 2. Recommendation based on feature type mix
        if len(numeric_cols) > 5 and len(categorical_cols) > 5:
            recommendation_focus = "Given the high dimensional mix of both numeric and categorical features, the next logical step is **Feature Engineering** to reduce dimensionality and apply robust encoding methods."
        else:
            recommendation_focus = "Focus on establishing a clear target variable. Since the feature count is moderate, a simple, interpretable model (like Decision Trees or Random Forests) can provide a strong baseline performance rapidly."
            
        # --- Constructing the Reports ---

        data_profile_summary = (
            f"The dataset **{file_identifier}** contains **{total_rows:,} records** and **{total_cols} features**. "
            f"It is primarily structured with **{len(numeric_cols)} numeric** features and **{len(categorical_cols)} categorical** features. "
            "A quick inspection suggests data types are appropriate, but further review of unique values in high-cardinality columns is advised."
        )
        
        data_quality_report = (
            f"**Data Quality Assessment:** {quality_assessment} "
            "Furthermore, initial visualizations (Box Plots, Violin Plots) should be checked for **severe outliers**, as these can dramatically impact model training. Please check the 'Anomaly Detection' section below."
        )
        
        insights_report = (
            f"**Key Structural Insight:** Correlation between numeric features ({len(numeric_cols)} total) is the primary area for exploration. "
            f"Initial statistics hint at variance and range differences, suggesting **feature scaling** (Normalization or Standardization) will be a mandatory preprocessing step."
        )
        
        recommendation_report = (
            f"**Actionable Recommendation:** {recommendation_focus} "
            f"Next steps include **feature scaling** for numeric columns and {quality_recommendation}"
        )
        
        return data_profile_summary, data_quality_report, insights_report, recommendation_report

# --- 2. Bivariate Analysis Function ---

def perform_bivariate_analysis(df, col1, col2):
    """
    Performs detailed analysis for two selected columns, including statistics and
    correlation/group plots based on data types.
    """
    plt.style.use('seaborn-v0_8-whitegrid')
    st.subheader(f"Feature Deep Dive: `{col1.title()}` vs. `{col2.title()}`")
    
    is_num1 = pd.api.types.is_numeric_dtype(df[col1])
    is_num2 = pd.api.types.is_numeric_dtype(df[col2])
    
    # Display Statistics for both columns
    stat_col1, stat_col2 = st.columns(2)
    with stat_col1:
        st.markdown(f"**Statistics for {col1.title()}**")
        st.dataframe(df[col1].describe().to_frame().T, use_container_width=True)
    with stat_col2:
        st.markdown(f"**Statistics for {col2.title()}**")
        st.dataframe(df[col2].describe().to_frame().T, use_container_width=True)
        
    st.markdown("---")
    
    if is_num1 and is_num2:
        # NUMERIC vs NUMERIC (Scatter & Correlation)
        st.markdown("### 📈 Numeric vs. Numeric Relationship")
        correlation = df[[col1, col2]].corr().iloc[0, 1]
        col_corr, col_scatter = st.columns([1, 2])
        
        with col_corr:
            st.metric(label=f"Pearson Correlation Coefficient", value=f"{correlation:.3f}")
            if abs(correlation) > 0.7: st.success("Strong Relationship")
            elif abs(correlation) < 0.2: st.warning("Weak Relationship")
            else: st.info("Moderate Relationship")

        with col_scatter:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.scatterplot(x=df[col1], y=df[col2], ax=ax, color=PALETTE_PRIMARY, alpha=0.6)
            ax.set_title(f'Scatter Plot of {col1.title()} vs {col2.title()}')
            st.pyplot(fig)
            
    elif (is_num1 and not is_num2) or (is_num2 and not is_num1):
        # NUMERIC vs CATEGORICAL (Grouped Box/Violin Plot)
        st.markdown("### 📊 Numeric Distribution Grouped by Category")
        numeric_col = col1 if is_num1 else col2
        categorical_col = col2 if is_num1 else col1
        
        if df[categorical_col].nunique() <= 15: # Limit for readability
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.boxplot(x=df[categorical_col], y=df[numeric_col], ax=ax, palette="Set2") 
            ax.set_title(f'Distribution of {numeric_col.title()} Grouped by {categorical_col.title()}', fontsize=14)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
            st.pyplot(fig)
            st.info(f"This plot compares the central tendency (median line) and spread of the **{numeric_col.title()}** feature across the unique groups in **{categorical_col.title()}**.")
        else:
            st.warning(f"Skipping grouped plot: **{categorical_col.title()}** has too many unique values ({df[categorical_col].nunique()}) for a readable visualization.")

    else:
        # CATEGORICAL vs CATEGORICAL (Cross-Tab/Heatmap)
        st.markdown("### 🗄️ Relationship between Two Categorical Features (Count Heatmap)")
        cross_tab = pd.crosstab(df[col1], df[col2])
        st.dataframe(cross_tab, use_container_width=True)
        
        if len(cross_tab.index) <= 15 and len(cross_tab.columns) <= 15:
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(cross_tab, annot=True, fmt='d', cmap='YlGnBu', ax=ax, linewidths=.5, linecolor='white')
            ax.set_title(f'Count Heatmap: {col1.title()} vs {col2.title()}', fontsize=14)
            st.pyplot(fig)
        else:
             st.warning("Skipping heatmap: One or both features have too many unique values for a readable cross-tab visualization.")


# --- 3. Target Variable Analysis (Logic) ---

def calculate_relationship_strength(df, target_col, feature_col):
    """
    Calculates a proxy metric for relationship strength based on feature types.
    Higher score means a stronger relationship.
    """
    temp_df = df.dropna(subset=[target_col, feature_col]).copy()
    
    is_target_num = pd.api.types.is_numeric_dtype(temp_df[target_col])
    is_feature_num = pd.api.types.is_numeric_dtype(temp_df[feature_col])

    if is_target_num and is_feature_num:
        # Numeric Target vs Numeric Feature: Absolute Correlation
        return abs(temp_df[target_col].corr(temp_df[feature_col]))
    
    elif is_target_num and not is_feature_num:
        # Numeric Target vs Categorical Feature: Std Dev of Grouped Means (ANOVA proxy)
        grouped_means = temp_df.groupby(feature_col)[target_col].mean()
        return grouped_means.std() / temp_df[target_col].std() if temp_df[target_col].std() > 0 else 0
        
    elif not is_target_num and is_feature_num:
        # Categorical Target vs Numeric Feature: Std Dev of Grouped Means (ANOVA proxy)
        grouped_means = temp_df.groupby(target_col)[feature_col].mean()
        return grouped_means.std() / temp_df[feature_col].std() if temp_df[feature_col].std() > 0 else 0
        
    elif not is_target_num and not is_feature_num:
        # Categorical Target vs Categorical Feature: Proxy based on count/proportion variance
        cross_tab = pd.crosstab(temp_df[target_col], temp_df[feature_col], normalize='all')
        return (cross_tab**2).sum().sum() # A simple sum of squared proportions as a variance proxy

    return 0.0

def analyze_target_variable(df, target_col):
    """Generates target distribution plot and identifies top predictors."""
    st.header(f"4. Target Variable Analysis: '{target_col.title()}'")
    
    # 1. Target Distribution
    is_target_num = pd.api.types.is_numeric_dtype(df[target_col])
    
    st.subheader(f"4.1. Target Distribution ({'Regression' if is_target_num else 'Classification'})")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    if is_target_num:
        sns.histplot(df[target_col].dropna(), kde=True, bins=30, ax=ax, color=PALETTE_PRIMARY)
        ax.set_title(f'Distribution of Target: {target_col.title()}')
        st.info("For Regression: Check for normality, skewness, and high variance.")
    else:
        counts = df[target_col].value_counts().nlargest(10)
        sns.barplot(x=counts.index, y=counts.values, ax=ax, palette="viridis")
        ax.set_title(f'Class Balance for Target: {target_col.title()}')
        ax.set_ylabel('Count')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        
        balance_check = counts.max() / counts.sum()
        if balance_check > 0.75 and counts.nunique() > 1:
             st.error("⚠️ **Severe Class Imbalance Detected!** The largest class makes up over 75% of the data. Use stratified sampling and specialized metrics (F1, AUC).")
        else:
             st.success("✅ Class Balance appears adequate for initial modeling.")

    fig.tight_layout()
    st.pyplot(fig)
    st.markdown("---")
    
    # 2. Identify Top 5 Predictors
    st.subheader("4.2. Top 5 Feature Predictors")
    
    relationship_scores = {}
    
    # Filter out the target column itself and non-useful columns (e.g., ID columns with high cardinality)
    cols_to_analyze = [col for col in df.columns if col != target_col and df[col].nunique() < len(df) * 0.9] 

    # Calculate strength for all valid features
    for feature in cols_to_analyze:
        score = calculate_relationship_strength(df, target_col, feature)
        relationship_scores[feature] = score

    # Sort and select top 5
    top_predictors = pd.Series(relationship_scores).sort_values(ascending=False).head(5)

    if top_predictors.empty:
        st.warning("Could not find suitable non-target features for analysis.")
        return

    st.markdown(f"The analysis identified **{len(top_predictors)}** features with the strongest relationship to `{target_col.title()}`.")
    st.dataframe(top_predictors.to_frame(name='Relationship Score (Proxy)'), use_container_width=True)
    st.markdown("---")
    
    # 3. Plot Top Predictors vs Target
    st.subheader("4.3. Top Predictor Visualizations")
    
    for i, (feature, score) in enumerate(top_predictors.items()):
        
        with st.expander(f"Top {i+1}: {feature.title()} (Score: {score:.3f})"):
            # Logic to generate the best plot for Target vs Feature
            
            is_feature_num = pd.api.types.is_numeric_dtype(df[feature])
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            if is_target_num and is_feature_num:
                # Num vs Num -> Scatter
                sns.scatterplot(x=df[feature], y=df[target_col], ax=ax, color=PALETTE_PRIMARY, alpha=0.6)
            elif is_target_num and not is_feature_num:
                # Num vs Cat -> Box Plot
                sns.boxplot(x=df[feature], y=df[target_col], ax=ax, palette="Set2")
                ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
            elif not is_target_num and is_feature_num:
                # Cat vs Num -> Box Plot
                sns.boxplot(x=df[target_col], y=df[feature], ax=ax, palette="Set2")
                ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
            elif not is_target_num and not is_feature_num:
                # Cat vs Cat -> Stacked Bar (or Count Plot on both)
                cross_tab_plot = pd.crosstab(df[target_col], df[feature], normalize='index')
                cross_tab_plot.plot(kind='bar', stacked=True, ax=ax, cmap='viridis')
                ax.legend(title=feature.title(), bbox_to_anchor=(1.05, 1), loc='upper left')
                ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
                ax.set_ylabel('Proportion')
                
            ax.set_title(f'Relationship: {feature.title()} vs. Target {target_col.title()}')
            fig.tight_layout()
            st.pyplot(fig)

# --- 4. Anomaly Detection Logic ---

@st.cache_data
def calculate_outlier_metrics(df):
    """Calculates IQR-based outlier metrics and finds the top anomalous rows."""
    numeric_df = df.select_dtypes(include=np.number)
    if numeric_df.empty:
        return pd.DataFrame(), pd.DataFrame()

    outlier_data = []
    
    # Calculate IQR and bounds (1.5 * IQR Rule)
    Q1 = numeric_df.quantile(0.25)
    Q3 = numeric_df.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Identify outliers per column
    for col in numeric_df.columns:
        series = numeric_df[col].dropna()
        if series.empty: continue
            
        l_bound = lower_bound[col]
        u_bound = upper_bound[col]
        
        # Count outliers
        outliers_low = series[series < l_bound].count()
        outliers_high = series[series > u_bound].count()
        total_outliers = outliers_low + outliers_high
        
        total_count = len(series)
        
        outlier_data.append({
            'Feature': col,
            'Outlier Count (1.5*IQR)': total_outliers,
            'Outlier %': (total_outliers / total_count) * 100 if total_count > 0 else 0,
            'Lower Bound': f"{l_bound:,.2f}",
            'Upper Bound': f"{u_bound:,.2f}",
        })
        
    metrics_df = pd.DataFrame(outlier_data).sort_values(by='Outlier Count (1.5*IQR)', ascending=False).reset_index(drop=True)
    
    # Simulate identifying top anomalous rows (using Z-score deviation sum as a proxy)
    # This is a simple measure of how far a row deviates across all numeric features.
    z_scores = (numeric_df - numeric_df.mean()) / numeric_df.std()
    
    # Calculate an 'Anomaly Score' for each row based on the sum of absolute Z-scores
    anomaly_scores = z_scores.abs().sum(axis=1)
    
    # Get the top 5 most anomalous rows
    top_rows_index = anomaly_scores.nlargest(5).index
    
    if len(top_rows_index) == 0:
        return metrics_df, pd.DataFrame()

    top_rows = df.iloc[top_rows_index].copy()
    
    # Add the score to the top rows dataframe
    top_rows['Anomaly_Score_Proxy'] = anomaly_scores.loc[top_rows_index].round(2)
    top_rows = top_rows.sort_values(by='Anomaly_Score_Proxy', ascending=False)
    
    # Reindex for better display
    top_rows.index.name = 'Original Index'

    return metrics_df, top_rows


# --- 5. Feature Engineering Advice Logic ---

@st.cache_data
def get_feature_engineering_recommendations(df):
    """Provides actionable advice on numeric transformation and categorical encoding."""
    recommendations = {
        'scaling': "Since features likely have different scales and variances, **Standardization (Z-score)** or **Normalization (Min-Max)** is mandatory for distance-based models (e.g., K-Means, SVM, Neural Networks).",
        'numeric': [],
        'categorical': []
    }
    
    # 1. Numeric Transformation (Skewness)
    numeric_cols = df.select_dtypes(include=np.number).columns
    for col in numeric_cols:
        series = df[col].dropna()
        if len(series) > 10 and series.min() >= 0: # Only check skewness for non-negative data that might need log-transform
            # Calculate skewness
            skew_val = series.skew()
            
            if abs(skew_val) > 1.0: # Highly skewed threshold
                recommendations['numeric'].append({
                    'feature': col,
                    'skew': f"{skew_val:.2f}",
                    'advice': 'Highly skewed. Consider **Log Transformation** (for positive data) or **Box-Cox/Yeo-Johnson** to stabilize variance and improve model linearity.'
                })
            elif abs(skew_val) > 0.5: # Moderately skewed threshold
                recommendations['numeric'].append({
                    'feature': col,
                    'skew': f"{skew_val:.2f}",
                    'advice': 'Moderately skewed. May benefit from **Square Root** or other mild power transformation if residuals are non-normal.'
                })
    
    # 2. Categorical Encoding
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    for col in categorical_cols:
        cardinality = df[col].nunique()
        
        if cardinality <= 10 and cardinality > 1:
            recommendations['categorical'].append({
                'feature': col,
                'cardinality': cardinality,
                'advice': 'Low Cardinality. Best handled using **One-Hot Encoding** (creating dummy variables) for most models.'
            })
        elif cardinality > 10 and cardinality <= 50:
            recommendations['categorical'].append({
                'feature': col,
                'cardinality': cardinality,
                'advice': 'Medium Cardinality. Consider **Target Encoding** (if target is known) or grouping/binning categories before One-Hot Encoding to prevent dimensionality issues.'
            })
        elif cardinality > 50:
            recommendations['categorical'].append({
                'feature': col,
                'cardinality': cardinality,
                'advice': 'High Cardinality. **Target Encoding** or careful binning/feature removal is necessary. Avoid standard One-Hot Encoding as it will create too many features.'
            })
            
    return recommendations


# --- 6. Model Benchmarking Simulation Logic (NEW) ---

@st.cache_data
def simulate_model_benchmarks(df, target_col):
    """
    Simulates simple Linear/Logistic Regression and Decision Tree performance 
    to establish a quick, realistic baseline.
    """
    if not target_col or target_col not in df.columns:
        return None

    # Determine Model Type
    is_target_num = pd.api.types.is_numeric_dtype(df[target_col])
    
    # 1. Simulate Preprocessing Complexity Score (0.4 to 0.9)
    numeric_cols = df.select_dtypes(include=np.number).columns
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    
    missing_ratio = df.isnull().sum().sum() / (len(df) * len(df.columns)) if len(df) > 0 else 0
    # Penalize complexity for high missing data and high cardinality
    high_cardinality_count = sum(df[col].nunique() > 50 for col in categorical_cols)
    
    complexity_penalty = (missing_ratio * 0.5) + (high_cardinality_count / max(1, len(df.columns)) * 0.3)
    complexity_score = 1 - complexity_penalty
    complexity_score = max(0.4, min(0.9, complexity_score)) 
    
    results = {'Model Type': 'Classification' if not is_target_num else 'Regression'}
    
    # 2. Simulate Results
    if not is_target_num: # Classification
        base_accuracy = complexity_score * 0.85 
        
        # Logistic Regression
        results['Logistic Regression'] = {
            'Accuracy': max(0.5, base_accuracy + np.random.uniform(-0.05, 0.02)),
            'F1-Score': max(0.5, base_accuracy * 0.95 + np.random.uniform(-0.04, 0.01)),
            'Baseline': 'The simplest linear model, useful for quick separation and feature importance checks.',
            'MetricInfo': 'Accuracy and F1-Score are key for classification, especially F1 if classes are imbalanced.'
        }
        # Decision Tree Classifier
        results['Decision Tree'] = {
            'Accuracy': max(0.5, base_accuracy + np.random.uniform(-0.02, 0.05)),
            'F1-Score': max(0.5, base_accuracy * 1.05 + np.random.uniform(-0.03, 0.02)),
            'Baseline': 'Non-linear model, good for capturing complex interactions without excessive scaling/encoding.',
            'MetricInfo': 'Often better than Logistic Regression if the underlying feature interactions are strong.'
        }
        
    else: # Regression
        target_std = df[target_col].std() if df[target_col].std() > 0 else 1.0
        
        # Linear Regression Simulation
        sim_r2_lr = max(0.1, (complexity_score * 0.65) + np.random.uniform(-0.1, 0.05))
        sim_mae_lr = target_std * (1 - sim_r2_lr) * np.random.uniform(0.1, 0.5) 
        
        results['Linear Regression'] = {
            'R-squared': sim_r2_lr,
            'MAE': sim_mae_lr,
            'Baseline': 'The standard linear baseline. Performance indicates how well the target can be modeled linearly.',
            'MetricInfo': 'R-squared measures variance explained (0-1); MAE is the average absolute error in the target unit.'
        }
        
        # Decision Tree Regressor Simulation
        sim_r2_tree = max(0.1, (complexity_score * 0.65) + np.random.uniform(-0.05, 0.15))
        sim_mae_tree = target_std * (1 - sim_r2_tree) * np.random.uniform(0.08, 0.4)
        
        results['Decision Tree Regressor'] = {
            'R-squared': sim_r2_tree,
            'MAE': sim_mae_tree,
            'Baseline': 'A non-linear baseline, often capturing relationships missed by linear models.',
            'MetricInfo': 'If R-squared improves significantly here, non-linear relationships are likely dominant.'
        }

    return results


# --- 7. Main Streamlit App Layout ---

def run_app():
    
    st.title("🧠 Generic AI Data Profiler")
    st.markdown("Automated data structure analysis, visualization, and strategic reporting for any CSV dataset.")
    
    # File Uploader (Mandatory Start)
    uploaded_file = st.file_uploader("Upload any CSV data file", type="csv")

    if uploaded_file is None:
        st.info("⬆️ Please upload a CSV file to begin the generic profiling and AI analysis.")
        return # Stop execution until file is uploaded
    
    try:
        df = pd.read_csv(uploaded_file)
        file_name = uploaded_file.name.replace('.csv', '').replace('_', ' ').title()
        st.title(f"📊 Analysis of: {file_name}")
        
    except Exception as e:
        st.error(f"Error reading the file: {e}. Please ensure it is a valid CSV format.")
        return
    
    # --- Sidebar for Interactive Analysis ---
    st.sidebar.title("🛠️ Interactive Analysis Tools")
    
    PLACEHOLDER = "-- Select a Feature --"
    all_columns_with_placeholder = [PLACEHOLDER] + df.columns.tolist()
    
    # Target Column Selection
    st.sidebar.markdown("### 🎯 Predictor Selection")
    selected_target = st.sidebar.selectbox(
        "Select the **Target Column** (Y-Variable)",
        options=all_columns_with_placeholder,
        index=0 
    )

    # Generic Bivariate Analysis 
    st.sidebar.markdown("### 🔎 Generic Bivariate Comparison")
    selected_col1 = st.sidebar.selectbox(
        "Feature 1 (X-axis/Base)",
        options=all_columns_with_placeholder,
        index=0 
    )
    
    if selected_col1 == PLACEHOLDER:
         available_cols2 = all_columns_with_placeholder
    else:
         available_cols2 = [PLACEHOLDER] + [col for col in df.columns.tolist() if col != selected_col1]

    selected_col2 = st.sidebar.selectbox(
        "Feature 2 (Y-axis/Comparison)",
        options=available_cols2,
        index=0 
    )
    
    
    # --- Execute Analysis ---
    data_summary, data_quality, insights, recommendations = get_llm_reports_generic(df, file_name)
    outlier_metrics_df, top_anomalous_rows = calculate_outlier_metrics(df)
    fe_recommendations = get_feature_engineering_recommendations(df)
    
    try:
        profiler_plots = generate_generic_plots(df)
        missing_plot = generate_missing_data_plot(df)
    except Exception as e:
        st.error(f"An unexpected error occurred during plot generation: {e}")
        return

    
    # -------------------------------------------------------------
    # SECTION 1: AI-Generated Summaries and Context
    # -------------------------------------------------------------
    st.markdown("---")
    st.header("1. Data Structure & AI Context")
    
    data_col, report_col = st.columns([2, 3])
    
    with data_col:
        st.subheader("Raw Data Preview")
        st.dataframe(df.head(10), use_container_width=True)
        st.caption(f"First 10 rows of {file_name}.")

    with report_col:
        st.subheader("Data Profile Summary (AI Generated)")
        st.info(data_summary)
        
        st.subheader("Data Quality Assessment")
        st.warning(data_quality)

        
    # -------------------------------------------------------------
    # SECTION 2: Exploratory Data Analysis (EDA)
    # -------------------------------------------------------------
    st.markdown("---")
    st.header("2. Exploratory Data Visualizations (Comprehensive)")
    
    st.subheader("2.1. Missing Data Overview")
    if missing_plot:
        st.pyplot(missing_plot)
    else:
        st.success("No missing data found! The dataset is fully complete.")
        
    st.subheader("2.2. Feature Level Visuals")
    
    if profiler_plots:
        dist_plots = {k: v for k, v in profiler_plots.items() if k.startswith('Dist')}
        box_violin_plots = {k: v for k, v in profiler_plots.items() if k.startswith(('Box', 'Violin'))}
        categorical_plots = {k: v for k, v in profiler_plots.items() if k.startswith(('Count', 'Pie'))}
        
        with st.expander("📈 Numeric Feature Distributions (Histograms)", expanded=True):
            if dist_plots:
                cols = st.columns(2)
                for i, key in enumerate(dist_plots):
                    with cols[i % 2]:
                        st.pyplot(dist_plots[key])
            else:
                st.info("No numeric columns with enough unique values for distribution plots.")

        with st.expander("🔍 Feature Outliers & Density (Box/Violin Plots)"):
            if box_violin_plots:
                cols = st.columns(2)
                for i, key in enumerate(box_violin_plots):
                    with cols[i % 2]:
                        st.pyplot(box_violin_plots[key])
            else:
                st.info("No numeric columns for outlier/density plots.")

        with st.expander("📋 Categorical Feature Counts & Proportions"):
            if categorical_plots:
                cols = st.columns(2)
                for i, key in enumerate(categorical_plots):
                    with cols[i % 2]:
                        st.pyplot(categorical_plots[key])
            else:
                st.info("No categorical columns found.")
                
    else:
        st.info("No auto-plots could be generated.")


    # -------------------------------------------------------------
    # SECTION 3: Global Feature Relationships
    # -------------------------------------------------------------
    st.markdown("---")
    st.header("3. Global Feature Relationships")
    
    corr_plot = generate_correlation_matrix(df)
    
    if corr_plot:
        st.subheader("Correlation Heatmap for Numeric Features")
        st.pyplot(corr_plot)
    else:
        st.info("No numeric columns found to generate a global correlation matrix.")
        
    
    # -------------------------------------------------------------
    # SECTION 4: Target Variable Analysis 
    # -------------------------------------------------------------
    st.markdown("---")
    if selected_target != PLACEHOLDER:
        analyze_target_variable(df, selected_target)
    else:
        st.header("4. Target Variable Analysis (Select a Target in the Sidebar)")
        st.info("Please select a column in the 'Predictor Selection' area of the sidebar to activate predictive analysis.")
    
    
    # -------------------------------------------------------------
    # SECTION 5: Anomaly Detection & Outlier Quantification
    # -------------------------------------------------------------
    st.markdown("---")
    st.header("5. Anomaly Detection & Outlier Quantification")
    
    if not outlier_metrics_df.empty:
        st.subheader("5.1. Feature Outlier Metrics (1.5 * IQR Rule)")
        st.warning("Outliers can skew statistical measures and damage linear models. Features with high % should be winsorized or transformed.")
        st.dataframe(outlier_metrics_df, use_container_width=True)

        if not top_anomalous_rows.empty:
            st.subheader("5.2. Top 5 Most Anomalous Rows")
            st.info("These rows have the highest cumulative deviation across all numeric features and are prime candidates for manual review or removal.")
            st.dataframe(top_anomalous_rows, use_container_width=True)
        else:
            st.success("No highly anomalous rows detected based on the Z-score proxy.")
            
    else:
        st.info("No numeric columns available to perform Anomaly Detection.")

    # -------------------------------------------------------------
    # SECTION 6: Feature Engineering & Preprocessing Advice
    # -------------------------------------------------------------
    st.markdown("---")
    st.header("6. Feature Engineering & Preprocessing Advice")
    
    st.subheader("6.1. Scaling Requirement")
    st.success(fe_recommendations['scaling'])

    st.subheader("6.2. Numeric Transformation Advice (Skewness)")
    if fe_recommendations['numeric']:
        numeric_advice_df = pd.DataFrame(fe_recommendations['numeric'])
        numeric_advice_df = numeric_advice_df.rename(columns={'feature': 'Feature', 'skew': 'Skewness', 'advice': 'Recommendation'})
        st.warning("These features exhibit skewness and may violate linear model assumptions. Apply the recommended transformation.")
        st.dataframe(numeric_advice_df, use_container_width=True)
    else:
        st.success("Numeric features appear reasonably symmetrical or are low-count. Transformations may not be critical.")


    st.subheader("6.3. Categorical Encoding Strategy")
    if fe_recommendations['categorical']:
        categorical_advice_df = pd.DataFrame(fe_recommendations['categorical'])
        categorical_advice_df = categorical_advice_df.rename(columns={'feature': 'Feature', 'cardinality': 'Cardinality', 'advice': 'Encoding Strategy'})
        st.info("Choosing the correct encoding method is vital for managing feature complexity and model performance.")
        st.dataframe(categorical_advice_df, use_container_width=True)
    else:
        st.success("No categorical features found that require complex encoding.")
        
    
    # -------------------------------------------------------------
    # SECTION 7: Model Benchmarking Simulation (NEW)
    # -------------------------------------------------------------
    st.markdown("---")
    st.header("7. Model Benchmarking Simulation")

    if selected_target != PLACEHOLDER:
        benchmark_results = simulate_model_benchmarks(df, selected_target)
        model_type = benchmark_results.pop('Model Type')
        
        st.subheader(f"7.1. Baseline Performance ({model_type})")
        st.markdown(f"This simulation provides a **quick baseline score** using minimal preprocessing. All future, highly-engineered models should aim to significantly beat these scores.")

        cols = st.columns(len(benchmark_results))
        
        for i, (model_name, metrics) in enumerate(benchmark_results.items()):
            with cols[i]:
                st.markdown(f"#### {model_name}")
                st.markdown(f"**Description:** *{metrics.pop('Baseline')}*")
                
                # Display metrics
                for metric_name, value in metrics.items():
                    if 'Info' in metric_name:
                         st.caption(value)
                    elif metric_name == 'MAE':
                         st.metric(label=metric_name, value=f"{value:,.2f}")
                    else: # R-squared, Accuracy, F1-Score (as percentage)
                         st.metric(label=metric_name, value=f"{value:.2%}")
                         
                st.markdown("---")
    else:
        st.info("Select a **Target Column** in the sidebar to run the Model Benchmarking Simulation.")


    # -------------------------------------------------------------
    # SECTION 8: Interactive Feature Comparison (Generic Bivariate)
    # -------------------------------------------------------------
    st.markdown("---")
    st.header("8. Interactive Feature Comparison (Generic Bivariate)")
    st.markdown("Use the sidebar's 'Generic Bivariate Comparison' tool to select any two features to analyze their joint relationship.")
    
    if selected_col1 != PLACEHOLDER and selected_col2 != PLACEHOLDER and selected_col1 != selected_col2:
        perform_bivariate_analysis(df, selected_col1, selected_col2)
    else:
        st.info("Select two different columns in the left sidebar (under 'Generic Bivariate Comparison') to activate this section.")


    # -------------------------------------------------------------
    # SECTION 9: Insights and Recommendations
    # -------------------------------------------------------------
    st.markdown("---")
    st.header("9. Key Insights & Strategic Recommendations")
    st.markdown("Synthesis of data structure, quality, and potential next steps.")

    col_ins, col_rec = st.columns(2)

    with col_ins:
        st.subheader("AI-Generated Insights")
        st.success(insights)

    with col_rec:
        st.subheader("Strategic Recommendations")
        st.error(recommendations)
        
    st.markdown("---")
    st.caption("This dashboard is a **Generic Data Profiler** designed for active exploration.")

# Run the app
if __name__ == "__main__":
    run_app()