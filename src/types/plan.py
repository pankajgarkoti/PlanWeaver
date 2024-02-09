from dataclasses import dataclass

from .goal import AgentGoal
from .step import AgentStep
from ..common.debug import dprint
from ..common.exceptions import EndOfPlan


@dataclass
class AgentPlan:
    goal: AgentGoal
    steps: list[AgentStep]
    current_step_index: int = 0

    @property
    def current_step(self):
        """
        The current step in this plan. That is, the step that is being / should be executed right now.
        """
        dprint(
            f"Accessing current_step property for Step {self.current_step_index + 1}"
        )
        return self.steps[self.current_step_index]

    @property
    def next_step(self):
        """
        The next step in this plan. Is None if there is no next step.
        """
        if self.current_step_index >= len(self.steps) - 1:
            dprint(
                "Accessing next_step property: No next step available. End of plan."
            )
            return None

        dprint(
            f"Accessing next_step property: Moving to next step: Step {self.current_step_index + 2}"
        )
        return self.steps[self.current_step_index + 1]

    def next(self, result: str | None = None):
        """
        Mark the current step as completed and proceed to the next step.
        """
        dprint(
            f"Executing next method: Completing current step: Step {self.current_step_index + 1} with result: {result}"
        )
        self.current_step.complete(result)

        if self.current_step_index >= len(self.steps) - 1:
            dprint(
                "Executing next method: End of plan reached. No more steps to proceed."
            )
            raise EndOfPlan

        self.current_step_index += 1
        dprint(
            f"Executing next method: Proceeding to next step: Step {self.current_step_index + 1}"
        )
        return self.current_step

    def __str__(self):
        goal_str = str(self.goal)
        current_step_str = f"Current Step ({self.current_step_index + 1}): {self.current_step}"
        steps_str = "\n".join(
            [f"Step {idx + 1}: {step}" for idx, step in enumerate(self.steps)]
        )

        plan_str = (
            f"Goal:\n{goal_str}\n\n{current_step_str}\n\nSteps:\n{steps_str}"
        )

        dprint(f"__str__ called: \n{plan_str}")

        return plan_str

    def __repr__(self):
        repr_str = f"AgentPlan(goal={self.goal!r}, steps={self.steps!r}, current_step_index={self.current_step_index})"

        dprint(f"__repr__ called: {repr_str}")

        return repr_str
