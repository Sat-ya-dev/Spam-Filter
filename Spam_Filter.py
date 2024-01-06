import csv
import re
import numpy as np

Spam = {}  # dictionary for storing spam words with their frequency
Non_Spam = {}  # dictionary for storing spam words with their frequency

# words to ignore
prop = ['a', 'an', 'the', 'for', 'from', 'by', 'over', 'on', 'off', 's', 'in', 'to', 'â', 'and', 'of', 'or', 'm', 't',
        'is', 'at', 'that', 'but', 'so', 'it', 'not', 'are']

total_spmsg = 0  # total spam messages
total_nspmsg = 0
with open('sms.csv', 'r') as f:
    s = csv.reader(f, delimiter='\t')
    for row in s:
        #         words=[]
        temp = []
        lis = []
        if row[0] == 'spam':
            total_spmsg += 1
            temp = row[1::]
            for st in temp:
                st = st.lower()
                lis = re.findall(r'\w+', st)
                for ele in lis:
                    if ele in prop:
                        continue
                    elif ele.isnumeric():
                        continue
                    elif ele in Spam:
                        Spam[ele] += 1
                    else:
                        Spam[ele] = 1
        elif row[0] == 'notspam':
            total_nspmsg += 1
            temp = row[1::]
            for st in temp:
                st = st.lower()
                lis = re.findall(r'\w+', st)
                for ele in lis:
                    if ele in prop:
                        continue
                    elif ele.isnumeric():
                        continue
                    elif ele in Non_Spam:
                        Non_Spam[ele] += 1
                    else:
                        Non_Spam[ele] = 1

# print(Spam)
val1 = []
val1 = sorted(Spam.values(), reverse=True)  # arranging values of Spam dictionary in descending order

print("Top 10 spam words are ->")
for i in range(10):
    for key in Spam.keys():
        if Spam[key] == val1[i]:  # finding the key that matches with the value
            print(key, " : ", Spam[key])

print("\n")
val2 = []
val2 = sorted(Non_Spam.values(), reverse=True)

print("Top 10 notspam words are ->")
for i in range(10):
    for key in Non_Spam.keys():
        if Non_Spam[key] == val2[i]:
            print(key, " : ", Non_Spam[key])
print("\n")

sp_total = 0  # total spam words
nsp_total = 0  # total non spam words
for value in Spam.values():
    sp_total += value
for value in Non_Spam.values():
    nsp_total += value
p = 10 ** (-8)  # probability if word is not present in both dictionaries


def Prob(word, T):
    if T == 'spam':
        if word not in Spam:
            return p
        else:
            count = Spam[word]
            pr = count / sp_total
            return pr
    elif T == 'non-spam':
        if word not in Non_Spam:
            return p
        else:
            count = Non_Spam[word]
            pr = count / nsp_total
            return pr


# print(sp_total)
# print(Prob('call', 'spam'))

def spam_check(m):
    lis = re.findall(r'\w+', m)
    ps = total_spmsg / (total_spmsg + total_nspmsg)  # P(spam messages)
    pn = total_nspmsg / (total_spmsg + total_nspmsg)  # P(nonspam messages)
    pm_sp = 1
    pm_nsp = 1
    for word in lis:
        pm_sp *= Prob(word, 'spam')  # P(m|spam)
        pm_nsp *= Prob(word, 'non-spam')

    Psp_m = pm_sp * ps / (pm_sp * ps + pm_nsp * pn)  # P(m|spam)*P(spam messages)/P(m)
    Pnsp_m = pm_nsp * pn / (pm_sp * ps + pm_nsp * pn)
    #     print(pm_sp)
    #     print((pm_sp*ps + pm_nsp*pn))
    print("Prob of spam given msg = ",Psp_m)

    x = np.random.choice([1, 0], p=[Psp_m, Pnsp_m])
    if x == 0:
        print("The message m is not a spam message")
    else:
        print("The message m is a spam message")

# enter a sentence to classify it as spam or non-spam
m = input("Enter a string :")
spam_check(m)