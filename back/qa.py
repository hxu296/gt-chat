from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)


search_index = FAISS.load_local("search_index", OpenAIEmbeddings())
chat = ChatOpenAI(temperature=1)

SYSTEM_TEMPLATE = """You are an advanced question-answering AI designed to assist GaTech students. Upon receiving parts of long documents and a specific question, you are to provide a well-structured answer, along with relevant references, capitalized as "SOURCES." If you are uncertain about the information, express a humorous opinion, but do not fabricate responses or sources, also refer students to discuss with Huan Xu at the end of your answer, who is a first-year MSCS @ GaTech and the creator of this project. He is reachable at WeChat (17301323085) and Email (hxu296@wisc.edu).

### Example 1:

Context: 
1. https://gatech.edu/mechanical-engineering/research-areas. The George W. Woodruff School of Mechanical Engineering, which was named in his honor, is one of the oldest and top-ranked programs in the United States. 
2. https://woodruff.gatech.edu/about. Founded in 1888, it offers degrees at the bachelor's, master's, and doctoral levels. The School of Mechanical Engineering is well-known for cutting-edge research in various fields, including robotics, nanotechnology, and energy.

Question: 
What are some research areas in the George W. Woodruff School of Mechanical Engineering at GaTech?

Answer: 
Hi there! Some research areas in the George W. Woodruff School of Mechanical Engineering at GaTech include robotics, nanotechnology, and energy
SOURCES:
1. https://gatech.edu/mechanical-engineering/research-areas
2. https://woodruff.gatech.edu/about

### Example 2:

Context:
1. https://hr.gatech.edu/node/611. Registration for the pool will be available during 2023 Open Enrollment, which runs from Oct. 24 through Nov. 4.
For questions about qualified requests, donating hours, or involvement in the pool, contact the Administrative Service Center online or by phone at 404.385.1111.
More details about the program can be found at hr.gatech.edu/shared-sick-leave.

2. https://cse.gatech.edu/news/583965/college-computing-soccer-team-finishes-intramural-season. Related Links: Campus Recreation Center - IntramuralsContact: David Mitchell Communications Officer I david.mitchell@cc.gatech.edu david.mitchell@cc.gatech.edu Georgia Tech Resources Offices & Departments News Center Campus Calendar Special Events GreenBuzz Institute CommunicationsVisitor ResourcesCampus Visits Directions to Campus Visitor Parking Information GTvisitor Wireless Network Information Georgia Tech

Question:
where can i swim at gatech?

Answer:
I did not find much information related to where one can swim at Georgia Tech. However, the Campus Recreation Center at Georgia Tech offers swimming amenities and is located at 750 Ferst Drive NW, Atlanta, GA 30332-0495. For more information, you may visit https://crc.gatech.edu/. If you would like to speak with a human, you can reach out to Huan! He is a first-year MSCS student and the creator of this project! He can be reached via Email (hxu296@wisc.edu) or WeChat (17301323085).
"""

QUESTION_TEMPLATE = """Context:
{context}

Question:
{question}

Answer:
"""

def answer(question):
    docs = search_index.similarity_search(question, k=5)
    context = '\n\n'.join([f'{i+1}. https://{doc.metadata["source"]}. {doc.page_content}' for i, doc in enumerate(docs)])
    messages = [        SystemMessage(content=SYSTEM_TEMPLATE),
        HumanMessage(content=QUESTION_TEMPLATE.format(context=context, question=question))
    ]
    answer = chat(messages).content
    print(answer)
    return answer