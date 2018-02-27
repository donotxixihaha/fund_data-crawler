# Fund_Data-Crawler
##### ------------------------------------------------------Script Specification EN-VERSION 2018/2/28 1:37 GMT（CHN-VERSION IS BELOW）
### __Basic function: Efficiently crawl day-level data of all open-ended funds in China (gain 5M records within 20 minutes)__
### **Future work: data analysis, prediction and find best combinations**
#### Data annotation:view the CHN-VERSION BELOW  
#### Features of the program：
>1.Tor is nat available in Chinese Mainland, so I crawl a proxy website and build an IP proxy pool to prevent anti-crawler in fund site 
 2.Controlling the Chrome automatically to get all fund codes which are dynamically loaded  
 3.Use 8 processes and 4 threads(3 crawl threads and 1 store data thread）, the speed increase 20 times, which makes it possible to acquire 5 million records from 6600+ funds of 8 types within 1300 seconds.  
 4.You can choose to store in local Mysql server.  
 5.In the very beginnig, you should use test_multi-core&multi-threads.py and multi-threading test.py to test whether your IDE supports multi-process and multi-threads. e.g. Spyder is no tvery supportive.  

#### Before start, you have to install：
>1.windows10 + python3 + IDE(PyCharm recommended)  
2.all packages that will be used, including：beautifulsoup4,selenium,chardet,requests,MySQLdb,sqlalchemy,multiprocessing,queue,threading   
3.Chrome browser, selenium driver of chrome, and set path in enviroment variable: see https://www.seleniumhq.org/docs/03_webdriver.jsp  
4.MySQL5.7 and upper version, create new account, or data would be saved in disk D 

#### Functions and alterable parameters of every script：
>**1.CodeCollector.py：**  
>>* ***Function***：use selenium to control Chrome automatically, gain all codes of 8 types of open-ended fund in China
>>* ***Alterable parameter***：you have to give the install content of selenium.exe in line 21  

>**2.IPPool.py:**   
>>* ***Function***：crawl highly anonymous proxy address in www.xicidaili/nn and select super ones due to test, then built proxy pool and save it as .npy  
>>* ***Alterable parameter***：you can change saving address in line 67, or the proxy pool.npy will be saved at D:// defaultly  
 
>**3.HistoryDataCollector.py:**  
>>* ***Function***：crawl all day-level data according to the fund code, from establishing day to present. proxy is chosen randomly from proxy pool, requests header is Chrome browser  
>>* ***Alterable parameter***：if you change saving address in IPPool.py, you have to give that address to line 18.  

>**4.DataSaver.py:**  
>>* ***Function***：save data to MySQL server or D:\\
>>* ***Alterable parameter***：alter MqSQL account information in line 20、23, and directly saving content in line 29    

>**5.test_multi-core&multi-threads.py and multi-threading test.py**:    
>>* ***Function***：test whether current IDE support multi-process and multi-thread. If nothing is printed, the result is negative and you cannot run SumUpManager.py directly. you need to modify, see 6.SumUpManager.py 
>>* ***Alterable parameter***：none  

>**6.SumUpManager.py**:  
>>* ***Function***：main script, use 8 processes and 4 threads to put all scripts together, use message queue to manage shared recourses  
>>* ***Alterable parameter***：if you wan to save data to mysql, alter line 50、51; if you wan to store data butnot in D:\\, alter line83-90; if test in 5 show a non-supportive result, annotate line 16-103 , run line107-133, the serial process main last for 300 minutes.

### Using approach：
Save all the scripts into same contents, install necessary packages and modify due to declarations above. Then run main script SumUpManager.py, wait for approximate 20 minutes  

#### -------------------------------------------------------------------------------------脚本说明中文版 2018/2/28 1:37 GMT
### 基本功能：高效抓取中国所有开放式基金日级别数据（20分钟内抓取5000000条记录）
### 未来工作：数据预测、分析、最优组合
#### 数据说明：
>**fund_data&part1.rar:** ***mix:混合型基金;  LOF:上市型开放式基金;  FOF:专门投资于其他证券投资基金的基金***  
**fund_data&part2.rar:**  ***stock:股票型基金;  all_index:指数型基金;  bond:债券型基金;  ETFlink:投资于ETF基金的基金;  QDII:合格境内机构投资者基金***

#### 脚本特色：
>1.由于大陆无法使用Tor代理，从xicidaili爬取代理，筛选多个优质高匿代理建立代理池，防止反爬虫    
 2.自动操控Chrome浏览器，获取所有动态加载的开放式基金的代码  
 3.采用8进程4线程（3个线程抓取基金数据+1个线程将数据存盘），运行速度提升2000%，1300秒内运行完毕，获取8个种类6600+基金的5000000条记录  
 4.保存到本地MySQL服务器  
 5.使用前请先运行test_multi-core&multi-threads.py测试IDE是否支持多进程与多线程，如：Spyder的支持存在问题，PyCharm正常运行  

#### 在运行脚本前，需要安装：
>1.windows10 + python3 + IDE（推荐pycharm） 
2.所有要使用的包，包括：beautifulsoup4,selenium,chardet,requests,MySQLdb,sqlalchemy,multiprocessing,queue,threading  
3.chrome浏览器，selenium的chrome驱动并配置环境变量，见https://www.seleniumhq.org/docs/03_webdriver.jsp  
4.MySQL5.7以上版本并建立新账户，否则数据将直接保存到D盘  

#### 各脚本功能与可调参数说明：
>**1.CodeCollector.py**：  
>>* ***功能***：使用selenium动态操控Chrome浏览器，获取8种开放式基金下属全部基金的代码  
>>* ***参数***：在line21中将地址改为自己的selenium安装地址  

>**2.IPPool.py**:  
>>* ***功能***：请求，解析并筛选www.xicidaili/nn上的高匿代理，建立代理池，以.npy格式存盘  
>>* ***参数***：在line67中可更改存盘地址，否则默认将代理池文件存盘到D根目录  

>**3.HistoryDataCollector.py**:  
>>* ***功能***：根据基金代码获取该基金成立以来的全部日数据，代理从代理池中随机获取，请求头为Chrome浏览器  
>>* ***参数***：若在IPPool中修改了存盘地址，需将line18处地址改为一致地址  

>**4.DataSaver.py**:  
>>* ***功能***：将HistoryDataCollector获取的基金数据文件存盘到本地数据库，或直接存到本地D盘fund_data目录  
>>* ***参数***：在line20、23中修改个人数据库信息，或在line29修改存到本地的目录  

>**5.test_multi-core&multi-threads 和multi-threading test.py**:    
>>* ***功能***：测试当前使用的IDE是否支持多进程和多线程。观察输出可知结果。若不支持则不能运行主脚本SumUpManager.py，需要修改，具体见6  
>>* ***参数***：无  

>**6.SumUpManager.py**:  
>>* ***功能***：主脚本，以8进程4线程的方式整合所有其他脚本，用消息队列控制线程的共享资源  
>>* ***参数***：若要存到数据库，修改line50、51；若要修改本地文件保存目录，修改line83-90；若5中测试不通过，注释line16-103，恢复line107-133，串行运行可能会花费300分钟左右  

### 使用方法：
将所有脚本保存到同一目录，按上述说明修改参数，安装包和驱动等，然后直接主脚本SumUpManager.py，等到20分钟左右完成
