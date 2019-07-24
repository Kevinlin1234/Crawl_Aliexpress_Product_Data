import requests
import numpy as np
import csv
from bs4 import BeautifulSoup
import xlsxwriter
# // headers={
# // 	'authority': 'feedback.aliexpress.com',
# // 	'method': 'GET',
# // 	'path': '/display/productEvaluation.htm?productId=32974045028&ownerMemberId=231326377&companyId=240697559&memberType=seller&startValidDate=&i18n=true',
# // 	'scheme': 'https',
# // 	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
# // 	'accept-encoding': 'gzip, deflate, br',
# // 	'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
# // 	'cookie': 'ali_apache_id=11.227.118.67.1557325977676.193839.3; xman_us_f=x_locale=en_US&x_l=0; intl_locale=en_US; aep_usuc_f=site=glo&c_tp=USD&region=US&b_locale=en_US; xman_f=aHHx/DM17tBQG89cF3dz/m7FVuvWzliG1tfc+o/fbH9rxtmHxRMDDw67Y7/EQ7acXZ2Oj3/UbnQtwoZbyJi/YsWgDrN9y3ZJY4oj7yaDUXbJp5jbkfxsrw==; xman_t=neZDeVkiwzGTzRLOHqwh6OeWtB0W5Pm0vfn+nNC3M+nF/cq5qH0hXI2E09M1yZoS; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%0932974045028; cna=m9ZZFaZCsEgCATLJX/ouEbkM; _ga=GA1.2.988124635.1557325982; _gid=GA1.2.1076998171.1557325982; acs_usuc_t=acs_rt=8f096ae1f62648b89ad20e623daf3714&x_csrf=ta_yelus_qm5; _fbp=fb.1.1557325983118.373660708; AKA_A2=A; intl_common_forever=Q4wHfCBpjR7gP+1qYKx8bUz5c4cwPNksg4xp1wZDx/9V4LOO9tgmsA==; JSESSIONID=D2837BE6E4EEDCB9CEFD640F2F0807F2; ali_apache_track=; ali_apache_tracktmp=; _m_h5_tk=968d637ac4a0eee8d5675943c83c6de6_1557338970180; _m_h5_tk_enc=e2769454ba476e625b3d82d826ddb002; l=bBEjaI_rv0AEqi8LBOCanurza77OSIRYYuPzaNbMi_5C36T_iIbOlKAkLF96Vx5RsZTB4a32vBJ9-etXZ; RT="sl=0&ss=1557337165740&tt=0&obo=0&sh=&dm=aliexpress.com&si=21b4dd22-2517-4623-a5c0-945df3f37034&se=900&bcn=%2F%2F173c5b0d.akstat.io%2F&nu=&cl=1557337171925"; isg=BFdXe5nPx33h9EPwcSmFyp2N5s3F2iXezPZk36mEdSaP2HYasWxlTgq6OwjjUQN2',
# // 	'dnt': '1',
# // 	'referer': 'https://www.aliexpress.com/item/Spring-Ladies-Urban-Chiffon-Loose-Printed-Pleated-Dress-Women-Fashion-Festival-Three-Quarter-Lantern-Sleeves-Knee/32974045028.html?spm=2114.search0103.3.1.40242104GY0Heg&ws_ab_test=searchweb0_0,searchweb201602_1_10065_10130_10068_10890_10547_319_10546_317_10548_10545_10696_453_10084_454_10083_10618_10307_537_536_10059_10884_10887_321_322_10103,searchweb201603_53,ppcSwitch_0&algo_expid=fff350e1-3c8a-4837-a729-02979055d33a-0&algo_pvid=fff350e1-3c8a-4837-a729-02979055d33a&transAbTest=ae803_3',
# // 	'upgrade-insecure-requests': '1',
# // 	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
# // }

class crawl:

	def __init__(self,inputFile,outputFile):
		self.inputFile = inputFile
		self.outputFile = outputFile
		self.urls = []
		self.ids = []
		self.result = [['Product_ID', 'Url', 'Title', 'Category', 'Img']]
	

	def crawl_title_category_pic(self):
		print "Start to crawl aliexpress pages:"
		for i in range(0, len(self.urls)):
			try:
				row = []
				print self.ids[i]
				row.append(self.ids[i])
				row.append(self.urls[i])
				res = requests.get(self.urls[i])
				#print(res)
				soup = BeautifulSoup(res.text, 'html.parser')
				product_name = soup.select('.product-name')[0].text.replace(",","")
				parent_category = soup.select('.ui-breadcrumb > div > a')
				category = soup.select('h2 > a')[0].text
				imgUrl = soup.select('.ui-image-viewer-thumb-frame > img')[0].attrs['src']
				img = requests.get(imgUrl)
				fname = 'f' + str(i)
				with open('./pics/' + str(self.ids[i]) + '.jpg','wb') as fname:
					fname.write(img.content)
				wholeCategory = ''
				for c in parent_category:
					wholeCategory += c.text.replace(",","") + ' > '
				wholeCategory += category.replace(",","")
				row.append(product_name)
				row.append(wholeCategory)
				#row.append(img)
				self.result.append(row)
			except:
				print "Not right!" 

		#print 'product_name' + product_name + '\n' + 'category' + category + '\n' + 'img' + img + '\n'

	def read_from_csv(self):
		with open(self.inputFile) as inF:
			reader1 = csv.DictReader(inF)
			print "Start to build url:"
			for row in reader1:
				productid = row['productID']
				#self.urls.append(url)
				self.ids.append(productid)
				try:
					res = requests.get("https://www.aliexpress.com/item/" + productid + '.html')
					soup = BeautifulSoup(res.text, 'html.parser')
					title = soup.findAll("meta", {"property" : "og:image"})
					part_url = title[0]['content'].split('/')[-1].split('.')[0]
					url = "https://www.aliexpress.com/item/" + part_url +'/' + productid + '.html'
					print url
					self.urls.append(url)
				except:
					print "Id not exist!"

	def write_to_csv(self):
		with open(self.outputFile,'w') as out:
			writer = csv.writer(out)
			for r in self.result:
				writer.writerow(r)

	def write_to_xlsx(self):
		filename = self.outputFile
		workbook = xlsxwriter.Workbook(filename)
		worksheet = workbook.add_worksheet('result')
		for i in range(0,len(self.result)):
			if i != 0:
				worksheet.set_column('E:E',20)
				worksheet.set_row(i,230)
				worksheet.insert_image(i,4,'./pics/'+self.result[i][0]+'.jpg', {'x_scale': 0.2, 'y_scale': 0.2})
			worksheet.write_row(i,0,self.result[i])
			#worksheet.insert_image('M2','screen0.png', {'x_scale': 0.2, 'y_scale': 0.2})
			#worksheet.set_row(i,192)
		#worksheet.insert_image('M2','screen0.png', {'x_scale': 0.2, 'y_scale': 0.2})
		workbook.close()


inputFile = 'crawlData.csv'
outputFile = 'ProductData.csv'

crawl1 = crawl(inputFile,outputFile)
crawl1.read_from_csv()
crawl1.crawl_title_category_pic()
crawl1.write_to_csv()
#crawl1.write_to_xlsx()
#result  = [[]]


#print(soup.select('.ui-tab-pane ui-switchable-panel'))
#print(soup.select('.ui-tab-pane ui-switchable-panel > iframe')[0].attrs['src'].split("?")[1].split("&")[1])
#print(soup.select('.ui-tab-pane ui-switchable-panel > iframe')[0].attrs['src'].split("?")[1].split("&")[2])