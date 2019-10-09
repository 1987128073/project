from pymongo import MongoClient
import csv

client = MongoClient("mongodb://192.168.1.45:27017")
database = client["pltaobao"]
collection = database["anchor_info"]
goods = database['tb_anchor_goods']
query = {
    "fansCount": {
        "$gt": 100000
    }
}

 


outFile = "test.csv"
 
outFileCsv = open(outFile,"a+",newline='')
 
fileheader = ['archorid','goodid']
outDictWriter = csv.DictWriter(outFileCsv,fileheader)
outDictWriter.writeheader()
#outDictWriter.writerow({'archorid':'abc' })
 
# Created with NoSQLBooster, the essential IDE for MongoDB - https://nosqlbooster.com
anchorlist = collection.find(query, limit=20)
try:
    for anchor in anchorlist:
        print(1)
        #print(doc["_id"]," -- ",doc["anchorId"])
    #先写入columns_name
    #writer.writerow("anchorId" )
		#data_row = doc["anchorId"]
        querygoods = {
          "accountId": anchor["anchorId"]
        }
        sort = [("_id", -1)]
        goodlist = goods.find(querygoods, sort=sort, limit=1)
        #goodlist = goods.findone(querygoods)
        #good=goodlist.fetchone()
        print(querygoods)
        outDictWriter.writerow({'archorid':anchor["anchorId"],'goodid':"2"})
        #if len(list(goodlist)):
        for good in goodlist:
        #if (good):
            print(good)
            print(3)
            outDictWriter.writerow({'archorid':anchor["anchorId"],'goodid':good["itemId"]})
		 
    else:
        print("没有循环数据!")
    print("完成循环!")

 

	
finally:
    anchorlist.close()
    outFileCsv.close() 
