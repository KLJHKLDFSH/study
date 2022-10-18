Spring boot 集成 mybatis

1. 添加依赖包

   ```xml
   <dependency>
       <groupId>mysql</groupId>
       <artifactId>mysql-connector-java</artifactId>
       <version>8.0.18</version>
   </dependency>
   <dependency>
       <groupId>com.baomidou</groupId>
       <artifactId>mybatis-plus-boot-starter</artifactId>
       <version>${baomidou.version}</version>
   </dependency>
   
   ```

2. 配置数据源

   ```yaml
   # Mysql数据库
   spring:
     datasource:
       driver-class-name: com.mysql.cj.jdbc.Driver
       url: jdbc:mysql://localhost:3306/test?autoReconnect=true&useUnicode=true&characterEncoding=utf8&zeroDateTimeBehavior=CONVERT_TO_NULL&useSSL=false&serverTimezone=CTT
       username: root
       password: abc@1235
       # 连接池大小根据实际情况调整
       max-active: 20
       max-pool-prepared-statement-per-connection-size: 20
   
   ```

3. 创建 Model 

   ```java
   //省略了get set
   public class User {
       private Long id;
       private String name;
       private Integer age;
       private String email;
   }
   ```

4. 创建 mapper接口

   ```java
   public interface UserMapper extends BaseMapper<User> {
   
   }
   ```

5. 在配置类中添加@mappersan用于扫描mapper接口

   ```java
   @MapperScan("com.example.demo.db.mapper")
   ```

6. 分页

   1. 配置

      ```java
      //配置 MybatisPlusInterceptor 
      @Bean
      public MybatisPlusInterceptor mybatisPlusInterceptor() {
          MybatisPlusInterceptor interceptor = new MybatisPlusInterceptor();
          interceptor.addInnerInterceptor(new PaginationInnerInterceptor(DbType.MYSQL));
          return interceptor;
      }
      ```

   2. 使用

      ```java
      
      // BaseMapper 中提供的方法使用 Page 对象分页
      // IPage 的默认实现是 Page
      IPage<UserVo> selectPageVo(IPage<?> page, Integer state);
      // or (class MyPage extends Ipage<UserVo>{ private Integer state; })
      MyPage selectPageVo(MyPage page);
      // or
      List<UserVo> selectPageVo(IPage<UserVo> page, Integer state);
      ```

7. 自定义接口

   1. 添加接口方法
       ```java
       public interface UserMapper extends BaseMapper<User> {
        //在 接口 中添加方法
           List<User> selectByName(IPage<User> page , String name);
       }
       ```
       
   2. 在创建mapper对应的 xml文件，xml文件默认保存在 resources/mapper 文件夹下

       ```xml-dtd
       <?xml version="1.0" encoding="UTF-8"?>
       <!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
       <mapper namespace="com.example.demo.db.mapper.UserMapper">
       
           <select id="selectByName" resultType="com.example.demo.db.model.User">
               select * from user where name = #{name}
           </select>
       </mapper>
       
       ```

       

   