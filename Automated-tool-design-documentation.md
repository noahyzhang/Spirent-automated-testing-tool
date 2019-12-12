# 自动化工具设计文档

### 1、系统总体描述

##### 1.1 需求分析

- 在评测一款视频会议软件的时候，我们需要一个更加专业的角度通过不同的维度去评测这款软件在传输视频或者其他方面是否有良好的性能。比如：我们的帧率、抖动度、丢包率等等。
- 因此我们使用思博伦机器在流畅度、全参考模式、无参考模式三种模式下，来评测传输视频过程中的性能问题

- 在使用思博伦工具对软件进行打分的时候，操作步骤过于繁琐，不适合不熟悉思博伦机器的人员使用，并且对于使用的人员费时费力，因此设计自动化工具帮助我们更好更快的使用思博伦机器进行软件测试。

##### 1.2 软硬件基础

- 硬件：思博伦机器、用于测试的PC、用来控制思博伦的PC、ATC网损设备
- 软件准备：python解释器、Spirent Umetrix Video、ATC网损设备API 和 思博伦机器的API

##### 1.3 功能设计

- 由于思博伦现提供的API 只有无参考模式的，因此我设计了无参考模式的自动化工具。
- 其次，在进行无参考模式的评估过程中，会采集到评测视频，因此我们可以借助无参考评测视频来进行全参考模式的评估，因此我设计了全参考模式下的半自动化工具。

### 2、系统体系结构

#####  2.1 整体框架图
![https://gitdojo.gz.cvte.cn/zhangyi/spirent-automated-testing-tool/raw/master/Image/Overall_framework.png]
- 大概解释一下，PC1和PC2是一组，PC3和PC4是一组。他们分别有发送端和接收端，都连接在ATC网络上。控制思博伦工具的PC 也连接在ATC网络上。并且PC1、PC2、PC3、PC4上分别运行一个server，用来获取ATC网络的token。控制思博伦工具的PC 有一个client，用来拿到token，之后进行控制他们的网损。
- 脚本运行在Spirent PC上，当设置好网损之后，进行配置思博伦软件的环境。就绪之后就可以测试了。

##### 2.2 ATC网损设置模块

- 完成的功能：通过ATC网络中Spirent PC 来控制测试PC 的网损。
- 实现
  1. 我们在测试PC 上运行一个服务器，用来拿到测试PC的token值。只需要向 http://192.168.10.1:8000/api/v1/token/  发送GET请求即可拿到token值。
  2. 在Spirent PC 上向测试PC 发送请求，拿到测试PC 的token值。接下来 向 http://192.168.10.1:8000/api/v1/auth/192.168.xx.xx/ (后面跟的是测试PC的IP) 发送POST报文，在body上带上token值。成功之后便可以控制测试PC。
  3. 最后我们就可以设置测试PC 的网损了。只需要向 http://192.168.10.1:8000/api/v1/shape/192.168.xx.xx/ (后面跟的是测试PC 的IP)，发送POST报文，在body 上带上需要设置的网损的值。就可以正确的设置了。

##### 2.3 Spirent 设置模块

- 完成的功能：完成思博伦工具的操作
- 实现
  1. 我所用到的思博伦工具的API 的解释我放在了附录1中了。
  2. 进入Spirent Umetrix Video软件的Setting中，选择无参考模式，并且设置参数。
  3. 进入软件的 Capture中，进行设置测试过程中一些参数，然后就可以启动
  4. 进入软件的Review 中，将Unprocessed 中的 sessions 进行proess。
  5. 最后Review中，将processed中sessions导出来就OK 了。

### 3、系统操作说明
- **详细的操作请查看README.md。**

##### 3.1 无参考模式操作过程

1. 在测试机器上直接运行 dist 目录下的 set_testPC_atc_server.exe。不用输入，端口号默认是8888。
2. 在测试机器上打开 cmd 运行 ipconfig ，得到测试机器的IP。
3. 注意：由于ATC路由器出口只有三个，因此我们在测试时，可以先测两对测试机器发送端的上行网损，后面在测接收端的下行网损。
4. 接下来就可以在一对测试 PC 之间打开云会议或者teams，进行共享桌面或者视频会议。
5. 接下来需要设置我们要测试的网损case。我们新建一个execl表格，如下图所示，按照下图格式来填写数据。第一列'session_name'是生成结果报告的execl 命名。up_bandwidth是上行带宽，up_delay 是上行延时，up_jitter是上行抖动，up_loss是上行丢包率，意down开头的是下行的参数。
  - 注意：session_name名字不可以相同。
![https://gitdojo.gz.cvte.cn/zhangyi/spirent-automated-testing-tool/raw/master/Image/case_atc_execl.png]
- 再SpirentPC 上启动 Spirent Umetrix Video.
- 接下来我们就可以在Spirent PC 上启动脚本。需要我们输入几个数值。帧率、测试时长（分、秒）、两台测试PC的 IP 和port、存放case的execl 表格的地址、结果报告导出的位置地址、用于全参考所采集的视频地址（注意：这两个地址的分隔符必须是双斜杠）。
- 启动之后我们就可以在一边喝茶了，结果报告execl会自动生成到自己填的位置。

##### 3.2 全参考模式操作过程

- 由于思博伦工具并没有提供全参考模式下的API，因此我们的全参考模式测试只能是半自动化工具。半自动化程度到我可以拿到所采集的视频，用来和原视频进行比对。
- 因此我们不用做任何操作，当无参考模式自动化工具跑完之后，会自动生成一个文本文件，里面存放的是我们采集到的视频，可以用来在全参考模式下的算法比对。

### 4.系统设计总结

##### 4.1 系统完成程度

- 设计的无参考模式下的自动化工具进行测试之后，没有出现什么问题。
- 半自动化的全参考模式下的自动化工具，半自动化程度到我可以拿到采集出来的视频，然后接下来和原视频比对的工作我们需要自己操作。

### 附录1

### Settings

| 功能                                        | 方法 | 解释                                                         |
| ------------------------------------------- | ---- | ------------------------------------------------------------ |
| Get parameters                              | GET  | 得到setting中的无参考界面内容，除了non_reference_real_time,（实时的勾选） |
| Set the respective Non Reference parameters | PUT  | 设置setting中无参考界面内容，除了non_reference_real_time，（实时的勾选） |

### System

| 功能                               | 方法 | 解释                                                         |
| ---------------------------------- | ---- | ------------------------------------------------------------ |
| Gets the currently set methodology | GET  | 得到当前的设置。比如：无参考以及对应的methodology的id，或者实时无参考以及对应的methodology的id |
| Sets current methodology           | PUT  | 设置模式，可选的有无参考、实时无参考、无参考4K，实时无参考4K。 |

### Methodologies

| 功能             | 方法 | 解释                                      |
| ---------------- | ---- | ----------------------------------------- |
| list methodology | GET  | 可以得到不同的模式所对应的methodology的id |

### Channel

| 功能                                   | 方法 | 解释                                                         |
| -------------------------------------- | ---- | ------------------------------------------------------------ |
| List channels information              | GET  | 通过methodology的id可以得到已开启的通道的info                |
| Enable channel                         | PUT  | 开启某一个通道，并且设置Video Device和Audio Device           |
| Disable channel                        | PUT  | 关闭某一个通道。channel Index中 1 代表A通道，2代表B通道。    |
| Configure channel                      | PUT  | 设置通道上的内容                                             |
| Set channel's buffering window profile | PUT  | 调节无参考模式上buffering window 上的窗口。（没有用到）      |
| Is Channel Ready                       | GET  | 判断通道是否开启，如何有一个以上开启，就显示true，全部关闭才会显示false |

### Sessions

| 功能                         | 方法 | 解释                                                         |
| ---------------------------- | ---- | ------------------------------------------------------------ |
| List sessions                | POST | 拿到Processed或者UnProcessed的session的信息。包括sessionID、description、folderpath等等 |
| Get Session                  | GET  | 可以根据某一个具体的SessionID得到具体某一个session的具体信息 |
| Start Session                | POST | 开始测试，其中的description 是 SessionName，后面是时间，还有一个是否测试完就自动 process |
| Stop session                 | PUT  | 停止测试。                                                   |
| Cancel session processing    | PUT  | 取消一个session的 process，需要SessionID。                   |
| Get Session KPIs             | GET  | 只能用于实时无参考模式，可以得到session KPIs                 |
| Process Unprocessed Sessions | PUT  | 开始process 一个unprocessed Session。需要session，可以多填几个。（和上一个PUT对应） |
| Get Session Report           | GET  | 得到session 的报告，就是session的信息。需要输入一个session的folderpath路径。（可不用） |
| Create Session Report        | POST | sessionID填我们需要用的sessionID，destinationPath就是想要存的地方，这是一个目录，会把文件按照当初命名的名字保存下来。 |
| Import Session               | POST | 导入一个session。在unprocessed界面的Add中是Add existing session。路径是就是sessionPath |
| Permanently delete a session | PUT  | 在unprocessed界面Discard选项。意思是永久删除一个session。里面填的是sessionID。 |
| Remove a list of sessions    | PUT  | 移除 unprocessed 或者 processed 中 的session。需要填的是sessionID。 |
| Import Video                 | POST | 导入视频。在unprocessed中Add的Import Video file。 需要填的是videoFilePath，主要是双斜杠。 |
| Mark Session as Processed    | PUT  | 在 unprocessed 中 Mark as Processed。功能是标记unprocessed Session为processed Session。需要填的是sessionID。 |
| Mark Session as Unprocessed  | PUT  | 在processed中Mark as Unprocessed。功能是标记Unprocessed Session 为 Unprocessed Session。需要填的是SessionID。 |