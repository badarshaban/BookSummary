from arguments import Arguments as args
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import PyPDFLoader
from langchain.llms import OpenAI
from langchain import PromptTemplate
import time
from fpdf import FPDF


class BookSummary:
    def __init__(self):
        pass

    def read_text_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            return content
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
        except:
            print("An error occurred while reading the file.")

    def pdf_splitter(self, pdf_file_path):

        loader = PyPDFLoader(pdf_file_path)
        docs = loader.load_and_split()
        print("There are: ",len(docs), " documents in total")

        return docs
    
    def summarize_pdf(self, docs):

        start_time = time.time()

        map_custom_prompt = self.read_text_file(args.map_custom_prompt)
        map_prompt_template = PromptTemplate(
            input_variables = ['text'],
            template=map_custom_prompt
            )

        combine_custom_prompt = self.read_text_file(args.combine_custom_prompt)
        combine_prompt_template = PromptTemplate(
            template=combine_custom_prompt, 
            input_variables=['text']
            )

        summary_chain = load_summarize_chain(
            llm=OpenAI(temperature=args.temp),
            chain_type='map_reduce',
            map_prompt=map_prompt_template,
            combine_prompt=combine_prompt_template,
            verbose=False
        )
        final_summary = summary_chain.run(docs)
        end_time = time.time()

        print("Summary Generation Execution Time: ", str(round(end_time - start_time,2))+" seconds")
        return final_summary
    
    def generate_pdf(self, doc_path, summary):
        text = doc_path.split("/")
        text1 = text[-1].split('.pdf')[0]
        text1 = "Summary_"+text1+".pdf"
        text[-1] = text1
        output_file_path = "/".join(text)

# Create PDF
        class PDF(FPDF):
            def header(self):
                self.set_font('Arial', 'B', 12)
                self.cell(0, 10, 'Summary', 0, 1, 'C')

            def chapter_title(self, title):
                self.set_font('Arial', 'B', 12)
                self.cell(0, 10, title, 0, 1, 'L')
                self.ln(10)

            def chapter_body(self, body):
                self.set_font('Arial', '', 12)
                
                # Use utf-8 encoding to handle special characters
                body = body.encode('latin-1', 'replace').decode('latin-1')
                
                self.multi_cell(0, 10, body)
                self.ln()

        pdf = PDF()
        pdf.add_page()

        # Split the text into paragraphs and add to the PDF
        paragraphs = [line.strip() for line in summary.replace('\n\n','\n').strip().split('\n')]
        for paragraph in paragraphs:
            pdf.chapter_body(paragraph)

        # Save the PDF
        pdf.output(output_file_path)
        
        print(f"PDF file '{output_file_path}' has been created.")


    def BookSummary(self, doc_path):
        docs_to_summarize = self.pdf_splitter(doc_path)
        response = self.summarize_pdf(docs_to_summarize[0:])
        self.generate_pdf(doc_path, response)
        return response


    def callBookSummary(self, doc_path):
        start_time = time.time()
        summary = self.BookSummary(doc_path)
        end_time =time.time()
        print("Overall Tool Execution Time: ", str(round(end_time - start_time,2))+" seconds")
        return summary

if __name__ == "__main__":

    book_summary = BookSummary()
    document =  "crime-and-punishment.pdf" # Enter your book path here!
    response = book_summary.callBookSummary(document)
    print("Summary")
    print(response)
    print()
