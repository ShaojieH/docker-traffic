### docker-spark集群的流量采集与控制



![1](./misc/image/1.png)

由gettyimages/spark构建的spark docker集群，由1个master与3个worker组成。图为该集群每30s运行一次javaTC任务时的流量折线图，蓝色为master。监控程序汇总每秒各个节点的入(?)流量并上报。