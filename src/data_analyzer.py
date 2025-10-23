"""
Data Analysis System for MC AI
Upload datasets, find patterns, detect anomalies, create visualizations
"""

import os
import json
import numpy as np
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime
import base64
from io import BytesIO

class DataAnalyzer:
    """Complete data analysis system"""
    
    def __init__(self):
        self.data_path = "datasets"
        self.viz_path = "visualizations"
        os.makedirs(self.data_path, exist_ok=True)
        os.makedirs(self.viz_path, exist_ok=True)
        
        self.current_dataset = None
        self.dataset_name = None
    
    def upload_dataset(self, file_path: str, dataset_name: str = None) -> Dict:
        """Upload and process dataset file"""
        if not os.path.exists(file_path):
            return {'success': False, 'error': 'File not found'}
        
        ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if ext == '.csv':
                df = pd.read_csv(file_path)
            elif ext in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            elif ext == '.json':
                df = pd.read_json(file_path)
            else:
                return {'success': False, 'error': 'Unsupported file type'}
        except Exception as e:
            return {'success': False, 'error': f'Failed to load: {str(e)}'}
        
        self.current_dataset = df
        self.dataset_name = dataset_name if dataset_name else os.path.basename(file_path)
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        stats_summary = df[numeric_cols].describe().to_dict() if len(numeric_cols) > 0 else {}
        
        return {
            'success': True,
            'dataset_name': self.dataset_name,
            'shape': df.shape,
            'columns': list(df.columns),
            'preview': df.head(10).to_dict('records'),
            'statistics': stats_summary,
            'data_types': {k: str(v) for k, v in df.dtypes.items()}
        }
    
    def analyze_text_dataset(self, text: str) -> Dict:
        """Quick analysis from pasted text data"""
        try:
            from io import StringIO
            df = pd.read_csv(StringIO(text))
            self.current_dataset = df
            self.dataset_name = "Pasted Data"
            
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            stats_summary = df[numeric_cols].describe().to_dict() if len(numeric_cols) > 0 else {}
            
            return {
                'success': True,
                'dataset_name': self.dataset_name,
                'shape': df.shape,
                'columns': list(df.columns),
                'preview': df.head(10).to_dict('records'),
                'statistics': stats_summary,
                'data_types': {k: str(v) for k, v in df.dtypes.items()}
            }
        except:
            return {'success': False, 'error': 'Could not parse text as CSV'}
    
    def basic_statistics(self, columns: List[str] = None) -> Dict:
        """Calculate statistics"""
        if self.current_dataset is None:
            return {'error': 'No dataset loaded'}
        
        df = self.current_dataset
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        results = {}
        for col in columns:
            if col not in df.columns:
                continue
            
            data = df[col].dropna()
            results[col] = {
                'count': int(len(data)),
                'mean': float(data.mean()),
                'median': float(data.median()),
                'std': float(data.std()),
                'min': float(data.min()),
                'max': float(data.max()),
                'q25': float(data.quantile(0.25)),
                'q75': float(data.quantile(0.75))
            }
        
        return results
    
    def find_correlations(self, threshold: float = 0.5) -> Dict:
        """Find correlations"""
        if self.current_dataset is None:
            return {'error': 'No dataset loaded'}
        
        df = self.current_dataset
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) < 2:
            return {'error': 'Need at least 2 numeric columns'}
        
        corr_matrix = df[numeric_cols].corr(method='pearson')
        
        significant_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                col1 = corr_matrix.columns[i]
                col2 = corr_matrix.columns[j]
                corr_value = corr_matrix.iloc[i, j]
                
                if abs(corr_value) > threshold:
                    strength = 'strong' if abs(corr_value) > 0.7 else 'moderate'
                    significant_pairs.append({
                        'column1': col1,
                        'column2': col2,
                        'correlation': float(corr_value),
                        'strength': strength
                    })
        
        significant_pairs.sort(key=lambda x: abs(x['correlation']), reverse=True)
        
        return {
            'significant_pairs': significant_pairs,
            'correlation_matrix': corr_matrix.to_dict()
        }
    
    def detect_anomalies(self, column: Optional[str] = None, method: str = 'isolation_forest') -> Dict:
        """Detect anomalies"""
        if self.current_dataset is None:
            return {'error': 'No dataset loaded'}
        
        df = self.current_dataset
        
        if column:
            if column not in df.columns:
                return {'error': 'Column not found'}
            data = df[[column]].dropna()
        else:
            data = df.select_dtypes(include=[np.number]).dropna()
        
        if len(data) < 10:
            return {'error': 'Insufficient data'}
        
        anomalies: List = []
        
        if method == 'isolation_forest':
            from sklearn.ensemble import IsolationForest
            iso_forest = IsolationForest(contamination='auto', random_state=42)
            predictions = iso_forest.fit_predict(data)
            anomaly_indices = np.where(predictions == -1)[0].tolist()
            anomalies = data.iloc[anomaly_indices].to_dict('records')
        
        elif method == 'zscore':
            from scipy import stats
            z_scores = np.abs(stats.zscore(data, nan_policy='omit'))
            anomaly_indices = np.where(z_scores > 3)[0].tolist()
            anomalies = data.iloc[anomaly_indices].to_dict('records')
        
        elif method == 'iqr':
            anomaly_indices_list = []
            for col in data.columns:
                col_data = data[col].values
                Q1 = np.percentile(col_data, 25)
                Q3 = np.percentile(col_data, 75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                col_anomaly_indices = np.where((col_data < lower_bound) | (col_data > upper_bound))[0]
                anomaly_indices_list.extend(col_anomaly_indices.tolist())
            
            anomaly_indices = list(set(anomaly_indices_list))
            anomalies = data.iloc[anomaly_indices].to_dict('records') if anomaly_indices else []
        
        return {
            'method': method,
            'anomaly_count': len(anomalies),
            'anomalies': anomalies[:50],
            'total_records': len(data)
        }
    
    def detect_patterns(self, column: str) -> Dict:
        """Detect patterns in data"""
        if self.current_dataset is None:
            return {'error': 'No dataset loaded'}
        
        df = self.current_dataset
        if column not in df.columns:
            return {'error': 'Column not found'}
        
        data = df[column].dropna()
        data_values = data.values
        
        if len(data_values) < 10:
            return {'error': 'Insufficient data'}
        
        window = min(10, len(data_values) // 3)
        ma = pd.Series(data_values).rolling(window=window).mean()
        ma_values = ma.values
        
        slope = 0.0
        recent_trend = ma_values[-window:] if len(ma_values) >= window else ma_values
        if len(recent_trend) >= 2:
            slope = float((recent_trend[-1] - recent_trend[0]) / len(recent_trend))
            if slope > 0.01:
                trend = 'increasing'
            elif slope < -0.01:
                trend = 'decreasing'
            else:
                trend = 'stable'
        else:
            trend = 'unknown'
        
        diff_data = np.diff(data_values)
        volatility = float(np.std(diff_data)) if len(diff_data) > 0 else 0.0
        
        return {
            'trend': trend,
            'slope': slope,
            'volatility': volatility,
            'data_points': len(data_values)
        }
    
    def create_visualization(self, chart_type: str, columns: Optional[List[str]] = None) -> Dict:
        """Create data visualization"""
        if self.current_dataset is None:
            return {'error': 'No dataset loaded'}
        
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        df = self.current_dataset
        
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()[:3]
        
        plt.figure(figsize=(12, 6))
        
        if chart_type == 'histogram':
            for col in columns:
                plt.hist(df[col].dropna(), bins=30, alpha=0.6, label=col)
            plt.legend()
            plt.title('Distribution Analysis')
            plt.xlabel('Value')
            plt.ylabel('Frequency')
        
        elif chart_type == 'correlation':
            numeric_df = df[columns]
            sns.heatmap(numeric_df.corr(method='pearson'), annot=True, cmap='coolwarm', center=0)
            plt.title('Correlation Heatmap')
        
        elif chart_type == 'timeseries':
            for col in columns:
                plt.plot(df[col], label=col)
            plt.legend()
            plt.title('Time Series Analysis')
            plt.xlabel('Index')
            plt.ylabel('Value')
        
        elif chart_type == 'scatter':
            if len(columns) >= 2:
                plt.scatter(df[columns[0]], df[columns[1]], alpha=0.6)
                plt.xlabel(columns[0])
                plt.ylabel(columns[1])
                plt.title(f'{columns[0]} vs {columns[1]}')
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return {
            'success': True,
            'chart_type': chart_type,
            'image_data': f'data:image/png;base64,{img_base64}'
        }
    
    def generate_insights(self) -> str:
        """Generate AI insights from data"""
        if self.current_dataset is None:
            return "No dataset loaded for analysis."
        
        df = self.current_dataset
        insights = []
        
        insights.append(f"📊 **Dataset Overview:** {len(df)} rows, {len(df.columns)} columns")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            insights.append(f"📈 **Numeric Columns:** {', '.join(numeric_cols[:5])}")
            
            for col in numeric_cols[:3]:
                mean_val = df[col].mean()
                std_val = df[col].std()
                insights.append(f"  • {col}: Mean={mean_val:.2f}, Std={std_val:.2f}")
        
        missing = df.isnull().sum()
        if missing.sum() > 0:
            top_missing = missing[missing > 0].head(3)
            insights.append(f"⚠️ **Missing Data:** {', '.join([f'{k} ({v} missing)' for k, v in top_missing.items()])}")
        
        return "\n".join(insights)
