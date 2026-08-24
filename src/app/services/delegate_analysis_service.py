from src.app.adapters.mcp.models.models import ToolCallResponse
from src.app.agents.analysis_agent import AnalysisAgent
from src.app.tools.tool_handler import Handler

class DelegateAnalysisService(Handler):

    def __init__(self, analysis_agent: AnalysisAgent):
        self._agent = analysis_agent

    async def execute(self, arguments: dict) -> ToolCallResponse:
        # TODO implement
        pass