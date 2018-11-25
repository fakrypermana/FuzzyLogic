import csv
import operator

def fuzzyIncome (row):
    listFuzzy = []
    if row[1]<=0.1119 or row[1] >= 1.7172:
        if row[1]<=0.4766:
            listFuzzy.append(["LOW",1])
        else:
            listFuzzy.append(["HIGH",1])
    elif row[1]>=0.9466 and row[1]<=1.1:
        listFuzzy.append(["MEDIUM",1])
    elif row[1]>=0.1119 and row[1]<0.9466:
        listFuzzy.append(["LOW", (0.9466-row[1])/(0.9466-0.1119)])
        listFuzzy.append(["MEDIUM", (row[1]-0.1119)/(0.9466-0.1119)])
    elif row[1]>1.1 and row[1]<=1.7172:
        listFuzzy.append(["MEDIUM", (1.7172-row[1])/(1.7172-1.1)])
        listFuzzy.append(["HIGH", (row[1]-1.1)/(1.7172-1.1)])
    return listFuzzy

def fuzzyDebt (row):
    listFuzzy = []
    if row[2]<=19.6 or row[2]>=78.4:
        if row[2]<=19.6:
            listFuzzy.append(["RENDAH",1])
        else:
            listFuzzy.append(["TINGGI",1])
    elif row[2]>=53.2 and row[1]<=58.8:
        listFuzzy.append(["SEDANG",1])
    elif row[2]>=19.6 and row[1]<=53.2:
        listFuzzy.append(["RENDAH", (53.2-row[2])/(53.2-19.6)])
        listFuzzy.append(["SEDANG", (row[2]-19.6)/(53.2-19.6)])
    elif row[2]>=58.8 and row[1]<=78.4:
        listFuzzy.append(["SEDANG", (78.4-row[2])/(78.4-58.8)])
        listFuzzy.append(["TINGGI", (row[2]-58.8)/(78.4-58.8)])
    return listFuzzy

def inference (inGaji,inHutang):
    arrInference = []
    #print(inGaji,inHutang)
    for rowGaji in inGaji:
        for rowHutang in inHutang:
            if rowGaji[0] == "HIGH" and rowHutang[0] == "TINGGI":
                if rowGaji[1] < rowHutang[1]:
                    arrInference.append(["considered", rowGaji[1]])
                else:
                    arrInference.append(["considered", rowHutang[1]])
            elif rowGaji[0] == "HIGH" and rowHutang[0] == "SEDANG":
                if rowGaji[1] < rowHutang[1]:
                    arrInference.append(["rejected", rowGaji[1]])
                else:
                    arrInference.append(["rejected", rowHutang[1]])
            elif rowGaji[0] == "HIGH" and rowHutang[0] == "RENDAH":
                if rowGaji[1] < rowHutang[1]:
                    arrInference.append(["rejected", rowGaji[1]])
                else:
                    arrInference.append(["rejected", rowHutang[1]])
            elif rowGaji[0] == "MEDIUM" and rowHutang[0] == "TINGGI":
                if rowGaji[1] < rowHutang[1]:
                    arrInference.append(["accepted", rowGaji[1]])
                else:
                    arrInference.append(["accepted", rowHutang[1]])
            elif rowGaji[0] == "MEDIUM" and rowHutang[0] == "SEDANG":
                if rowGaji[1] < rowHutang[1]:
                    arrInference.append(["considered", rowGaji[1]])
                else:
                    arrInference.append(["considered", rowHutang[1]])
            elif rowGaji[0] == "MEDIUM" and rowHutang[0] == "RENDAH":
                if rowGaji[1] < rowHutang[1]:
                    arrInference.append(["rejected", rowGaji[1]])
                else:
                    arrInference.append(["rejected", rowHutang[1]])

            elif rowGaji[0] == "LOW" and rowHutang[0] == "SEDANG":
                if rowGaji[1] < rowHutang[1]:
                    arrInference.append(["accepted", rowGaji[1]])
                else:
                    arrInference.append(["accepted", rowHutang[1]])
            elif rowGaji[0] == "LOW" and rowHutang[0] == "TINGGI":
                if rowGaji[1] < rowHutang[1]:
                    arrInference.append(["accepted", rowGaji[1]])
                else:
                    arrInference.append(["accepted", rowHutang[1]])
            elif rowGaji[0] == "LOW" and rowHutang[0] == "RENDAH":
                if rowGaji[1] < rowHutang[1]:
                    arrInference.append(["considered", rowGaji[1]])
                else:
                    arrInference.append(["considered", rowHutang[1]])

    #untuk menyeleksi jika scorenya ada yg sama maka ambil data yg derajatnya paling besar
    if len(arrInference)>1:
        if arrInference[0][0] == "accepted" and arrInference[1][0] == "accepted":
            if arrInference[0][1] > arrInference[1][1]:
                del arrInference[1]
            else:
                del arrInference[0]
        elif arrInference[0][0] == "considered" and arrInference[1][0] == "considered":
            if arrInference[0][1] > arrInference[1][1]:
                del arrInference[1]
            else:
                del arrInference[0]
        elif arrInference[0][0] == "rejected" and arrInference[1][0] == "rejected":
            if arrInference[0][1] > arrInference[1][1]:
                del arrInference[1]
            else:
                del arrInference[0]
    #print("after inference",arrInference)
    return arrInference

def deffuzification (arrInference):
    x = 0
    y = 0
    for inInfer in arrInference:
        if inInfer[0]=="accepted":
            x = x+(inInfer[1]*100)
            y = y+(inInfer[1])
        elif inInfer[0]=="considered":
            x = x+(inInfer[1]*70)
            y = y+(inInfer[1])
        elif inInfer[0]=="rejected":
            x = x+(inInfer[1]*50)
            y = y+(inInfer[1])


    score = x/y
    #print("score",score)
    return score

with open('DataTugas2.csv') as csv_file:
    csv_reader = csv.reader(csv_file,skipinitialspace = True)
    listData = []
    next(csv_reader)
    terpilih = []
    data = []
    for row in csv_reader:
        row[1] = float(row[1])
        row[2] = float(row[2])
        row[0] = int(row[0])
        listData.append([row[0],deffuzification(inference(fuzzyIncome(row),fuzzyDebt(row)))])

    data = sorted(listData, key=operator.itemgetter(1), reverse=True)
    for i in range(0, 20):
        terpilih.append([data[i][0]])

    terpilih = sorted(terpilih, key=operator.itemgetter(0))
    print(terpilih)


    with open('TebakanTugas2.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(terpilih)
