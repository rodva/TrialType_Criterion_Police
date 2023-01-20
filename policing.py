## NAME: RODRIGO DE ALMEIDA
## This code is a "bad trial type police" officer.
## It is aimed to find violations of accuracy and latency per trial,
## and find which trial type it belongs to.

## Heating up:
import os
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
headingLine = 0

## Identifying the file you want to analyse:
fileToAnalyse = input("Please write the name of the data file with its filename extension, and press Enter:\n")

## Creating output files in writing mode:
fileAccuracy = open("trialsViolate_Accuracy.txt","w")
fileLatency = open("trialsViolate_Latency.txt","w")
latenciesPerBlock = open("blocksAverageLatencies.txt","w")
Means_perParticipant_1isTestBlock_perTrialType_acrossConIncon = open("Means_perParticipant_1isTestBlock_perTrialType_acrossConIncon.txt","w")
Means_1isTestBlock_perTrialType_perParticipant_acrossConIncon = open("Means_1isTestBlock_perTrialType_perParticipant_acrossConIncon.txt","w")
Means_perOrder = open("Means_perOrder_perTrialType_acrossConIncon.txt","w")
fileAllDscores = open("fileAllDscores.txt","w")

## Preparing the data file to open:
with open(fileToAnalyse, 'r') as fp:
    for l_no, line in enumerate(fp):
        if "Version	3.0" in line:
            headingLine = l_no+1
            break
fp.close()

arrestedFile = pd.read_csv(fileToAnalyse, sep='\t', header = headingLine, index_col=False, usecols=['participantCode', 'startingRule', 'isTestBlock', 'blockPairNumber', 'currentRule', 'trialNumber', 'trialType', 'timeToFirstAnswer', 'timeToCorrectResponse', 'accuracy'])

## Finding the average latency and accuracy per block of each trial type:
perBlock = arrestedFile.groupby(["isTestBlock","accuracy","currentRule","trialType"])[["timeToFirstAnswer","timeToCorrectResponse","accuracy"]].mean()
print("\n"+"Finding the average latency of each block"+"\n\n")
print(perBlock)
latenciesPerBlock.write(str(perBlock))

## Finding average latency and accuracy per trial type, per starting block order:
print("\n\n"+"Finding average latency and accuracy per trial type, per starting practice block order (1=con; 2=incon):"+"\n")
ana007 = arrestedFile.groupby(["isTestBlock","startingRule","trialType"])[["timeToCorrectResponse","accuracy"]].mean()
print(ana007)
Means_perOrder.write(str(ana007))

## Finding average latency and accuracy per trial type, per participant:
print("\n\n"+"Finding average latency and accuracy per trial type, order per participant:"+"\n")
ana01 = arrestedFile.groupby(["participantCode","isTestBlock","trialType"])[["timeToCorrectResponse","accuracy"]].mean()
Means_perParticipant_1isTestBlock_perTrialType_acrossConIncon.write(str(ana01))
print(ana01)

## Finding average latency and accuracy per trial type, practice blocks first:
print("\n\n"+"Finding average latency and accuracy per trial type, order pract/test block first:"+"\n")
ana02 = arrestedFile.groupby(["isTestBlock","trialType","participantCode"])[["timeToCorrectResponse","accuracy"]].mean()
Means_1isTestBlock_perTrialType_perParticipant_acrossConIncon.write(str(ana02))
print(ana02)

## Identifying trials that violate accuracy:
print("\n\n"+"Trials INACCURATELY responded to:"+"\n")
bustedAccuracy = arrestedFile.loc[arrestedFile['accuracy'] == 0]
print(bustedAccuracy)
fileAccuracy.write(str(bustedAccuracy))

## Identifying trials that violate latency:
print("\n\n"+"Trials responded to with LATENCY bigger than 2000ms:"+"\n")
bustedLatency = arrestedFile.loc[arrestedFile['timeToFirstAnswer'] > 2000]
print(bustedLatency)
fileLatency.write(str(bustedLatency))

## Finding D IRAP per trial type:
arrestedFile = pd.read_csv(fileToAnalyse, sep='\t', header = headingLine, index_col=False, usecols=['participantCode','D_IRAP_TrialType_1_Test_mean','D_IRAP_TrialType_2_Test_mean','D_IRAP_TrialType_3_Test_mean','D_IRAP_TrialType_4_Test_mean'])
print("\n\n"+"The D scores per trial type, per participant, is in fileAllDscores.txt and here:")
fileAllDscores.write(str(arrestedFile.groupby(["participantCode"])[["D_IRAP_TrialType_1_Test_mean","D_IRAP_TrialType_2_Test_mean","D_IRAP_TrialType_3_Test_mean","D_IRAP_TrialType_4_Test_mean"]].mean()))
print(arrestedFile.groupby(["participantCode"])[["D_IRAP_TrialType_1_Test_mean","D_IRAP_TrialType_2_Test_mean","D_IRAP_TrialType_3_Test_mean","D_IRAP_TrialType_4_Test_mean"]].mean())

## Fecking off:
fileAccuracy.close()
fileLatency.close()
latenciesPerBlock.close()
Means_perParticipant_1isTestBlock_perTrialType_acrossConIncon.close()
Means_1isTestBlock_perTrialType_perParticipant_acrossConIncon.close()
Means_perOrder.close()
fileAllDscores.close()
input("\n\nSuccess!\nThe information above is also stored in TXT files located in the folder where you ran this analysis from.\nPress anything to exit.\nCheers, Rodrigo.")
