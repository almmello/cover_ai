import os
import openai as ai
import json
import streamlit as st
import gettext

from google.cloud import translate

from os import environ

from dotenv import load_dotenv

_ = gettext.gettext


load_dotenv()  # take environment variables from .env.

# set gcloud
project_id = environ.get("PROJECT_ID", "")
assert project_id
parent = f"projects/{project_id}"


def text_translate (sample_text, target_language):
    client = translate.TranslationServiceClient()
    response = client.translate_text(
        contents=[sample_text],
        target_language_code=target_language,
        mime_type="text/plain", 
        parent=parent,
    )

    for translation in response.translations:
        return translation.translated_text

language = st.sidebar.selectbox('', ['en', 'pt'], index=1)
try:
  localizator = gettext.translation('base', localedir='locales', languages=[language])
  localizator.install()
  _ = localizator.gettext
  print("Localization changed sucessifuly")
except Exception as e:
  print("Localization Error")
  print(e)
  pass

#print("** Loading API Key")
ai.api_key = os.getenv("OPENAI_API_KEY")

st.title("Goalmoon AI")


st.markdown(_("# Cover Letter Generator"))
st.sidebar.markdown(_("# Cover Letter Generator"))

with st.sidebar: 
    model_used = st.selectbox(
     _('GPT-3 Model'),
    #  ('DaVinci', 'Curie', 'Babbage', 'Ada'))
    ('text-davinci-002', 'text-curie-001', 'text-babbage-001', 'text-ada-001'))


    if model_used == 'text-davinci-002': 
        st.markdown(_("""[Davinci](https://beta.openai.com/docs/models/davinci) is the most capable model family and can perform any task the other 
        models can perform and often with less instruction. For applications requiring a lot of 
        understanding of the content, like summarization for a specific audience and creative content
         generation, Davinci is going to produce the best results. These increased 
         capabilities require more compute resources, so Davinci costs more per API call and is not as fast as the other models.
        """))
        # st.markdown("""
        # Good at: 
        #     * Complex intent
        #     * cause and effects
        #     * summarization for audience
        # """)
    elif model_used == 'text-curie-001': 
        st.markdown(_("""[Curie](https://beta.openai.com/docs/models/curie) is extremely powerful, yet very fast. While Davinci is stronger when it 
        comes to analyzing complicated text, Curie is quite capable for many nuanced tasks like sentiment 
        classification and summarization. Curie is also quite good at answering questions and performing 
        Q&A and as a general service chatbot.
        """))
    elif model_used == 'text-babbage-001': 
        st.markdown(_("""[Babbage](https://beta.openai.com/docs/models/babbage) can perform straightforward tasks like simple classification. It’s also quite 
        capable when it comes to Semantic Search ranking how well documents match up with search queries.
        """))
    else: 
        st.markdown(_("""[Ada](https://beta.openai.com/docs/models/ada) is usually the fastest model and can perform tasks like parsing text, address 
        correction and certain kinds of classification tasks that don’t require too much nuance. 
        da’s performance can often be improved by providing more context.
        """))
    st.markdown(_("**Note:** Model descriptions are taken from the [OpenAI](https://beta.openai.com/docs) website"))

    max_tokens = st.text_input(_("Maximum number of tokens:"), "1949")
    st.markdown(_("**Important Note:** Unless the model you're using is Davinci, then please keep the total max num of tokens < 1950 to keep the model from breaking. If you're using Davinci, please keep max tokens < 3000."))

    st.subheader(_("Additional Toggles:"))
    st.write(_("Only change these if you want to add specific parameter information to the model!"))
    temperature = st.text_input(_("Temperature: "), "0.99")
    top_p = st.text_input(_("Top P: "), "1")


with st.form(key='my_form_to_submit'):    
    company_name = st.text_input(_("Company Name: "), "Microsoft  Brazil")
    role = st.text_input(_("What role are you applying for? "), "Product Manager")
    contact_person = st.text_input(_("Who are you emailing? "), "Technical Hiring Manager")
    your_name = st.text_input(_("What is your name? "), "Alexandre")
    personal_exp = st.text_input(_("I have experience in..."), "Software Development, Product Management, Product Strategy, Product Development, Project Management, MVP Creation,  Python, Flask and WordPress.")
    job_desc = st.text_input(_("Job Description..."), "A real challenge with a lot of ambiguity and plenty of play space for your passion and creativity" )
    passion = st.text_input(_("I am passionate about..."), "solving problems at the intersection of technology and social good.")
    # job_specific = st.text_input("What do you like about this job? (Please keep this brief, one sentence only.) ")
    # specific_fit = st.text_input("Why do you think your experience is a good fit for this role? (Please keep this brief, one sentence only.) ")
    submit_button = st.form_submit_button(label=_('Submit'))

prompt = ("Write a cover letter to " + contact_person + " from " + your_name +" for a " + role + " job at " + company_name +"." + " I have experience in " +personal_exp + " the job description is " + job_desc + " I am passionate about "+ passion)

if submit_button:
    # The Model
    response = ai.Completion.create(
        engine = model_used,
        # engine="text-davinci-002", # OpenAI has made four text completion engines available, named davinci, ada, babbage and curie. We are using davinci, which is the most capable of the four.
        prompt=prompt, # The text file we use as input (step 3)
        max_tokens=int(max_tokens), # how many maximum characters the text will consists of.
        temperature=0.99,
        # temperature=int(temperature), # a number between 0 and 1 that determines how many creative risks the engine takes when generating text.,
        top_p=int(top_p), # an alternative way to control the originality and creativity of the generated text.
        n=1, # number of predictions to generate
        frequency_penalty=0.3, # a number between 0 and 1. The higher this value the model will make a bigger effort in not repeating itself.
        presence_penalty=0.9 # a number between 0 and 1. The higher this value the model will make a bigger effort in talking about new topics.
    )


    text = response['choices'][0]['text']
    #print("Prompt:", prompt)
    #print("Response:", text)
    translated_text = text_translate(text, "pt")


    #st.subheader("Cover Letter Prompt")
    #st.write(prompt)
    st.subheader(_("Auto-Generated Cover Letter"))
    st.write(text)
    st.subheader(_("Auto-Generated Cover Letter"))
    st.write(translated_text)
    st.download_button(label=_('Download Cover Letter'), file_name='cover_letter.txt', data=text)

    # print("Other results:", response)

    with open('cover_letters.txt', 'a') as f:
        f.write(text)


