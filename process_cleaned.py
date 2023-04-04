from serpapi import GoogleSearch
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain import SerpAPIWrapper
from langchain.llms import OpenAI
from langchain.memory import ConversationEntityMemory, SimpleMemory
import os
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
llm = OpenAI(temperature=0)
api_key = os.environ['SERPAPI_API_KEY'] = "40f6fba6120a66c379436fe451a4117f8ffea1edffbb935fef773be799b9bac4"

# this file will include the chain, not the text cleaning functions. text cleaning will be useful when you figure out how to use entire text files as memory

#gets question from user input, writes to simple memory
def get_question_from_user():
    question = input("Enter your question: ")
    simple_memory = SimpleMemory()
    simple_memory.memories = {"question":question}

#trying a class, but likely need to initialize an instance of this class the first time you use it 
class SimpleMemoryClass():
    def __init__(self):
        self.memory = SimpleMemory()
    def get_user_input(self):
        question = input("Enter your question: ")
        self.memory.memories = {"question":question}
        return question # TODO: won't return stored
    def return_memories(self):
        memory = self.memory
        return memory.memories
    
#question = "What's the molecular basis of Rett syndrome?"
# defines question to query chain, returns the chain output
def q2query_chain(question):
    memory = ConversationEntityMemory(llm=llm)
    q2q_prompt_template = """ 
    Turn the following question into a search query: {question}
    """
    # def question -> query chain
    q2q_prompt = PromptTemplate(
        input_variables = ["question"],
        template = q2q_prompt_template,
    )
    question_to_query_chain = LLMChain(
        llm=llm,
        prompt=q2q_prompt,
        output_key="query",
        memory=memory
    )
    output = question_to_query_chain({"question":question})
    return output.get('query')

def search_tool(query):
    params = {
        "q":query,
        "engine":'google',
        "gl":'us'
    }
    serpapi = SerpAPIWrapper(serpapi_api_key = api_key)
    result = serpapi.run(query)
    print(result)
    return result

def get_answer_from_results(question,result):
    llm = OpenAI(temperature=0)
    parse_result_template = """ 
    Parse the following result: {result} to get the answer to the question: {question}
    """
    parse_result_prompt = PromptTemplate(
        input_variables=["result", "question"],
        template=parse_result_template
    )
    parse_result_chain = LLMChain(
        llm=llm,
        prompt=parse_result_prompt,
        output_key="answer",
    )
    ans = parse_result_chain({"result":result,"question":question})
    return ans

#write anything to the memory of your choice
def write_to_memory(memoryId, content):
    memory = memoryId
    try:
        input = {"input":content}
        memory.load_memory_variables(input)
        return "success"
    except content is None: 
        print("Error: couldn't store memory, content is None")
        return "error"
    
#trying entity memory class instead, so all reading/writing is to the same place
class EntityMemory():
    def __init__(self):
        self.memory = ConversationEntityMemory(llm=llm)
    def write_to_memory(self,content):
        memory = self.memory
        input = {"input":content}
        #TODO: this may not be the same as memory.store; memory_variables loads the variables but not necessarily the context?
        memory.load_memory_variables(input)
        return "success"
    def read_memory(self):
        memory = self.memory
        #this returns an empty dict, so load_memory)variables probbaly don't work
        return memory.store
        
#return full entity memory
def read_memory(memoryId):
    return memoryId.memory_variables
    
#answers questions from memory
def ans_from_memory(memoryId,question):
    memory = memoryId
    ans_mem_q_template = """ 
    Memory: {memory}
    Using your memory, answer this question: {question}
    """
    ans_mem_q_prompt = PromptTemplate(
        input_variables=["question", "memory"],
        template=ans_mem_q_template,
    )
    ans_mem_q_chain = LLMChain(
        llm=llm,
        prompt=ans_mem_q_prompt,
        output_key="answer",
    )
    return ans_mem_q_chain({"question":question,"memory":memory})


# gets 5 new questions using memory stores on a given entity, parses into list
def new_qs_from_memory(entity,memoryId):
    memory = memoryId

    check_memory_template = """ 
    Given what you know about {entity}, generate 5 new questions to learn more about it. Use your {memory} stores to help you

    """
    check_memory_prompt = PromptTemplate(
        input_variables=["entity", "memory"],
        template=check_memory_template,
    )
    check_memory_chain = LLMChain(
        llm=llm,
        prompt=check_memory_prompt,
        output_key="questions",
    )
    output = check_memory_chain({"entity":entity,"memory":memory})
    q_list = []
    questions = output.get('questions')
    for q in questions.split('\n'):
        q_list.append(q)
    q_list.remove('')

    return q_list

def full_loop(question,entity,memoryId):
    query = q2query_chain(question)
    result = search_tool(query)
    memory = ConversationEntityMemory(llm=llm)

    # now write results to entity memory
    memoryId.write_to_memory(content=result)
    # read memory -> 5 new questions
    #
    questions = new_qs_from_memory(entity = entity, memoryId = memoryId)
    return questions
    
memoryId = EntityMemory()
init = SimpleMemoryClass()
init.get_user_input()
question = init.return_memories().get('question')
print("full loop: ", full_loop(question,memoryId, "Rett syndrome"))
print("memoryId: ", memoryId.read_memory())

