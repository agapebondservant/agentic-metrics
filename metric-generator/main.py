from crewai import Agent, Task, Crew, LLM
from opentelemetry import trace
from random import randint, random
from openlit import start_trace, init as openlit_init
from openinference.instrumentation.crewai import CrewAIInstrumentor
from time import time, sleep
from uuid import uuid4
from datetime import datetime
from os import getenv


class Metric:
    def __init__(self, issue_id: int, message: str):
        date_format = "%Y-%m-%d %H:%M:%S"
        now = datetime.now()
        sleep(randint(1, 3))
        later = datetime.now()
        self.uuid = str(uuid4())
        self.issue_id = issue_id
        self.created_at = now.strftime(date_format)
        self.issue_created_at = self.created_at
        self.merge_requested_at = later.strftime(date_format)
        self.lines_of_code_count = randint(1, 10000)
        self.test_coverage_pre_migration = random()
        self.test_coverage_post_migration = random()
        self.unit_test_failure_count = randint(0, 10)
        self.unit_test_total_count = self.unit_test_failure_count + randint(1, 10)
        cve1 = randint(0, 100)
        cve2 = randint(0, 100)
        if cve2 < cve1:
            self.cve_count_pre_migration = cve1
            self.cve_count_post_migration = cve2
        else:
            self.cve_count_pre_migration = cve2
            self.cve_count_post_migration = cve1
        failure_count1 = randint(0, 10)
        failure_count2 = randint(0, 10)
        if failure_count2 < failure_count1:
            self.behavior_test_pre_migration_failure_count = failure_count1
            self.behavior_test_post_migration_failure_count = failure_count2
        else:
            self.behavior_test_pre_migration_failure_count = failure_count2
            self.behavior_test_post_migration_failure_count = failure_count1
        self.behavior_test_pre_migration_total_count = (
            self.behavior_test_pre_migration_failure_count + randint(1, 10)
        )
        self.behavior_test_post_migration_total_count = (
            self.behavior_test_post_migration_failure_count + randint(1, 10)
        )
        self.message = message


def log(metric_event_name: str, issue_id: int, message: str) -> None:
    # gets current span
    span = trace.get_current_span()

    if span.is_recording():
        # create and log metric
        metric = Metric(issue_id, message)
        span.add_event(metric_event_name, metric.__dict__)

        # add searchable tag
        span.set_attribute("custom.layer", "agent_metrics")
    else:
        print(f"No active trace found. Message: {message}")


def main() -> None:
    # global vars
    issue_id = 1
    metric_collection_name = "Agentic Metrics"
    metric_event_name = "Agentic Metric"
    llm_api_key = getenv("LLM_API_KEY")
    llm_base_url = getenv("LLM_BASE_URL")
    llm_model_name = getenv("LLM_MODEL_NAME")

    openlit_init(capture_message_content=True)
    CrewAIInstrumentor().instrument(skip_dep_check=True)

    with start_trace(metric_collection_name) as trace:
        # set high level trace metadata
        trace.set_metadata(
            {
                "custom_message_type": "metric",
            }
        )
        log(metric_event_name, issue_id, "hi 1")

        llm = LLM(
            model=llm_model_name,
            api_key=llm_api_key,
            base_url=llm_base_url,
        )
        log(metric_event_name, issue_id, "hi 2")

        greeter = Agent(
            role="Greeter",
            goal="Greet the world in a friendly and enthusiastic way",
            backstory="You are a friendly agent whose sole purpose is to greet people.",
            llm=llm,
            verbose=True,
        )
        log(metric_event_name, issue_id, "hi 3")

        greet_task = Task(
            description="Say hello to the world. Be enthusiastic and friendly.",
            expected_output="A short, enthusiastic greeting to the world.",
            agent=greeter,
        )
        log(metric_event_name, issue_id, "hi 4")

        crew = Crew(
            agents=[greeter],
            tasks=[greet_task],
            verbose=True,
        )
        log(metric_event_name, issue_id, "hi 5")

        log(metric_event_name, issue_id, "hi 6")

        result = crew.kickoff()
        log(metric_event_name, issue_id, "hi 7")
        print(result)


if __name__ == "__main__":
    main()
