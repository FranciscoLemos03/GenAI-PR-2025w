# import_pdfs_to_db.py
import os
import arxiv
from data_manager import DataManager, PDF_FOLDER, DATABASE_FILE, EXAMPLE_FOLDER
from baseline_retriever import BaselineRetriever

os.makedirs(PDF_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(DATABASE_FILE), exist_ok=True)


###   1. ADD 15 PDFS TO THE DATABASE INITIALLY, TO HAVE SOME EXAMPLES
###      (this part is skipped automatically if they are already on the database)
### -------------------------------------------------------------------

N_TO_IMPORT = 15
researchers = ["Alice Robertson", "Bob Martinez", "Chloe Nguyen", "Daniel Fischer"]

# Load PDFs from example folder
pdf_files = [f for f in os.listdir(EXAMPLE_FOLDER) if f.lower().endswith(".pdf")]
if len(pdf_files) < N_TO_IMPORT:
    raise ValueError(f"Not enough PDFs in example_pdfs_to_upload" )
selected_pdfs = pdf_files[:N_TO_IMPORT]


# Upload them to the database
dm = DataManager()
client = arxiv.Client()
for i, pdf_file in enumerate(selected_pdfs):
    arxiv_id = pdf_file.replace(".pdf", "")
    pdf_path = os.path.join(EXAMPLE_FOLDER, pdf_file)

    out_path = os.path.join(dm.pdf_folder, f"{arxiv_id}.pdf")
    if os.path.exists(out_path):
        print(f"Skipping already uploaded PDF: {arxiv_id}.pdf")
        continue
    
    print(f"\n[{i+1}/{N_TO_IMPORT}] Importing arXiv:{arxiv_id}")

    # Find title of paper with arXiv ID
    search = arxiv.Search(id_list=[arxiv_id], max_results=1)
    results = list(client.results(search))
    if not results:
        print("Could not resolve title for:", arxiv_id)
        continue
    else:
        title = results[0].title.strip().replace("\n", " ")

    researcher = researchers[i % len(researchers)]
    dm.upload_pdf(pdf_path, title, researcher, arxiv_id)

print("\n\n\n")



###   2. RUN THE MAIN PROGRAMM
### -------------------------------------------------------------------

while True:

    action = input("Main menu:\n  1. Upload\n  2. Retrieve\n> ")
    dm = DataManager()
    retr = BaselineRetriever()

    # ------------------ UPLOAD ------------------
    if action == "1":
        # ---------------- examples:
        # example_pdfs_to_upload/2104.10157v2.pdf   - VideoGPT: Video Generation using VQ-VAE and Transformers
        # example_pdfs_to_upload/2109.07830v3.pdf   - Reframing Instructional Prompts to GPTk's Language
        # ------------------------------------------------------------

        # Select pdf
        file_path = input("Enter path to PDF: ")
        arxiv_id = os.path.splitext(os.path.basename(file_path))[0]
        
        # Enter metadata
        title = input("Enter paper title: ")
        researchers = ["Alice Robertson", "Bob Martinez", "Chloe Nguyen", "Daniel Fischer"]
        while True:
            print("Select researcher:")
            for idx, name in enumerate(researchers, start=1):
                print(f"  {idx}. {name}")
            choice = input("Enter number: ")
            if choice.isdigit() and 1 <= int(choice) <= len(researchers):
                researcher = researchers[int(choice) - 1]
                break
            else:
                print("Invalid selection. Please choose a number from the list.\n")

        # Upload pdf to the database
        dm = DataManager()
        dm.upload_pdf(file_path, title, researcher, arxiv_id)

    # ------------------ RETRIEVE ------------------
    elif action == "2":
        retr = BaselineRetriever()
        query = input("Enter a concept/idea to search:\n> ")
        results = retr.search(query, threshold=0.50)
        if not results:
            print("\nNo relevant papers found for that query.\n")
        else:
            print("\nResults:")
            for r in results:
                print(f"- {r['pdf_name']}\n"
                      f"  {r['title']}\n"
                      f"      Score: {r['score']}\n      Researcher: {r['researcher']}\n\n")

        """
        "unsupervised language modeling with transformers"	1907.02052v1, 1911.02365v1
        "scaling laws in GPT models"	1911.02365v1
        "prompting techniques for text generation"	1911.00536v3
        "conditional text synthesis using GPT"	1911.00536v3
        "how GPT improves with more parameters"	1911.02365v1
        "autoregressive transformer for sentence continuation"	1907.02052v1

        NO PAPERS RETURNED
        "quantum computing optimization for cryptography"
        "protein folding transformers"
        "graph neural networks for social networks"
        """


    # ------------------ SUMMARIZE ------------------
    #from summarizer import Summarizer
    #summ = Summarizer()
    #elif action == "3":
    #    summ.summarize_all()


