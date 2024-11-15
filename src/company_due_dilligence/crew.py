from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
# from company_due_dilligence.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
from crewai_tools import SerperDevTool, WebsiteSearchTool, ScrapeWebsiteTool

@CrewBase
class CompanyDueDilligenceCrew():
	"""CompanyDueDilligence crew"""

	@agent
	def lead_researcher_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['lead_researcher_agent'],
			tools=[SerperDevTool(), WebsiteSearchTool(), ScrapeWebsiteTool()],
			verbose=True
		)

	@agent
	def lead_sentiment_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['lead_sentiment_agent'],
			tools=[SerperDevTool(), WebsiteSearchTool(), ScrapeWebsiteTool()],
			verbose=True
		)
	
	@agent
	def personal_relations_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['personal_relations_agent'],
			tools=[SerperDevTool(), WebsiteSearchTool(), ScrapeWebsiteTool()],
			verbose=True
		)
	
	@agent
	def product_specialist_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['product_specialist_agent'],
			tools=[SerperDevTool(), WebsiteSearchTool(), ScrapeWebsiteTool()],
			verbose=True
		)

	@agent
	def document_coordinator_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['document_coordinator_agent'],
			allow_delegation=True,
			verbose=True,
			max_iter=5
		)
	
	# @agent
	# def quality_assurance_agent(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['quality_assurance_agent'],
	# 		tools=[SerperDevTool(), WebsiteSearchTool(), ScrapeWebsiteTool()],
	# 		verbose=True,
	# 		allow_delegation=True
	# 	)

	@task
	def lead_researcher_task(self) -> Task:
		return Task(
			config=self.tasks_config['lead_researcher_task'],
			agent=self.lead_researcher_agent()
		)

	@task
	def lead_sentiment_task(self) -> Task:
		return Task(
			config=self.tasks_config['lead_sentiment_task'],
			agent=self.lead_sentiment_agent()
		)
	
	@task
	def personal_relations_task(self) -> Task:
		return Task(
			config=self.tasks_config['personal_relations_task'],
			agent=self.personal_relations_agent()
		)

	@task
	def product_specialist_task(self) -> Task:
		return Task(
			config=self.tasks_config['product_specialist_task'],
			agent=self.product_specialist_agent()
		)
	
	@task
	def document_coordinator_task(self) -> Task:
		return Task(
			config=self.tasks_config['document_coordinator_task'],
			agent=self.document_coordinator_agent(),
			output_file="report.md"
		)
	
	
	
	# @task
	# def quality_assurance_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['quality_assurance_task'],
	# 		agent=self.quality_assurance_agent(),
	# 		output_file="report.md"
	# 	)

	@crew
	def crew(self) -> Crew:
		"""Creates the CompanyDueDilligence crew"""
		return Crew(
			agents=[self.lead_researcher_agent(), 
		   		self.lead_sentiment_agent(),
				self.personal_relations_agent(),
				self.product_specialist_agent(),
			], # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.hierarchical,
			manager_agent=self.document_coordinator_agent(),
			verbose=True
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)