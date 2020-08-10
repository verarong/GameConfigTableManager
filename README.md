# GameConfigTableManager
通过脚本将excel策划表一键部署至服务端mongodb，并生成json文件、类文件供客户端(如cocoscreator)使用


# 策划表管理痛点：

a.一张excel多个sheet

b.双端均需要管理配置表，且格式不同

c.git类不支持excel的版本控制

d.双端热更需求


# 解决方案：

a.基于pandas的excel全表全sheet读取

b.通过apply方法生成对应格式

c.通过excel配置version的sheet，来管理版本号及是否需要更新

d.后端存储至mongo，game内实现hot_refresh方法，用于配置表全局变量自mongo读取更新；前端讲生成的json等文件放置于cdn，客户端重启时对比更新


# 效果示意：
![](http://www.weikunt.cn:7788/selif/hn4x8sgv.png)
![](http://www.weikunt.cn:7788/selif/wsfj8nf0.png)
![](http://www.weikunt.cn:7788/selif/nrdmkeik.png)