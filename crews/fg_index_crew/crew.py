from crewai import Crew
from langchain_openai import ChatOpenAI

from crews.fg_index_crew.agents import Agents
from crews.fg_index_crew.tasks import Tasks


class FGIndexCrew:
    def __init__(self):
        self.gpt_4o = ChatOpenAI(model="gpt-4o", temperature=0.5)
        self.agent = Agents()
        self.tasks = Tasks()

    def crew(self) -> Crew:
        """Creates the FGIndexCrew crew"""

        fg_analyst = self.agent.fg_analyst()
        fg_analysis = self.tasks.fg_analysis(agent=fg_analyst)

        return Crew(
            agents=[fg_analyst],
            tasks=[fg_analysis],
            verbose=True,
        )
