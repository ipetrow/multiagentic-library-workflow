class AgentError(Exception):
    """Base exception for all agent-related errors."""

class AgentExecutionError(AgentError):
    """The agent failed during execution."""

class MaxStepsExceededError(AgentExecutionError):
    """The agent exceeded the configured maximum number of steps."""

