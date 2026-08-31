import json
from datetime import datetime
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from src.app.adapters.mcp.models.models import ToolCallResponse
from src.app.config import get_settings
from src.app.tools.definitions.tool_definitions import GENERATE_BAR_CHART_TOOL
from src.app.tools.tool_handler import Handler

from .models import BarChartInput

class GenerateBarChartService(Handler):

    async def execute(self, arguments: dict) -> ToolCallResponse:
        log = f"[Log: Calling tool with name '{GENERATE_BAR_CHART_TOOL.name}']"

        chart_info: BarChartInput = BarChartInput.model_validate(arguments)

        df = pd.DataFrame([
            {
                "month": data_point.month,
                "value": data_point.value
            }
            for data_point in chart_info.data
        ])

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(df["month"], df["value"], color="#87CEEB")

        ax.set_title(chart_info.title, fontsize=14, weight="bold")
        ax.set_xlabel(chart_info.x_axis_label, fontsize=12)
        ax.set_ylabel (chart_info.y_axis_label, fontsize=12)
        ax.grid(axis="x", linestyle="--", alpha=0.6)
        ax.invert_yaxis()

        plt.tight_layout()

        chart_file_path = self.build_chart_file_path(chart_title=chart_info.title)
        fig.savefig(chart_file_path, format="png", dpi=300, bbox_inches="tight")

        plt.close(fig)

        result = self.generate_result_report(chart_info=chart_info, chart_file_path=chart_file_path)

        return ToolCallResponse(content = json.dumps(result), log = log)

    def build_chart_file_path(self, chart_title: str) -> Path:
        charts_output_dir = Path(get_settings().charts_output_dir)

        now = datetime.now()
        date_time_suffix = now.strftime("%Y-%m-%d_%H-%M-%S")

        file_name = f"{chart_title.replace(' ', '-').lower()}_{date_time_suffix}.png"

        return charts_output_dir / file_name

    def generate_result_report(
            self, 
            chart_info: BarChartInput, 
            chart_file_path: Path
    ) -> dict:
        if not chart_file_path.exists():
            return {
                "valid": "false",
                "title": chart_info.title,
                "x-axis-lable": chart_info.x_axis_label,
                "y-axis-label": chart_info.y_axis_label,
                "error": "Chart has not been created successfuly."
            }
        
        return {
            "valid": "true",
            "title": chart_info.title,
            "x-axis-lable": chart_info.x_axis_label,
            "y-axis-label": chart_info.y_axis_label,
            "chart_file_name": chart_file_path.name
        } 
        