# ClassLoader

## 作用

- 负责把`.class` 文件加载到jvm内存中，并生成`java.lang.Class`类的一个实例。

- 负责加载java应用所需要的资源，图像文件和配置文件等。

## 分类

- Java内建
  - BootStrap ClassLoader
  - Platform ClassLoader(java 11)
    - java se 平台
    - jdk runtime 
  - System ClassLoader
- 自定义（继承 ClassLoader）