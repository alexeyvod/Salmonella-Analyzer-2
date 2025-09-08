#Импортируем библиотеки
import os
import multiprocessing
import time
import glob
import argparse, sys

#Обозначаем требуемые параметры для работы программы
parser=argparse.ArgumentParser(description="Salmonella Analyzer")

parser.add_argument("-j", help="Jar file of program", dest='jar', required=True)
parser.add_argument("-i", help="Input directory", dest='inp', required=True)
parser.add_argument("-o", help="Output directory", dest='out', required=True)
parser.add_argument("-t", help="Number of threads", dest='t', required=True, type=int)

args=parser.parse_args()

#Привязываем параметры к переменным
in_fasta_dir = args.inp
RezDir = args.out
MaxThreads = args.t
JarFilePath = args.jar

path = os.path.abspath(os.path.dirname(__file__))
os.chdir(path)

qual = input("Do you need to perform quality validation? (y/n): ")
sero = input("Do you need to perform serotyping? (y/n): ")
crisp = input("Do you need to perform CRISPR-typing? (y/n): ")
viro = input("Do you need to perform virulome-typing? (y/n): ")
ind = input("Do you need to perform INDEL-typing? (y/n): ")
snp = input("Do you need to perform SNP-typing? (y/n): ")

if qual == "n": qual = '-noQuality '
else: qual = ''

if sero == "n": sero = '-noSero '
else: sero = ''

if crisp == "n": crisp = '-noCRISPR '
else: crisp = ''

if viro == "n": viro = '-noVirulome '
else: viro = ''

if ind == "n": ind = '-noINDEL '
else: ind = ''

if snp == "n": snp = '-noSNP'
else: snp = ''

try:
    os.mkdir(RezDir)
except:
    print(f'{RezDir} уже есть')

InList = []
for in_fasta_file in glob.glob(in_fasta_dir + "/**/*.fa*", recursive = True):
    InList.append(in_fasta_file)

def Compute(fn):
    print(f'{fn}')
    BaseName = os.path.splitext(os.path.basename(fn))[0]
    OutFile = RezDir + os.path.sep + BaseName + '.json'
    command = f'java -jar "{JarFilePath}" -i "{fn}" -r "{OutFile}" {qual}{sero}{crisp}{viro}{ind}{snp}'
    #command = f'java -jar "{JarFilePath}" -i "{fn}" -r "{OutFile}"'
    print(command) 
    res = os.system(command)
    print(res)
    time.sleep(0.5)


def init(l):
    global lock
    lock = l

if __name__ == "__main__":
    l = multiprocessing.Lock()
    pool = multiprocessing.Pool(initializer=init, initargs=(l,), processes = MaxThreads)
    pool.map(Compute, InList)
    time.sleep(0.5)
    print("Done")
