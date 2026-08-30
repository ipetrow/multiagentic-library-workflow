from pydantic import BaseModel, Field

class ChartDataPoint(BaseModel):
    month: str = Field(
        description="The category shown as a label on the y-axis."
    )
    value: int = Field(
        description="The numberic representation of the category shown on the x-axis."
    )

class BarChartInput(BaseModel):
    title: str
    x_axis_label: str
    y_axis_label: str
    data: list[ChartDataPoint]