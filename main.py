from documentCollection import DocumentCollection
from indexer import Indexer
from GUI import Window


documents = DocumentCollection.get_file_names("DocumentCollection")
index = Indexer.pos_index(documents)

Window.show(documents, index)




