# Spring-Boot-Introduction

## Agenda
0. Spring Boot Basics
1. Hibernate Basics
2. Set Up
3. Build a Spring boot applicaton with MySQL database together!

## 0. Spring Boot Basics

### 0.0 Comparision between Spring and Spring boot

|  | Spring | Spring boot|
| ------------- | ------------- | ------------- |
| Definition|  huge Enterprise Java Framework | bootstrap a standalone, producation-grade Spring application that can be easily run|
| Features|  POJOs<br> Dependency Injection<br> MVC<br> Security<br> Integrate with other framework like Hibernate <br> ...| Convention over configuration. On top of Spring framework, help developers solve the additional jar files and configurations, while you can also done manual configuration in `src/main/resources/applicatoin.properties` <br><br> Embedded Tomcat server <br><br> ...|

### 0.1 When will you use Spring boot?

- [ ] Develop web application.

- [x] Send data to Front-end via RESTful API.
  - RESTful API: An application program interface (API) that uses HTTP requests to GET, PUT, POST and DELETE data.

- [ ] Security solution to web application.

- [x] Communicate with database.

- [ ] Integrate with external resources.

### 0.2 Important Concept

- POJO: Plain Old Java Object. An ordinary Java object. [For more information](https://www.geeksforgeeks.org/pojo-vs-java-beans/)

| POJO | Java Bean |
| ---- | ----- |
| E.g `public class Employee { … }` | E.g  `public class GFG extends javax.servlet.http.HttpServlet { … } `|
| Not all POJOs are Java Beans | All Java Beans are POJOS |


- MVC: Model-View-Controller (MVC). An architectural pattern.
![](https://github.com/LiMengyang990726/Spring-Boot-Introduction/blob/master/images/MVC.png)

- Tomcat:
  - A combination of HTTP server and servlet container.
  - Work with HTTP Protocol. (Thus, the default port number will be 8080)

- Servlet:

- Dependency Injection: Details will be talked with the hands-on coding part.

## 1. Hibernate Basics

### 1.0 What is Hibernate? (http://hibernate.org/orm/what-is-an-orm/)

An object-relational mapping tool for the Java programming language.

Using Hibernate ORM will help your application to achieve Data Persistence.

### 1.1 What is ORM?

A way to leverage SQL in other programming languages.

Example:

| SQL | Hibernate ORM |
|-----| --------------|
| CREATE TABLE product | @Entity<br>@Table(name = "product")<br>public class Cart { … } |

## 2.Set Up

### 2.0 Environment Requirement

- Java 8 SDK
- A Java IDE that you are comfortable to work with.
- [Postman](https://www.getpostman.com/downloads/)

### 2.1 Create Spring Boot Application (Enable Maven Auto-import)

- **Suggested** Method 1: Use [Intellij IDE](https://www.jetbrains.com/idea/download/#section=mac)

![](https://github.com/LiMengyang990726/Spring-Boot-Introduction/blob/master/images/Step1.png)

![](https://github.com/LiMengyang990726/Spring-Boot-Introduction/blob/master/images/Step2.png)

![](https://github.com/LiMengyang990726/Spring-Boot-Introduction/blob/master/images/Step3.png)

- Method 2: Use Eclipse IDE

![](https://github.com/LiMengyang990726/Spring-Boot-Introduction/blob/master/images/EStep1.png)

![](https://github.com/LiMengyang990726/Spring-Boot-Introduction/blob/master/images/EStep2.png)

![](https://github.com/LiMengyang990726/Spring-Boot-Introduction/blob/master/images/EStep3.png)

Add the following codes to your `pom.xml` under the first hierarchy
```
<parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.1.3.RELEASE</version>
        <relativePath/> <!-- lookup parent from repository -->
</parent>

<dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-devtools</artifactId>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
 </dependencies>
 ```

- Method 3: [Download from Spring Boot Website](https://start.spring.io/)
![](https://github.com/LiMengyang990726/Spring-Boot-Introduction/blob/master/images/IStep1.png)

### 2.2 Set Up MySQL database

- For Windows
  - [Download MySQL Community Server](https://dev.mysql.com/downloads/mysql/). Please download the `zip` file.
  
  ![](https://github.com/LiMengyang990726/Spring-Boot-Introduction/blob/master/images/MySQLWindows.png)
  
  ![](https://github.com/LiMengyang990726/Spring-Boot-Introduction/blob/master/images/MySQL1.png)
  
  - Unzip the `tar.gz` to a directory. E.g. C:\SpringBootIntroduction
  
  - Open CMD. Type in the followings:
  ```
  //assume in C folder already
  cd \SpringBootIntroduction\mysql\bin
  
  // Initialize the database. Create a root user with random password. Show the messages on console
  mysqld --initialize --console
  ...
  ...A temporary password is generated for root@localhost: xxxxxxxx // take note of this password, if forget, delete and unzipped folder, unzip it, and repeat the above steps
  ```
  - To start the server:
  ```
  //assume in C folder already
  cd \SpringBootIntroduction\mysql\bin
  
  mysqld --console
  ```
  - To shut down the server: Ctrl+C
  
  - To start a 'Client'
  ```
  cd \SpringBootIntroduction\mysql\bin
  mysql -u root -p
  Enter password:   // Enter the root's password set during installation.
  Welcome to the MySQL monitor.  Commands end with ; or \g.
  Your MySQL connection id is 1
  Server version: 8.0.xx
  Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

  mysql>
  ```
  
- For MacOS.
  - [Download MySQL Community Server](https://dev.mysql.com/downloads/mysql/). Please download the `dmg` file.
  
  ![](https://github.com/LiMengyang990726/Spring-Boot-Introduction/blob/master/images/MySQLMac.png)
  
  ![](https://github.com/LiMengyang990726/Spring-Boot-Introduction/blob/master/images/MySQL1.png)
  
  -  Follow [this](https://dev.mysql.com/doc/refman/8.0/en/osx-installation-pkg.html). Basically just open the dmg and follow the instruction. Take note of the password!!
  
  - It will be installed in `/usr/local/mysql`
  
  - To start and shutdown the server: 
  
  ![](https://github.com/LiMengyang990726/Spring-Boot-Introduction/blob/master/images/MySQLMac1.png)
  
  ![](https://github.com/LiMengyang990726/Spring-Boot-Introduction/blob/master/images/MySQLMac2.png)
  
  - To start a 'Client':
  ```
  cd /usr/local/mysql/bin
  ./mysql -u root -p
  Enter password:   // Enter the root's password given during installation. You will NOT any * for maximum security
  Welcome to the MySQL monitor.  Commands end with ; or \g.
  ......
  mysql>
  ```
  
- For [Ubuntu](https://www.ntu.edu.sg/home/ehchua/programming/howto/Ubuntu_HowTo.html#mysql).

### 2.3 Connect MySQL Database to Spring Boot project via Hibernate

- Step 1: Open `File/Project Structure` in Intellij

![](https://github.com/LiMengyang990726/Spring-Boot-Introduction/blob/master/images/Hibernate1.png)

![](https://github.com/LiMengyang990726/Spring-Boot-Introduction/blob/master/images/Hibernate2.png)

- Step 2: Open `Database` on the right-hand side tool bar

![](https://github.com/LiMengyang990726/Spring-Boot-Introduction/blob/master/images/Hibernate3.png)

![](https://github.com/LiMengyang990726/Spring-Boot-Introduction/blob/master/images/Hibernate4.png)

![](https://github.com/LiMengyang990726/Spring-Boot-Introduction/blob/master/images/Hibernate5.png)

![](https://github.com/LiMengyang990726/Spring-Boot-Introduction/blob/master/images/Hibernate6.png)
  
![](https://github.com/LiMengyang990726/Spring-Boot-Introduction/blob/master/images/Hibernate7.png)

**We are good to go!**

## 3. Build a Spring boot applicaton with MySQL database together!

### 3.1 Goals

- (GET) Retreive products according to catagory 

- (POST) Add new products

- (PUT) Update product information

- (DELETE) Delete products

- (Relational Database) Retreive all products that a merchant has

### 3.2 File Structure (Good Software Engineering Practice Suggestion)

![](https://github.com/LiMengyang990726/Spring-Boot-Introduction/blob/master/images/fileStructure.png)

## Reference:
1. https://www.quora.com/What-is-Spring-Framework-used-for
2. https://www.ntu.edu.sg/home/ehchua/programming/sql/MySQL_HowTo.html
3. [Java Brains Youtube Tutorial Series](https://www.youtube.com/watch?v=bDtZvYAT5Sc&list=PLqq-6Pq4lTTbx8p2oCgcAQGQyqN8XeA1x&index=8)
4. [Telusko Youtube Tutorial Series](https://www.youtube.com/watch?v=Ch163VfHtvA)
