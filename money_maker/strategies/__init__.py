from money_maker.strategies.freelancing import FreelancingStrategy
from money_maker.strategies.microtasks import MicroTaskStrategy
from money_maker.strategies.content_creation import ContentCreationStrategy
from money_maker.strategies.agent_marketplaces import AgentMarketplaceStrategy
from money_maker.strategies.web_research import WebResearchStrategy
from money_maker.strategies.dynamic_agents import DynamicWebAgentsStrategy

STRATEGY_REGISTRY = {
    "freelancing": FreelancingStrategy,
    "microtasks": MicroTaskStrategy,
    "content_creation": ContentCreationStrategy,
    "agent_marketplaces": AgentMarketplaceStrategy,
    "web_research": WebResearchStrategy,
    "dynamic_agents": DynamicWebAgentsStrategy,
}
