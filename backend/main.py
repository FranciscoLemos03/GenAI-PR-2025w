# import_pdfs_to_db.py
import os
from data_manager import DataManager, PDF_FOLDER, DATABASE_FILE, EXAMPLE_FOLDER
from baseline_retriever import BaselineRetriever
from datetime import date

os.makedirs(PDF_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(DATABASE_FILE), exist_ok=True)


###   1. ADD 20 PDFS TO THE DATABASE INITIALLY, TO HAVE SOME EXAMPLES
###      (this part is skipped automatically if they are already on the database)
### -------------------------------------------------------------------

"""N_TO_IMPORT = 20

dm = DataManager()

existing_pdf_names = {doc["pdf_name"] for doc in dm.database}
pdf_files = [f for f in os.listdir(EXAMPLE_FOLDER) if f.lower().endswith('.pdf')]

# Sort files chronologically and select the first 20
pdf_files.sort()
files_to_process = pdf_files[:N_TO_IMPORT]

print(f"Found {len(pdf_files)} PDFs. Processing {len(files_to_process)} files...")

for filename in files_to_process:

    if filename in existing_pdf_names:
        print(f"   Skipping {filename}: Already exists in database.json.")
        continue

    file_path = os.path.join(EXAMPLE_FOLDER, filename)
    name_without_ext = filename.replace(".pdf", "") 
    parts = name_without_ext.split("_")

    if len(parts) >= 3:
        date_str = parts[0]
        researcher = parts[1]
        title = parts[2]
        print(f"\nUploading: {filename}...")
        
        try:
            dm.upload_pdf(
                file_path=file_path, 
                title=title, 
                day=date_str,
                researcher=researcher)
        except Exception as e:
            print(f"   Failed to upload: {e}")
    else:
        print(f"   Skipping {filename}: Filename does not follow the YYYY-MM-DD_Name_Title format.")

print("\n\n\n")"""



###   2. RUN THE MAIN PROGRAMM
### -------------------------------------------------------------------

while True:

    action = input("Main menu:\n  1. Upload\n  2. Retrieve\n> ")
    dm = DataManager()
    retr = BaselineRetriever()

    # ------------------ UPLOAD ------------------
    if action == "1":
        # -------------------- examples: -----------------------------
        # 1. 
        #       example_pdfs_to_upload/2026-01-05_Alice-Robertson_Compliance-Review.pdf
        #       Compliance Review
        #       Alice Robertson
        #       2026-01-05      
        # 2. 
        #       example_pdfs_to_upload/2026-01-08_Chloe-Nguyen_Multimodal-Fusion-Logic.pdf
        #       Multimodal Fusion Logic
        #       Chloe Nguyen
        #       2026-01-08
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
        day = date.today()

        # Upload pdf to the database
        dm = DataManager()
        dm.upload_pdf(file_path, title, day, researcher)

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




    # ------------------ SUMMARIZE ------------------
    #from summarizer import Summarizer
    #summ = Summarizer()
    #elif action == "3":
    #    summ.summarize_all()


