from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain.tools import Tool
from tools.finance_data_tool import get_financial_data
from tools.finance_chart_tool import get_stock_chart_markdown
from tools.calculator import calculate

from langchain_ollama import OllamaLLM
llm = OllamaLLM(model="mistral", temperature=0.2)

finance_tool = Tool(
    name='FinanceDataTool',
    func=get_financial_data,
    description='Get price, market cap, P/E, volume for Indian stocks. Input: plain name or ticker.'
)

chart_tool = Tool(
    name='StockChart',
    func=get_stock_chart_markdown,
    description='Return a markdown image (base64) with a 30-day close price chart. Input: company name or ticker.'
)

calculator_tool = Tool(
    name='Calculator',
    func=calculate,
    description='Evaluate math expressions. Use only for math.'
)

TOOLS = [finance_tool, chart_tool, calculator_tool]

prompt_text = """
You are an intelligent financial assistant using the ReAct pattern.
You have access to these tools:
{tools}

Available tool names:
{tool_names}

Always think step by step. Follow this exact format for your reasoning and actions:

Thought: Describe your reasoning here.
Action: The tool name exactly as listed in {tool_names}
Action Input: The input string for the tool (just the stock name or expression).

When you have the final answer, respond with:

Final Answer: <your response here>

Examples:

Question: What is the share price of TCS?
Thought: The user wants the current share price. I will use the FinanceDataTool.
Action: FinanceDataTool
Action Input: TCS

Question: What is 2+2?
Thought: This is a math calculation. I will use the Calculator.
Action: Calculator
Action Input: 2+2

Begin!

Question: {input}
{agent_scratchpad}
"""


# Create prompt properly
prompt = PromptTemplate(
    input_variables=["tools", "tool_names", "input", "agent_scratchpad"],
    template=prompt_text
)

agent = create_react_agent(
    llm=llm,
    tools=TOOLS,
    prompt=prompt
)
agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=TOOLS, handle_parsing_errors=True, verbose=True)
