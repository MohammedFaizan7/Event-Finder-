import google.generativeai as genai
from tkinter import messagebox

class Geminiai:
    def _init_(self,api_key):
        self.api_key=api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
    def ask_question(self,question):
        response = self.model.generate_content(f"{question} in 10 words")
        generated_text=response.text
        words=generated_text.split()
        limited_response=" ".join(words[:10])
        return limited_response
