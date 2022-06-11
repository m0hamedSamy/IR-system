from nltk import word_tokenize
from nltk.corpus import stopwords
from prettytable import PrettyTable
import math

class PrintValue:
    def TableViews(self, files_to_terms_index):

        AllDocuments = files_to_terms_index


        ############################################### to Get Term Frequency ###########################

        mytable = PrettyTable(["   ", "doc1", "doc2", "doc3", "doc4", "doc5", "doc6", "doc7", "doc8", "doc9", "doc10"])
        noDublicated = []
        ### get words
        for key in AllDocuments:
            list = AllDocuments[key]
            for item in list:
                if item not in noDublicated:
                    noDublicated.append(item)

        # noDublicated.sort()
        ResultFrequency = []

        for word in noDublicated:
            list = [word]
            for values in AllDocuments:
                if word in AllDocuments[values]:
                    list.append(AllDocuments[values].count(word))
                else:
                    list.append("0")
            ResultFrequency.append(list)
            mytable.add_row(list)

        print("############################################### Term Frequency ############################################### ")
        print(mytable)
        mytable.clear_rows()
        ############################################### to GetWieght Values ######################################################
        MyWieght = []
        for i in range(0, len(ResultFrequency)):
            MyWieght.append(ResultFrequency[i].copy())
        print(
            "############################################### Wieght Values ###############################################")
        for list in MyWieght:
            for i in range(0, len(list)):
                if i == 0:
                    continue
                if list[i] == '0':
                    list[i] = '0'
                else:
                    list[i] = str(1 + math.log10(int(list[i])))
            mytable.add_row(list)

        print(mytable)
        mytable.clear_rows()
        MyWieght.clear()
        ############################################### to Get  DF and IDF ######################################################

        MyIdf = []
        mytable = PrettyTable(["    ", "DF", "IDF"])
        for word in noDublicated:
            counter = 0
            list = []
            list.append(word)
            for i in AllDocuments:
                if word in AllDocuments[i]:
                    counter = counter + AllDocuments[i].count(word)
            list.append(counter)
            list.append(str(math.log10(10 / counter)))
            MyIdf.append(list)
            mytable.add_row(list)

        print(
            "############################################### DF and IDF ######################################################")

        print(mytable)
        # mytable.clear()

        ###############################################   tf*IDF    ######################################################

        print(
            "############################################### TF * IDF #######################################################")
        mytable = PrettyTable(["   ", "doc1", "doc2", "doc3", "doc4", "doc5", "doc6", "doc7", "doc8", "doc9", "doc10"])
        ResultIDF = [];
        j = 0
        for list in ResultFrequency:
            value = [list[0]]
            for i in range(1, len(list)):
                value.append(str(float(list[i]) * float(MyIdf[j][2])))
            j = j + 1;
            ResultIDF.append(value)
            mytable.add_row(value)

        print(mytable)
        mytable.clear();

        ## use table
        ###############################################   Lenght    ######################################################
        item = 0.0
        mytable = PrettyTable(["Docments", "Length"])
        Total = [];
        for i in range(1, 11):
            item = 0.0
            list = [str(i)]
            for j in range(0, len(ResultIDF)):
                item = item + math.pow(float(ResultIDF[j][i]), 2)
            item = math.sqrt(item)
            list.append(str(item))
            Total.append(str(item))
            mytable.add_row(list)
        print(mytable)
        mytable.clear()

        ###############################################   Normalize    ######################################################

        column = [" Words  ", "doc1", "doc2", "doc3", "doc4", "doc5", "doc6", "doc7", "doc8", "doc9", "doc10"]
        currentColumn = 0
        list = []
        for i in range(0, len(ResultIDF)):
            list.append(ResultIDF[i][0])
        mytable.add_column(column[0], list)
        for i in range(1, 11):
            ColumnValues = []
            for j in range(0, len(ResultIDF)):
                ColumnValues.append(str(float(ResultIDF[j][i]) / float(Total[currentColumn])))

            currentColumn = currentColumn + 1
            mytable.add_column(column[currentColumn], ColumnValues)
        print(mytable)


    def normalize_matrix(self, query, files_to_terms_index):

        AllDocuments = files_to_terms_index
        AllDocuments["query"] = query.lower().split()

        noDublicated = []
        ### get words
        for key in AllDocuments:
            list = AllDocuments[key]
            for item in list:
                if item not in noDublicated:
                    noDublicated.append(item)

        # noDublicated.sort()
        ResultFrequency = []

        for word in noDublicated:
            list = [word]
            for key in AllDocuments:
                if word in AllDocuments[key]:
                    list.append(AllDocuments[key].count(word))
                else:
                    list.append("0")
            if word in query.split():
                list
            ResultFrequency.append(list)

        MyWieght = []
        for i in range(0, len(ResultFrequency)):
            MyWieght.append(ResultFrequency[i].copy())

        for list in MyWieght:
            for i in range(1, len(list)):
                if list[i] == '0':
                    list[i] = '0'
                else:
                    list[i] = str(1 + math.log10(int(list[i])))

        MyWieght.clear()

        MyIdf = []

        for word in noDublicated:
            counter = 0
            list = []
            list.append(word)
            for i in AllDocuments:
                if word in AllDocuments[i]:
                    counter = counter + 1
            if word in query:
                counter -= 1
            list.append(counter)
            list.append(str(math.log10(10 / counter)))
            MyIdf.append(list)

        ResultIDF = []
        j = 0
        for list in ResultFrequency:
            value = [list[0]]
            for i in range(1, len(list)):
                value.append(str(float(list[i]) * float(MyIdf[j][2])))
            j = j + 1
            ResultIDF.append(value)


        ## use table
        ###############################################   Lenght    ######################################################
        item = 0.0
        mytable = PrettyTable(["Docments", "Length"])
        Total = []
        for i in range(1, 12):
            item = 0.0
            list = [str(i)]
            for j in range(0, len(ResultIDF)):
                item = item + math.pow(float(ResultIDF[j][i]), 2)
            item = math.sqrt(item)
            list.append(str(item))
            Total.append(str(item))

        ###############################################   Normalize    ######################################################

        currentColumn = 0

        query_normalize = []
        ColumnValues = []
        for i in range(1, 12):
            list = []
            for j in range(0, len(ResultIDF)):
                list.append(str(float(ResultIDF[j][i]) / float(Total[currentColumn])))
            ColumnValues.append(list)
            currentColumn = currentColumn + 1


        return ColumnValues





