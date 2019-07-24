1. Log into Aliexpress account to get cookie, update to cookie.txt file
2. Run python crawl_Aliexpress_threading.py
3. Download tomcat 8.5
4. In the tomcat folder: conf->server.xml add section:
 <Context path="/alishow" docBase="/Users/apple/Desktop/Alishow/Web" debug="0" privileged="true" reloadable="true"></Context>
 More details: https://blog.csdn.net/jq_ak47/article/details/70667608
5. go to tomcat -> bin -> run ./startup.sh
6. In the browser localhost:8080/alishow to show the crawled data in the website
