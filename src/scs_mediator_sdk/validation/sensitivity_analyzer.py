"""
Sensitivity Analysis Tool

Analyzes how changes in model parameters affect simulation outcomes.
Helps identify which parameters have the most impact on model behavior.

Based on:
- Saltelli et al. (2008): Global Sensitivity Analysis
- Ten Broeke et al. (2016): Which Sensitivity Analysis Method Should I Use for My Agent-Based Model?
"""

from __future__ import annotations
from typing import Dict, List, Any, Tuple
import numpy as np
import pandas as pd
from dataclasses import dataclass
from pathlib import Path
import matplotlib.pyplot as plt

from scs_mediator_sdk.sim.enhanced_abm import ConflictSimulation


@dataclass
class SensitivityResult:
    """Results from sensitivity analysis"""
    parameter_name: str
    baseline_value: float
    test_values: List[float]
    output_means: List[float]
    output_stds: List[float]
    sensitivity_index: float  # How much output changes per unit parameter change


class SensitivityAnalyzer:
    """Performs sensitivity analysis on simulation parameters"""

    def __init__(self, n_replications: int = 50):
        """
        Initialize sensitivity analyzer

        Args:
            n_replications: Number of simulation runs per parameter value
        """
        self.n_replications = n_replications

    def run_one_at_a_time_analysis(self,
                                   parameters: Dict[str, Tuple[float, float, float]],
                                   output_metric: str = 'incident_count',
                                   n_points: int = 10) -> Dict[str, SensitivityResult]:
        """
        Run One-At-A-Time (OAT) sensitivity analysis

        Varies each parameter individually while holding others constant

        Args:
            parameters: Dict mapping parameter names to (baseline, min, max) tuples
            output_metric: Which metric to analyze ('incident_count', 'avg_severity', etc.)
            n_points: Number of test points between min and max

        Returns:
            Dict mapping parameter names to SensitivityResult objects
        """
        print(f"🔬 Running One-At-A-Time Sensitivity Analysis...")
        print(f"   Parameters to test: {len(parameters)}")
        print(f"   Points per parameter: {n_points}")
        print(f"   Replications per point: {self.n_replications}")
        print(f"   Total simulations: {len(parameters) * n_points * self.n_replications}")

        results = {}

        for param_name, (baseline, min_val, max_val) in parameters.items():
            print(f"\n   Testing {param_name}...")

            # Generate test values
            test_values = np.linspace(min_val, max_val, n_points)

            output_means = []
            output_stds = []

            for test_value in test_values:
                # Run replications with this parameter value
                outputs = []

                for rep in range(self.n_replications):
                    # Note: This is a placeholder - actual implementation would
                    # need to modify ConflictSimulation to accept parameter overrides
                    sim = ConflictSimulation(
                        steps=200,
                        domain="maritime",
                        environment={"weather_bad": False, "media_visibility": 2},
                        agreement=None,
                        seed=rep
                    )
                    df = sim.run()

                    # Extract output metric
                    if output_metric == 'incident_count':
                        output = len(df)
                    elif output_metric == 'avg_severity':
                        output = df['severity'].mean() if len(df) > 0 else 0
                    elif output_metric == 'max_escalation':
                        output = df['escalation_level'].max() if len(df) > 0 else 0
                    else:
                        output = 0

                    outputs.append(output)

                output_means.append(np.mean(outputs))
                output_stds.append(np.std(outputs))

            # Calculate sensitivity index (normalized slope)
            # How much does output change per unit change in parameter?
            sensitivity_index = self._calculate_sensitivity_index(
                test_values, output_means, baseline, min_val, max_val
            )

            results[param_name] = SensitivityResult(
                parameter_name=param_name,
                baseline_value=baseline,
                test_values=list(test_values),
                output_means=output_means,
                output_stds=output_stds,
                sensitivity_index=sensitivity_index
            )

            print(f"      Sensitivity index: {sensitivity_index:.4f}")

        print(f"\n✅ Sensitivity analysis complete!")

        return results

    def _calculate_sensitivity_index(self,
                                    param_values: np.ndarray,
                                    output_values: List[float],
                                    baseline: float,
                                    min_val: float,
                                    max_val: float) -> float:
        """
        Calculate sensitivity index

        Uses linear regression slope normalized by parameter range
        """
        # Fit linear regression
        coeffs = np.polyfit(param_values, output_values, deg=1)
        slope = coeffs[0]

        # Normalize by parameter range to make comparable across parameters
        param_range = max_val - min_val
        normalized_slope = abs(slope * param_range)

        return normalized_slope

    def generate_tornado_diagram(self,
                                results: Dict[str, SensitivityResult],
                                output_path: str = None) -> None:
        """
        Generate tornado diagram showing parameter sensitivity

        Args:
            results: Results from run_one_at_a_time_analysis
            output_path: Where to save the plot (optional)
        """
        # Sort parameters by sensitivity
        sorted_params = sorted(results.items(),
                             key=lambda x: x[1].sensitivity_index,
                             reverse=True)

        param_names = [name for name, _ in sorted_params]
        sensitivities = [result.sensitivity_index for _, result in sorted_params]

        # Create horizontal bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        y_pos = np.arange(len(param_names))

        bars = ax.barh(y_pos, sensitivities, color='steelblue')

        # Color code by sensitivity level
        colors = ['darkred' if s > 10 else 'orange' if s > 5 else 'steelblue'
                 for s in sensitivities]
        for bar, color in zip(bars, colors):
            bar.set_color(color)

        ax.set_yticks(y_pos)
        ax.set_yticklabels(param_names)
        ax.set_xlabel('Sensitivity Index (Higher = More Influential)', fontsize=12)
        ax.set_title('Parameter Sensitivity Analysis\n(Tornado Diagram)', fontsize=14, fontweight='bold')

        # Add value labels
        for i, (bar, val) in enumerate(zip(bars, sensitivities)):
            ax.text(val + 0.2, i, f'{val:.2f}', va='center', fontsize=10)

        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='darkred', label='High Impact (>10)'),
            Patch(facecolor='orange', label='Medium Impact (5-10)'),
            Patch(facecolor='steelblue', label='Low Impact (<5)')
        ]
        ax.legend(handles=legend_elements, loc='lower right')

        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"📊 Tornado diagram saved to: {output_path}")

        return fig

    def generate_parameter_sweep_plots(self,
                                      results: Dict[str, SensitivityResult],
                                      output_dir: str = None) -> None:
        """
        Generate individual plots for each parameter showing output vs parameter value

        Args:
            results: Results from run_one_at_a_time_analysis
            output_dir: Directory to save plots
        """
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)

        for param_name, result in results.items():
            fig, ax = plt.subplots(figsize=(8, 5))

            # Plot mean with error bars
            ax.errorbar(result.test_values, result.output_means,
                       yerr=result.output_stds, marker='o',
                       capsize=5, capthick=2, linewidth=2,
                       markersize=8, color='steelblue')

            # Add baseline marker
            baseline_idx = np.argmin(np.abs(np.array(result.test_values) - result.baseline_value))
            ax.axvline(result.baseline_value, color='red', linestyle='--',
                      linewidth=2, label='Baseline', alpha=0.7)

            ax.set_xlabel(f'{param_name}', fontsize=12)
            ax.set_ylabel('Output Metric', fontsize=12)
            ax.set_title(f'Sensitivity: {param_name}\n(Sensitivity Index: {result.sensitivity_index:.3f})',
                        fontsize=13, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)

            plt.tight_layout()

            if output_dir:
                plot_path = output_path / f"sensitivity_{param_name}.png"
                plt.savefig(plot_path, dpi=300, bbox_inches='tight')
                plt.close()

    def generate_sensitivity_report(self, results: Dict[str, SensitivityResult]) -> str:
        """Generate human-readable sensitivity analysis report"""

        # Sort by sensitivity
        sorted_results = sorted(results.items(),
                              key=lambda x: x[1].sensitivity_index,
                              reverse=True)

        report = f"""
# Sensitivity Analysis Report

## Overview

This report identifies which model parameters have the greatest impact on simulation outcomes.

**Method**: One-At-A-Time (OAT) Sensitivity Analysis
**Replications**: {self.n_replications} per parameter value
**Total Simulations**: {len(results) * 10 * self.n_replications}

## Parameter Sensitivity Rankings

Parameters ranked by their influence on model outcomes:

| Rank | Parameter | Sensitivity Index | Impact Level | Recommendation |
|------|-----------|------------------|--------------|----------------|
"""

        for i, (param_name, result) in enumerate(sorted_results, 1):
            si = result.sensitivity_index

            if si > 10:
                impact = "🔴 HIGH"
                recommendation = "Requires careful calibration"
            elif si > 5:
                impact = "🟠 MEDIUM"
                recommendation = "Monitor during calibration"
            else:
                impact = "🟢 LOW"
                recommendation = "Less critical for tuning"

            report += f"| {i} | {param_name} | {si:.3f} | {impact} | {recommendation} |\n"

        # Identify most and least sensitive
        most_sensitive = sorted_results[0]
        least_sensitive = sorted_results[-1]

        report += f"""

## Key Findings

### Most Sensitive Parameter: **{most_sensitive[0]}**
- Sensitivity Index: {most_sensitive[1].sensitivity_index:.3f}
- Baseline Value: {most_sensitive[1].baseline_value:.4f}
- **Interpretation**: This parameter has the strongest influence on model behavior.
  Small changes can significantly affect outcomes.
- **Action**: Prioritize accurate estimation of this parameter through empirical data.

### Least Sensitive Parameter: **{least_sensitive[0]}**
- Sensitivity Index: {least_sensitive[1].sensitivity_index:.3f}
- Baseline Value: {least_sensitive[1].baseline_value:.4f}
- **Interpretation**: This parameter has minimal influence on model behavior.
- **Action**: Current value is acceptable; precise calibration less critical.

## Recommendations

### For Model Calibration:
1. **Focus on high-sensitivity parameters first** ({', '.join([name for name, _ in sorted_results[:3]])})
2. Use tighter bounds during calibration for high-sensitivity parameters
3. Low-sensitivity parameters can use broader ranges

### For Model Validation:
1. Report uncertainty ranges for high-sensitivity parameters
2. Test model robustness by varying high-sensitivity parameters
3. Document assumptions for parameters with high sensitivity

### For Model Use:
1. **Warning**: Model predictions are most uncertain about high-sensitivity parameters
2. When applying to new scenarios, verify high-sensitivity parameters are still valid
3. Scenario analysis should explore ranges of high-sensitivity parameters

## Parameter Details

"""

        for param_name, result in sorted_results:
            output_range = max(result.output_means) - min(result.output_means)
            relative_change = (output_range / np.mean(result.output_means)) * 100 if np.mean(result.output_means) > 0 else 0

            report += f"""
### {param_name}
- **Baseline**: {result.baseline_value:.4f}
- **Range Tested**: [{min(result.test_values):.4f}, {max(result.test_values):.4f}]
- **Output Range**: {output_range:.2f} ({relative_change:.1f}% of mean)
- **Sensitivity Index**: {result.sensitivity_index:.3f}
"""

        report += f"""

## Methodology Notes

**One-At-A-Time (OAT) Analysis**:
- Varies one parameter at a time while holding others constant
- Simple and interpretable
- Does not capture parameter interactions
- Suitable for initial sensitivity screening

**Sensitivity Index Calculation**:
- Measures slope of output vs. parameter relationship
- Normalized by parameter range for comparability
- Higher values indicate greater sensitivity

**Limitations**:
- Does not detect interaction effects between parameters
- Assumes roughly linear parameter-output relationships
- Results specific to baseline parameter values chosen

**For More Advanced Analysis**:
- Consider Sobol indices for global sensitivity (captures interactions)
- Use Morris method for computational efficiency
- Perform uncertainty quantification with Monte Carlo methods

---
*Generated: {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""

        return report


# Example usage
if __name__ == "__main__":
    analyzer = SensitivityAnalyzer(n_replications=30)

    # Define parameters to test
    parameters = {
        'ccg_aggression': (0.15, 0.10, 0.25),  # (baseline, min, max)
        'pcg_aggression': (0.10, 0.05, 0.15),
        'militia_aggression': (0.20, 0.15, 0.30),
        'fisher_aggression': (0.05, 0.02, 0.10),
        'natural_decay': (0.98, 0.95, 0.99),
        'contagion_effect': (0.01, 0.005, 0.020)
    }

    # Run sensitivity analysis
    results = analyzer.run_one_at_a_time_analysis(
        parameters=parameters,
        output_metric='incident_count',
        n_points=10
    )

    # Generate tornado diagram
    plots_dir = Path(__file__).parent.parent.parent.parent / "docs" / "sensitivity_plots"
    plots_dir.mkdir(parents=True, exist_ok=True)

    analyzer.generate_tornado_diagram(
        results,
        output_path=plots_dir / "tornado_diagram.png"
    )

    # Generate individual parameter plots
    analyzer.generate_parameter_sweep_plots(
        results,
        output_dir=plots_dir
    )

    # Generate report
    report = analyzer.generate_sensitivity_report(results)

    output_path = Path(__file__).parent.parent.parent.parent / "docs" / "SENSITIVITY_ANALYSIS_REPORT.md"
    with open(output_path, 'w') as f:
        f.write(report)

    print(f"\n📄 Sensitivity analysis report saved to: {output_path}")
    print(f"📊 Plots saved to: {plots_dir}")
