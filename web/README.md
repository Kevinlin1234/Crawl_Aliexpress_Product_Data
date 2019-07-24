1. 登陆个人Aliexpress账号得到cookie 更新到 cookie.txt 文件中
2. Run python crawl_Aliexpress_threading.py
3. Download tomcat 8.5
4. In the tomcat folder: conf->server.xml add section:
 <Context path="/alishow" docBase="/Users/apple/Desktop/Alishow/Web" debug="0" privileged="true" reloadable="true"></Context>
 更详细的查看: https://blog.csdn.net/jq_ak47/article/details/70667608 中 section: "server.xml文件中配置"
5. go to tomcat -> bin -> run ./startup.sh
6. 浏览器输入 localhost:8080/alishow 注意这里的path 和上面的 path="/alishow" 是一致的
