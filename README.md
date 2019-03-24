# Spring-Boot-Introduction
Special thanks to Java Brain Youtube Tutorial Series.

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
| Features|  POJOs<br> Dependency Injection<br> MVC<br> Security<br> Integrate with other framework like Hibernate <br> ...| Convention over configuration. On top of Spring framework, help developers solve the additional jar files and configurations, while you can also done manual configuration in `applicatoin.properties` <br><br> Embedded Tomcat server <br><br> ...|

### 0.1 When will you use Spring boot? (https://www.quora.com/What-is-Spring-Framework-used-for)

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

### 2.1 Create Spring Boot Application

- Method 1: Use Intellij IDE

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

## Reference:
1. https://www.quora.com/What-is-Spring-Framework-used-for
