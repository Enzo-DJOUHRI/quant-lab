import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

class BacktestPlotter:

    def __init__(self, results_dict, output_dir="outputs/plots"):
        self.results_dict = results_dict
        output_path = Path(output_dir)
        if not output_path.is_absolute():
            project_root = Path(__file__).resolve().parent.parent
            output_path = project_root / output_path
        self.output_dir = output_path
    
    def plot_equity(self):
        fig = go.Figure()

        for name, results in self.results_dict.items():
            fig.add_trace(go.Scatter(
                            x= results.index,
                            y= results["equity"],
                            mode="lines",
                            name= name))
            
        fig.update_layout(title="Equity Curve Comparison",
                          xaxis_title="Date",
                          yaxis_title="Equity")

        self.output_dir.mkdir(parents=True, exist_ok=True)
        output_path = self.output_dir / "equity_curve_comparison.html"
        fig.write_html(output_path, include_plotlyjs="cdn")
        print(f"Plot saved to: {output_path.resolve()}")

    def plot_drawdown(self):
        fig = go.Figure()

        for name, results in self.results_dict.items():
            fig.add_trace(go.Scatter(
                            x= results.index,
                            y= results["drawdown"],
                            mode="lines",
                            name= name))
            
        fig.update_layout(title="Drawdown Curve Comparison",
                          xaxis_title="Date",
                          yaxis_title="Drawdown")

        self.output_dir.mkdir(parents=True, exist_ok=True)
        output_path = self.output_dir / "drawdown_curve_comparison.html"
        fig.write_html(output_path, include_plotlyjs="cdn")
        print(f"Plot saved to: {output_path.resolve()}")
    
    def plot_price_and_signal(self, strategy_name):
        results = self.results_dict[strategy_name]
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(
            go.Scatter(
                x= results.index,
                y= results["price"],
                mode="lines",
                name="Price"
            ),
            secondary_y=False
        )

        fig.add_trace(
            go.Scatter(
                x= results.index,
                y= results["signal"],
                mode="lines",
                name="Signal"
            ),
            secondary_y=True
        )

        fig.update_layout(
            title=f"Price and Signal - {strategy_name}",
            xaxis_title="Date"
        )

        fig.update_yaxes(title_text="Price", secondary_y=False)
        fig.update_yaxes(title_text="Signal", secondary_y=True)

        self.output_dir.mkdir(parents=True, exist_ok=True)
        output_path = self.output_dir / f"price_signal_{strategy_name.lower().replace(' ', '_')}.html"
        fig.write_html(output_path, include_plotlyjs="cdn")
        print(f"Plot saved to: {output_path.resolve()}")