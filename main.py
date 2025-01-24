import streamlit as st
import openai
import PyPDF2

def add_space(n=1):
  for _ in range(n):
    st.sidebar.text(" ")

    # Recognizes if the file is pdf or txt
def get_text_from_file(uploaded_file):
  if uploaded_file.type == "application/pdf":
    return pdf_to_text(uploaded_file)
  else:
    return uploaded_file.read().decode()
  


# function is called when filetype is a pdf, converts the pdf into a txt
def pdf_to_text(pdf_file):
  pdf_reader = PyPDF2.PdfReader(pdf_file)
  # Initialize an empty string to store the text
  text = ''
  for page_num in range(len(pdf_reader.pages)):
    page = pdf_reader.pages[page_num]
    text += page.extract_text()

  return text



def main():
  """
  The main function that handles the Streamlit app logic.
  """


# Title

  st.sidebar.image("Gbot.jpg", use_container_width=True)
  st.sidebar.divider()
  lnkd_profile_url="https://www.linkedin.com/in/aadhyathmik/"
  st.sidebar.markdown("[Aadhyathmik Varahagiri](%s)" % lnkd_profile_url)  



#what change shall be made?



  st.sidebar.title("Welcome")
  st.sidebar.text(" ")
  st.sidebar.text(" ")
  st.sidebar.header("This is a free community version of Grader Bot AI")
  st.sidebar.text(" ")
  st.sidebar.text(" ")
 ### st.sidebar.text("Use This: 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")
  #st.sidebar.text(" ")
  #st.sidebar.text(" ")

  options = ["gpt-4o", "gpt-4o-mini", "gpt-4", "gpt-3.5-turbo"]

  # Single selection input
  model_input = st.sidebar.selectbox("Choose an option:", options, index=0)

  # Display the selected option
  #st.sidebar.write("You selected:", model_input)

  
  secret_key = st.secrets["openapi"]["openapi_key"]



  add_space(2)

  user_input = st.sidebar.text_input("OpenAI API Key", value = secret_key)
  #st.sidebar.write("Current input value:", user_input)

  


  add_space(5)

  # Get OpenAI API key
  openai_api_key = user_input

  url = "https://www.graderbotai.com"
  st.sidebar.markdown("Visit this [link](%s) to sign up for Upgraded Version" % url)  

  st.sidebar.text(" ")
  st.sidebar.text(" ")
  st.sidebar.text(" ")

  tos="https://graderbotai.com/terms-and-conditions/"
  pp="https://graderbotai.com/privacy-policy/"
  gvsc="https://graderbotai.com/graderbot-vs-chatgpt/"
  samplefiles="https://github.com/Aadhyathmik/GraderBotAI/tree/main/SampleFiles"
  st.sidebar.text(" ")
  st.sidebar.text(" ")
  st.sidebar.markdown("[Terms of Service](%s)" % tos)  
  st.sidebar.text(" ")
  st.sidebar.text(" ")
  st.sidebar.markdown("[Privacy Policy](%s)" % pp)  
  st.sidebar.text(" ")
  st.sidebar.text(" ")
  st.sidebar.markdown("[GraderBot vs ChatGPT](%s)" % gvsc)  

  image_file="Gbot.jpg"
  st.image(image_file, use_container_width=True)
  link_url="https://graderbotai.com/"
  


  st.divider()
  st.title("Assignment Evaluation and Feedback")

  st.markdown("# [Demo Files to test](%s)" % samplefiles)  
  

  st.divider()

  # Upload files (Syllabus, Rubric, Papers)
  uploaded_syllabus = st.file_uploader("Upload syllabus (Drop a pdf or txt file)", type=("txt", "md", "pdf"))
  uploaded_rubric = st.file_uploader("Upload rubric (Drop a pdf or txt file)", type=("txt", "md", "pdf"))
  uploaded_papers = st.file_uploader("Upload papers (Drop a pdf or txt file)", type=("txt", "md", "pdf"), accept_multiple_files=False)
  submit_button = st.button("Submit")
  #question = st.text_input(
  #    "Ask something about the article(s)",
  #    placeholder="Can you give me a short summary?",
  #    disabled=not uploaded_rubric,
  #)

  # Check for missing inputs
  if (uploaded_syllabus
      and uploaded_rubric
      and uploaded_papers
      #and question
      and not openai_api_key
      and submit_button
  ):
      st.info("1 or more inputs are missing. Please provide the missing input(s) to continue.")
  elif uploaded_syllabus and uploaded_rubric and uploaded_papers and openai_api_key and submit_button:
      
      # Process files
      syllabus_text = get_text_from_file(uploaded_syllabus)
      rubric_text = get_text_from_file(uploaded_rubric)
      paper_text = get_text_from_file(uploaded_papers)
    

     # LLM Structure
      all_responses = []
        
        # Given prompt
      #prompt = f"""Here's a syllabus:\n\n{syllabus_text}\n\nHere's a rubric:\n\n{rubric_text}\n\nHere's a paper:\n\n{paper_text}"""

      sys_prompt = f"""
You are an AI grading assistant tasked with evaluating a student's paper based on specific course expectations and grading criteria. Below are the course syllabus and grading rubric provided by the instructor:

**Syllabus:**  
{syllabus_text}

**Rubric:**  
{rubric_text}

Using the syllabus and rubric, assess the paper {paper_text}.

Provide feedback and a grade that reflects the rubrics scoring categories. Offer constructive comments where improvements are needed, and highlight strengths where applicable.
"""


        # Model
      client = openai.Client(api_key=openai_api_key)
      response = client.chat.completions.create(
          model= model_input,
          messages=[
              {"role": "user", "content": sys_prompt},
              {"role": "system", "content": "Grade the answers using syllabus, rubric and uploaded response"},
          ],
          temperature=1,
          max_tokens=1000,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0,
      )
        # Takes the first output choice given from the model
      msg = response.choices[0].message.content
      all_responses.append(msg)

      for i, response in enumerate(all_responses):
          st.write(f"Response for article {i + 1}:")
          st.write(response)

# Runs program
if __name__ == "__main__":
  main()


  
