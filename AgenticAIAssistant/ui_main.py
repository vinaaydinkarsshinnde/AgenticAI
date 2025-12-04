import streamlit as st
from AgentExecutor import agent_executor
st.set_page_config(page_title='Agentic AI Assistant', page_icon='🤖')
st.title('🤖 Agentic AI Assistant (Mistral + ReAct)')
q = st.text_input('Ask me anything:')
if q:
    with st.spinner('Thinking...'):
        try:
            resp = agent_executor.invoke({'input': q})
            out = resp.get('output') if isinstance(resp, dict) else resp
            st.markdown(out)
        except Exception as e:
            st.error(f'Error: {e}')
