import requests, time, os, json, random, pycurl, io, certifi
from textblob import TextBlob
from requests import get,post
from urllib.parse import urlencode


def load(waktune):
	for z in range(0,waktune):
		timelap="Loading"+"."*z
		print(timelap, end="\r")
		time.sleep(0.2)

try:
	infoo=open("D:\script\PYTHON\chai\history.txt", "r")
	with infoo as inf:
		inf_hsl="Dialogue : "+str(len(inf.readlines()))
except:
    inf_hsl = "Dialogue : 0"
os.system("cls")
print(f"""
=====================================
           ABOUT THIS AI
=====================================
Total {inf_hsl}
• Clear all memory => "erase all"
• Clear first => "erase first memory"
• Clear last => "erase last memory"
• Detail memory => "show memory"
• Introduce yourself first
• Don't pressed AI
=====================================
""")


url="https://model-api-shdxwd54ta-nw.a.run.app/generate/gptj"


head={
"Host": "model-api-shdxwd54ta-nw.a.run.app",
"developer_uid": "mUCsg14rQqYbpRkcqMbiPKa29xg1",
"developer_key": "sLdHjVjwMKd_7pd4C4l8S8yugfqq8caILaez7KJAmtKrZErnAOIVx_RoyOF6xRcAMvQ_yqlkxEWi87X0FIoaOg",
"user-agent": "Mozilla/5.0 (Linux; Android 11; Infinix X662 Build/RP1A.200720.011;) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.85 Mobile Safari/537.36"
}

try:
	countline=len(open("D:\script\PYTHON\chai\history.txt", "r").readlines())
	if countline <= 5:
		totaltime=3
	if countline > 5 and countline <= 10:
		totaltime=5
	if countline > 10 and countline <= 50:
		totaltime=6
	if countline > 50:
		totaltime=10
	load(totaltime)
	time.sleep(random.randint(1,3))
	print("""
|||||||||||||||||||||||||||||||||||||
 ARTIFICIAL INTELLIGENCE HAS STARTED
|||||||||||||||||||||||||||||||||||||
""")
	while True:
		kata=input("Me : ")
		pen=open("D:\script\PYTHON\chai\history.txt",'r+')
		tek=pen.read()
		if "erase all" in kata:
			print("ERASING ALL DATA MEMORY....")
			time.sleep(2)
			pen.truncate(0)
			print("Erase success, restart....")
			os.system("cls")
			os.system("python chai.py")
		if "erase last memory" in kata:
			print("ERASING SOME MEMORY OF ELIZA....")
			time.sleep(2)
			with open("D:\script\PYTHON\chai\history.txt","r+") as jmls:
				dlts=jmls.readlines()
				jmls.seek(0)
				jmls.truncate()
				jmls.writelines(dlts[:-30])
			print("Erase success, restart....")
			os.system("cls")
			os.system("python chai.py")
		if "erase first memory" in kata:
			print("ERASING SOME MEMORY OF ELIZA....")
			time.sleep(2)
			with open("D:\script\PYTHON\chai\history.txt","r+") as jmlsa:
				dlts=jmlsa.readlines()
				jmlsa.seek(0)
				jmlsa.truncate()
				jmlsa.writelines(dlts[-30:])
			print("Erase success, restart....")
			os.system("cls")
			os.system("python chai.py")
		if "show memory" in kata:
			info=open("D:\script\PYTHON\chai\history.txt", "r")
			print("""
+++++++++++++++++++++++++++++++
Information about Eliza Program
+++++++++++++++++++++++++++++++
""")
			print("Loading...", "\r")
			time.sleep(2)
			with info as dia:
				print("Dialogue : "+str(len(dia.readlines())))

			print("All dialogue : \n"+str(tek))
			os.system("python chai.py")

		if "^C" in kata:
			exit()

		data={
"text": str(tek)+"\nMe: "+kata+"\nEliza:",
"temperature": 0.6,
"repetition_penalty": 1.1,
"top_p": 1,
"top_k": 40,
"response_length": 64
}

		send=post(url,headers=head,json=data).text
		print(send)
		get_res=json.loads(send)["data"].strip()
		print("Robot: "+get_res)
		open("D:\script\PYTHON\chai\history.txt","a+").write("\nMe: "+kata)
		open("D:\script\PYTHON\chai\history.txt","a+").write("\nEliza: "+get_res)


except KeyError:
	print("Something wrong!!!Memory Eliza is too much")
	tanya=input("You want erase memory Eliza [y/n] ? ")
	if "y" in tanya:
		print("ERASING SOME LAST MEMORY OF ELIZA....")
		time.sleep(2)
		with open("D:\script\PYTHON\chai\history.txt","r+") as jml:
			dlt=jml.readlines()
			jml.seek(0)
			jml.truncate()
			jml.writelines(dlt[:-30])
		print("Erase success, restart....")
		os.system("cls")
		os.system("python chai.py")
	elif "n" in tanya:
		print("Ok, system canceled")
		os.system("python chai.py")

except KeyboardInterrupt:
	print("\n")
except json.decoder.JSONDecodeError:
	print("Error Internet !! restart script...")
	time.sleep(2)
	os.system("python chai.py")

