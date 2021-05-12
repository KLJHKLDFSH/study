### Swagger

#### 是什么？

- 生成API文档的工具
- 

#### springfox-swagger

- spring 集成了swagger，API还是由swagger生成



### 使用

1. pom 引入依赖。

   ```xml
   <denpendency>
   	<g>io.springfox</g>
   	<a>springfox-swagger2</a>
   </denpendency>
   <denpendency>
   	<g>io.springfox</g>
   	<a>springfox-swagger-ui</a>
   </denpendency>
   ```

2. Java配置

   ```java
   @AutoConfigration
   @EnableSwagger2
   public class Config{
   	
   	@Bean
   	public Docket create(){
   			return Docket();
   	}
   
   }
   ```

3. 使用Java 注解。

   ```txt
   在Controller中添加注解
   
   ```

   

   - @ApiModel  针对Model属性注解
   - @ApiOpration

   - @ApiModelProperties

4. 访问localhost:port/path/swagger-ui.html

5. plugin 使用

   添加swagger2markup-maven-plugin

   通过执行maven plugin 命令生成

   可以生成各种格式的API文档



### 原理

