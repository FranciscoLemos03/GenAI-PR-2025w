from data_manager import DataManager
from baseline_retriever import BaselineRetriever


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
        # entry = dm.upload_pdf(file_path, title, researcher)

        # Create and save embeddings
        # dm.process_pdf(entry)
        dm = DataManager()
        dm.upload_pdf(file_path, title, researcher)

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
                print(f"- {r['title']}\n"
                      f"      Score: {r['score']})\n      Researcher: {r['researcher']}\n\n")

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


