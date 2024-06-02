
import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

class summariz():
   def __init__(self) -> None:
        self.GOOGLE_API_KEY=""
        genai.configure(api_key=self.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')

