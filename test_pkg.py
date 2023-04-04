from testopentargets import *
from process_cleaned import *

from langchain.memory import ConversationEntityMemory
memory = ConversationEntityMemory(llm=llm)

input = {"input": "Rett syndrome is caused by mutations in the gene MECP2, which encodes methyl CpG binding protein 2 (MECP2)"}
# memory.store doesn't save to memory
memory.store

from pprint import pprint
pprint(memory.store)

#package imports work, but code won't run -> maybe can't have two files open at once

memoryId = ConversationEntityMemory(llm=llm)
init = SimpleMemoryClass()
init.get_user_input()

