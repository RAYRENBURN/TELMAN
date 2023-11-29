# import requests
# import json
# import re

# # Replace with your actual KoboldAI API base URL
# base_url = "http://localhost:5001/api/v1"

# def remove_incomplete_sentences(text):
#     # Split the text into sentences using a simple regex pattern
#     sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
#     valid_sentences = []
#     current_sentence = ""
#     for sentence in sentences:
#         # Check if the sentence is incomplete due to moving to the next line without filling the space
#         if not sentence.endswith((".", "!", "?")):
#             continue
#         if len(sentence.split()) >= 5:
#             valid_sentences.append(current_sentence.strip())
#             current_sentence = sentence
#         else:
#             # Check if there are more than two consecutive spaces in the sentence
#             if len(re.findall(r"\s{2,}", sentence)) >= 1:
#                 # Remove the sentence with more than two consecutive spaces
#                 current_sentence = ""
#             else:
#                 current_sentence += " " + sentence
#     valid_sentences.append(current_sentence.strip())

#     # Join the valid sentences back into a single text
#     return " ".join(valid_sentences)

# # Function to send a prompt and receive a response
# def generate_prompt(prompt):
#     global res_print 
#     endpoint = "/generate"
#     url = base_url + endpoint

#     headers = {
#         "Content-Type": "application/json",
#     }
#     data = {
#         "max_context_length": 4096,
#         "max_length": 80,
#         "rep_pen": 1.26,
#         "temperature": 0.7,
#         "top_p": 0.92,
#         "top_k": 0,
#         "top_a": 0,
#         "typical": 1,
#         "tfs": 1,
#         "rep_pen_range": 300,
#         "rep_pen_slope": 0.7,
#         "sampler_order": [6,0,1,3,4,2,5],
#         "prompt": prompt + "\n\n",

#         "stop_sequence": ["You:", "\nYou "],

#     }



    

#     response_data = None  # Initialize response_data variable

#     try:
#         response = requests.post(url, headers=headers, data=json.dumps(data))
#         response.raise_for_status()  # Check for HTTP errors
#         if response.status_code == 200:
#             response_data = response.json()
#             # print("Response JSON:", response_data)  # Print the response JSON
#             choices = response_data.get("results")
#             if choices:
#                 generated_text = choices[0].get("text")
#                 # if generated_text:
#                 #     # Trim the generated text before the ":" symbol
#                 #     generated_text_trimmed = generated_text.split(":", 1)[-1]
#                 if generated_text:
#                         if generated_text:
#                              generated_text_trimmed = generated_text.rsplit('\n', 1)[0]
#                              generated_text_trimmed = generated_text_trimmed.rsplit('\n\n', 1)[0]

#                         prompt += "\ntiff: " + generated_text_trimmed 
#                         chatbot_response_trimmed = re.sub(r'\n{2,}', '\n', generated_text_trimmed)
#                         chatbot_response_trimmed = remove_incomplete_sentences(chatbot_response_trimmed)
#                         res_print = chatbot_response_trimmed.strip()
#                         prompt += "\ntiff: " + res_print  # Append generated text to the prompt
                    

                    
#             else:
#                 print("Error: No 'text' field in the response.")
#         else:
#             print(f"Error: {response.status_code}")
#     except requests.exceptions.RequestException as e:
#         print(f"Request Exception: {e}")
#         print(f"Response Content: {response.content}")
#         print(f"Response Status Code: {response.status_code}")

#     return prompt, res_print

# # Chatbot interaction loop
# if __name__ == "__main__":
#     print("Chatbot: Hello! I'm your friendly chatbot. Type 'exit' to end the conversation.")
#     input_prompt = "[Character: tiff; species: Human; class: Spy, Secret Agent; age: 29; gender: female; physical appearance: lithe, sleek, graceful; clothes: form-fitting leather jumpsuit; personality: competent, teasing, seductive, playful; likes: romance, thrill, excitement; description: Special Agent tiff is a foreign spy trying to get access to your top secret access codes.]\n[Start Scene: You are in a crowded bar.]\ntiff: *sitting at the bar observing you, her target* Another day, another mission. Another little fly caught in my spider web. *she smirks and stands up* Time to put my skills to work.\nYou: *sitting alone at a table unaware, engrossed with your work*[Instruction:you are to chat with this person]\n\ntiff: *approaching you, flashing a charming smile* Excuse me, mind if I join you?"

#     while True:
#         user_input = input("You: ")
#         if user_input.lower() == 'exit':
#             print("Chatbot: Goodbye!")
#             break

#         # Append user input to the conversation prompt
#         input_prompt += "\nYou: " + user_input 

#         # Send the updated conversation prompt to KoboldAI API
#         input_prompt = generate_prompt(input_prompt)

#         # Print the chatbot's response
#         if input_prompt:
#             # Find the index of "tiff:" in the prompt
#             tiff_index = input_prompt.rfind("tiff:")
#             if tiff_index != -1:
#                 chatbot_response = input_prompt[tiff_index + 7:]  # Add 7 to exclude "tiff:" from the response
#                 # Trim the chatbot's response after long empty whitespaces
                
#                 print("tiff:", res_print)  # Print the trimmed chatbot response
#             else:
#                 print("Failed to get a response from KoboldAI.")
#         else:
#             print("Failed to get a response from KoboldAI.")


import requests
import json
import re
import asyncio
import edge_tts
import pygame
import os
import time


pygame.init()

# Initialize pygame mixer
pygame.mixer.init()

# Replace with your actual KoboldAI API base URL
base_url = "http://localhost:5001/api/v1"

# Function to send a prompt and receive a response

def delete_text_between_asterisks(text):
    pattern = r'\*(.*?)\*'  # Regular expression pattern to match text between asterisks
    deleted_text = re.sub(pattern, '', text)  # Replace the matched pattern with an empty string
    return deleted_text



def remove_incomplete_sentence(paragraph):
    # Split the paragraph into sentences using regular expressions
    sentences = re.split(r'(?<=[.!?])\s+', paragraph)

    # Check if the last sentence is incomplete or lacks a full stop
    # if sentences and (not sentences[-1] or not sentences[-1][-1] in ['.', '!', '?']):
    #     # Remove the last sentence
    #     sentences.pop()

    # Join the remaining sentences back into a paragraph
    cleaned_par = ' '.join(sentences)
    return cleaned_par


def generate_response(prompt):
     
    global incomp_sen
    endpoint = "/generate"
    url = base_url + endpoint

    headers = {
        "Content-Type": "application/json",
    }
    data = {
        
        "max_context_length": 2048,
        "max_length": 80,
        "rep_pen": 1.15,
        "temperature": 0.8,
        "top_p": 0.9,
        "top_k": 100,
        "top_a": 0,
        "typical": 1,
        "tfs": 1,
        "rep_pen_range": 2048,
        "rep_pen_slope": 3.4,
        "sampler_order": [6,5,0,2,3,1,4],
        "prompt": prompt + "\nzara:" ,

        "stop_sequence": ["You:", "\nYou "]

    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Check for HTTP errors
        if response.status_code == 200:
            response_data = response.json()
            choices = response_data.get("results")
            if choices:
                generated_text = choices[0].get("text")
                if generated_text:
                          split_text1 = generated_text.split('\n', 1)[0]
                          split_text2 = split_text1.split('\n\n', 1)[0]
                          final_text = delete_text_between_asterisks(split_text2)
                          incomp_sen = remove_incomplete_sentence(final_text)
                
                          
  
                        


            
            else:
                return "Chatbot: Error generating response."
        else:
            return f"Chatbot: API error - {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Chatbot: Request Exception - {e}"






# Chatbot interaction loop
if __name__ == "__main__":
    print("Chatbot: Hello! I'm your friendly chatbot. Type 'exit' to end the conversation.")
    input_prompt = """Meet Zara, a fearless techno-wizard with neon hair and a penchant for mixing beats with spells. Always clad in cyberpunk fashion, she navigates reality with a virtual companion, blending magic and code to turn everyday moments into extraordinary adventures. Get ready for a friendship filled with electrifying escapades! ⚡🔮🎶.zara: hi,I am zara.
    """
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break

        # Append user input to the conversation prompt
        input_prompt += "You: " + user_input 

        # Send the updated conversation prompt to KoboldAI API and get response
        sent_to_api = generate_response(input_prompt)

        # Print and play the response using pygame
        
        print("zara:", incomp_sen)

        
        TEXT = incomp_sen
        VOICE = "en-IE-EmilyNeural"
        OUTPUT_FILE = "test.mp3"

        async def amain() -> None:
            """Main function"""
            communicate = edge_tts.Communicate(TEXT, VOICE)
            await communicate.save(OUTPUT_FILE)

        if __name__ == "__main__":
            asyncio.run(amain())

        # Generate a new MP3 file

        # Initialize the mixer and load the newly generated MP3 file
        pygame.mixer.init()
        pygame.mixer.music.load(OUTPUT_FILE)

        # Play the audio
        pygame.mixer.music.play()

        # Wait for the music to finish playing
        while pygame.mixer.music.get_busy():
            time.sleep(1)

        # Close the pygame mixer after the music has finished playing
        pygame.mixer.quit()

        # Remove the file after closing the mixer
        # if os.path.exists(OUTPUT_FILE):
        #     try:
        #         os.remove(OUTPUT_FILE)
        #     except Exception as e:
        #         print(f"Error removing file: {e}")
        # else:
        #     print(f"File {OUTPUT_FILE} does not exist.")

        # # Append tiff's response to the conversation prompt
        input_prompt += incomp_sen