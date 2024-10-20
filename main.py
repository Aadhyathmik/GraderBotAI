import streamlit as st
import openai
import PyPDF2

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

def add_space(n=1):
  for _ in range(n):
    st.sidebar.text(" ")

def main():
  """
  The main function that handles the Streamlit app logic.
  """


# Title

  st.sidebar.image("Gbot.jpg", use_column_width=True)
  st.sidebar.divider()
  lnkd_profile_url="https://www.linkedin.com/in/aadhyathmik/"
  st.sidebar.markdown("[Aadhyathmik Varahagiri](%s)" % lnkd_profile_url)  


  st.sidebar.title("Welcome")
  st.sidebar.text(" ")
  st.sidebar.text(" ")
  st.sidebar.header("This is a free community version of Grader Bot AI")
  st.sidebar.text(" ")
  st.sidebar.text(" ")
  user_input = st.sidebar.text_input("OpenAI API Key")
  add_space(10)

  # Get OpenAI API key
  openai_api_key = user_input

  url = "https://www.graderbotai.com"
  st.sidebar.markdown("Visit this [link](%s) to sign up for Upgraded Version" % url)  

  st.sidebar.text(" ")
  st.sidebar.text(" ")
  st.sidebar.text(" ")

  tos="https://graderbotai.com/terms-and-conditions/"
  pp="https://graderbotai.com/privacy-policy/"
  st.sidebar.text(" ")
  st.sidebar.text(" ")
  st.sidebar.markdown("[Terms of Service](%s)" % tos)  
  st.sidebar.text(" ")
  st.sidebar.text(" ")
  st.sidebar.markdown("[Privacy Policy](%s)" % pp)  
  

  image_file="Gbot.jpg"
  st.image(image_file, use_column_width=True)
  link_url="https://graderbotai.com/"
  


  st.divider()
  st.title("Assignment Evaluation and Feedback")

  # Upload files (Syllabus, Rubric, Papers)
  uploaded_syllabus = st.file_uploader("Upload syllabus", type=("txt", "md", "pdf"))
  uploaded_rubric = st.file_uploader("Upload rubric", type=("txt", "md", "pdf"))
  uploaded_papers = st.file_uploader("Upload papers", type=("txt", "md", "pdf"), accept_multiple_files=False)
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
  ):
      st.info("1 or more inputs are missing. Please provide the missing input(s) to continue.")
  elif uploaded_syllabus and uploaded_rubric and uploaded_papers and openai_api_key:
      
      # Process files
      syllabus_text = get_text_from_file(uploaded_syllabus)
      rubric_text = get_text_from_file(uploaded_rubric)
      paper_text = get_text_from_file(uploaded_papers)
    

     # LLM Structure
      all_responses = []
        
        # Given prompt
      prompt = f"""Here's a syllabus:\n\n{syllabus_text}\n\nHere's a rubric:\n\n{rubric_text}\n\nHere's a paper:\n\n{paper_text}"""

        # Model
      client = openai.Client(api_key=openai_api_key)
      response = client.chat.completions.create(
          model="gpt-3.5-turbo",
          messages=[
              {"role": "user", "content": prompt},
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


  
