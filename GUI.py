from tkinter import *

from documentCollection import DocumentCollection
from indexer import Indexer
from rank import Rank
from search import Search


class Window:

    @staticmethod
    def show(documents, index):

        win = Tk()  # creating window
        win.title("Information Retrieval System")  # window title
        win.geometry("500x300")

        # Create a label
        FYI_lbl = Label(win, text="This program will retrieve the documents (from "
                                  "DocumentCollection folder)\n that are relevant to "
                                  "your search phrase.", fg="#E83A14", font=("Helvetica", 10))
        FYI_lbl.pack(pady=20)

        # Create an entry box
        entry = Entry(win, font=("Helvetica", 20))
        entry.pack()

        # Create a listbox
        listbox = Listbox(win, width=50)
        listbox.pack(pady=40)

        def update(result_documents):
            # Clear the listbox
            listbox.delete(0, END)

            # Add documents to the listbox
            counter = 1
            for document in result_documents:
                listbox.insert(END, str(counter) + "-  " + document)
                counter += 1

        def check(e):
            # Grab what was typed
            typed = entry.get()

            result_documents = []
            if typed == "":
                result_documents = documents
            else:
                relevant = Search.get_relevant_docs(typed, index)
                if len(relevant) == 0:  # If there is no matching documents
                    result_documents = []
                else:
                    result = Rank.rank_results(typed, documents, index, relevant)
                    result_documents = [document_tuple[0] for document_tuple in result]

            update(result_documents)

        # Showing all documents at first
        update(documents)

        # Create a binding on the entry box
        entry.bind("<KeyRelease>", check)

        win.mainloop()  # showing the window