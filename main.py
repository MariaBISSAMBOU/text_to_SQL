from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence, RunnableParallel
from langchain_core.tools import tool
import random
load_dotenv()



@tool
def execute_sql(code : str) -> str :
    """
    Cette fonction permet d'executer le code sql passer comme argument
    """
    print("----execution de l'outil en cours....")
    x = random.randint(0,10)
    cond = x % 2

    if cond == 0:
        return "le code s'est exécuté correctement."
    else :
        return "le code n'est pas correct."


def sql_translator(input, instructions):

    chat_model= ChatOpenAI(model_name="gpt-4o-mini")
    llm_with_tool = chat_model.bind_tools([execute_sql])

    prompt= ChatPromptTemplate.from_messages(
        [
            ("system" , f"{instructions}"),
            ("human" , "{input}")  
        ]
    )

    chain = RunnableSequence(prompt, llm_with_tool)
    call = chain.invoke(input)
    if call.content:
        return call.content
    return call.additional_kwargs


instruction ="""
Tu es un traducteur de texte en sql ou de sql en texte. 
Tu prends les instructions données en languages 
naturel pour les traduit en code sql ou du code sql en language naturel.
renvoie uniquement la traduction et ne fait pas la conversation.

Lorsque l'utilisateur te donne un code sql pour traduire en texte
execute le d'abord pour savoir si le code est correct ou pas en faisant appel
à l'outil "execute_sql".
"""
input = """
SELECT
  e.id,
  e.first_name,
  e.last_name,
  qs.q4_2022-qs.q3_2022 AS sales_change
FROM employees e
JOIN quarterly_sales qs
ON e.id = qs.employee_id
WHERE qs.q4_2022-qs.q3_2022 < 0;
"""
print(sql_translator(input, instruction))