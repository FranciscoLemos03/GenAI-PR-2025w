from data_manager import DataManager
from summarizer import Summarizer


dm = DataManager()
summ = Summarizer()


while True:

    action = input("Main menu:\n  1. Upload\n  2. Summarize\n  3. Retrieve\n> ")


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
        entry = dm.upload_pdf(file_path, title, researcher)

        # Create and save embeddings
        dm.process_pdf(entry)


    # ------------------ SUMMARIZE ------------------
    elif action == "2":
        while True:
            sub = input("\nSummarization options:\n  1. Summarize ALL papers\n  2. Summarize by researcher\n> ")

            if sub == "1":
                summ.summarize_all()
                break

            elif sub == "2":
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
                summ.summarize_by_researcher(researcher)
                break
            else:
                print("Invalid option. Please choose 1 or 2.\n")



    # ------------------ RETRIEVE ------------------
    elif action == "3":
        print("Retrieve functionality goes here")