from langchain import LLMChain, PromptTemplate, OpenAI
import os
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
llm = OpenAI(temperature=0)

# generate hypotheses from sota
def get_treatment_questions(memory):
    treatment_q_template = """ 
    {memory}
    Using your memory as an aid, generate 5 hypotheses of ways to find treatments for Rett syndrome through drug repurposing. For example, a hypothesis might be: "Look for drugs that target genes that are one hop away from the Rett syndrome gene, i.e. regulate the Rett syndrome gene"
    """

    treatment_q_prompt = PromptTemplate(
        input_variables=["memory"],
        template=treatment_q_template,
    )

    treatment_q_chain = LLMChain(
        llm=llm,
        prompt=treatment_q_prompt,
        output_key="hypotheses",
    )
    output = treatment_q_chain({"memory": memory})
    return output
