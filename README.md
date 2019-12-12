# Spirent automated testing tool

Video conference software in different network loss, in the case of spirent no reference mode of an automated test tool.

## 详细的操作步骤
- 首先，先诠释几个硬件的简称。4台用来测试的机器PC1、PC2、PC3、PC4。PC1和PC2是一组，PC1是发送端，PC2是接收端。PC3和PC4类同。
- 用来控制思博伦机器的PC我们称为SpirentPC。这五台PC都接在ATC网络中，用来设置发送端（上行）或者接收端（下行）的网损，SpirentPC接在ATC网络中用来控制四台测试机器。

##### 项目目录结构

- Image目录是存放图片的，这些图片使用在项目的介绍文档中
- dist目录放的是可执行文件，分别是运行在测试机器P1--P4上的`set_testPC_atc_server.exe`。还有一个是运行在SpirentPC上的`main.exe`。
- `Automated-tool-design-documentation.md`是项目的设计文档，如果要深究项目，建议阅读。
- `README.md`是具体的操作操作步骤，和项目目录的简单介绍。
- `atc.py`封装的类主要功能向测试机器运行的HTTP服务器发送GET请求，获取它的token值，从而控制测试机器的网损。
- `execl.py`是用来操作execl的，包括提取存放不同case的函数，还有导出最终execl报告的类。
- `spirent.py` 封装了操作Spirent机器API的类，用来控制思博伦机器。
- `main.py`将所有不同模块的类融合在一起，实现整个项目文件的统一调配。
- `set_testPC_atc_server.py`的功能是给测试机器提供一个HTTP服务，用来获取本机连接在ATC网络上的token值。

##### 测试机器配置

- 将dist目录里 `set_testPC_atc_server.exe`可执行文件拷贝到测试机器PC1-PC4。在测试机器上直接双击运行，便可开启HTTP服务。(注意：端口默认是8888)
- 打开测试机器的cmd窗口，输入`ipconfig`得到测试机器的IP。

- 注意：ATC网络路由器只有3个口，而我们测试的时候，最好使设置网损的机器使用宽带，不使用wifi。
- 因此我们一般使PC1、PC3连接ATC网络，设置上行网损，进行测试。测试完成之后，使PC2、PC4连接ATC网络，设置下行网损，进行测试。
- 接下来，测试机器打开视频会议软件，进行播放视频或者桌面共享。

##### SpirentPC机器配置

- 在spirentPC上打开 Spirent Umetrix Video 软件。

- 将dist目录里的`main.exe`可执行文件拷贝到SpirentPC上，在SpirentPC上直接双击运行，便可开始自动化脚本的的运行。
- 需要输入一些参数
  - 帧率：测试视频的帧率
  - 测试时间（分、秒）：需要测试多长时间
  - 两对测试机器运行的HTTP服务的IP：用来控制测试机器
  - 存放网损case的execl文档路径(例: “C:\\\Users\\\SPIRENT\\\Desktop\\\test.xlsx”)
  - 生成最终报告的路径(是目录，例: "C:\\\Users\\\SPIRENT\\\Desktop\\\11-15")
  - 采集到的视频的存放路径(例如:"C:\\\Users\\\SPIRENT\\\Desktop\\\test_video_path.txt")
  - **注意：这几个路径分隔符必须是双斜杠**
- 当自动化脚本退出时，报告生成结束。

##### 结果

- 无参考模式打分：我们在最终生成报告的路径下，就可以看到不同case的execl表。并且我将这些execl表的有效提取出去放在这个目录下的res.xlsx表中了。更加方便参考。
- 全参考打分：如果我们需要做全参考模式，就可以在采集的视频的存放路径中找到视频的路径，用来做全参考模式的打分。

