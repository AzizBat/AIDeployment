import os

import json  



from langchain.llms import CTransformers

from langchain.callbacks.base import BaseCallbackHandler



# Handler that prints each new token as it is computed

class NewTokenHandler(BaseCallbackHandler):

    def on_llm_new_token(self, token: str, **kwargs) -> None:

        print(f"{token}", end="", flush=True)



# Initialize the Llama model outside the run function

model_path = os.path.join(os.getenv("AZUREML_MODEL_DIR"), "filex.bin")

llm = CTransformers(

    model=model_path,  # Location of downloaded GGML model

    model_type="llama",  # Model type Llama

    stream=True,

    callbacks=[NewTokenHandler()],

    config={'max_new_tokens': 256, 'temperature': 0.3}

)



def init():

    # This function is called when the container is started

    pass



def run(input_data):

    # This function is called for each batch of input data

    try:

        # Assume your input data is in JSON format

        input_data = json.loads(input_data)



        # Extract the prompt from input data

        prompt = input_data.get("prompt", "")



        # Generate text using the llm

        output = llm(prompt)



        # Format the output

        output_data = {"generated_text": output}



        return json.dumps(output_data)

    except Exception as e:

        error = str(e)

        return json.dumps({"error": error})