# Spring-Boot-Introduction

## Agenda
0. Spring Boot Basics
1. Hibernate ORM Basics
2. Set Up
3. Build a Spring boot applicaton with MySQL database together!

## 0. Spring Boot Basics

### 0.0 Why Java?

![](https://github.com/LiMengyang990726/Spring-Boot-Introduction/blob/master/images/trending.png)

### 0.1 Comparision between Spring and Spring boot

|  | Spring | Spring boot|
| ------------- | ------------- | ------------- |
| Definition|  huge Enterprise Java Framework | bootstrap a standalone, producation-grade Spring application that can be easily run|
| Features|  - POJOs<br> - MVC<br> Dependency Injection<br> - Testing <br> - Dependency Injection <br> - Security <br>...| - Convention over configuration. <br> - Embedded Tomcat server <br> <br><br> ...|

### 0.2 When will you use Spring boot?

- [ ] Develop web application.

- [x] Send data to Front-end via RESTful API.
  - RESTful API: An application program interface (API) that uses HTTP requests to GET, PUT, POST and DELETE data.

- [ ] Security solution to web application.

- [x] Communicate with database.

- [ ] Integrate with external resources.

### 0.3 Important Concept

- POJO: Plain Old Java Object. [For more information.](https://www.geeksforgeeks.org/pojo-vs-java-beans/)

| POJO | Java Bean |
| ---- | ----- |
| No `extends` <br> No `implements` <br> No prespecified annotation <br> |  |
| Not all POJOs are Java Beans | All Java Beans are POJOS |

POJO example:

```
@Component
public class ExampleListener {

    @JmsListener(destination = "myDestination")
    public void processOrder(String message) {
        System.out.println(message);
    }
}
```

Java Bean example:

```
public class ExampleListener implements MessageListener {

    public void onMessage(Message message) {
        ...
    }

}
```

- MVC: Model-View-Controller architecture(MVC).
![](https://github.com/LiMengyang990726/Spring-Boot-Introduction/blob/master/images/MVC.png)

- Dependency Injection: Details will be talked with the hands-on coding part.

- Tomcat: A Java-capable HTTP Server

- HTTP Server: A piece of software that understands URLs and HTTP protocol.


## 1. Hibernate ORM Basics

### 1.0 Hibernate

Hibernate is a high-performance object/relational persistence and query service.

### 1.1 ORM

A way to leverage SQL in other programming languages.

Example:

| SQL | Hibernate ORM |
|-----| --------------|
| CREATE TABLE product | @Entity<br>@Table(name = "product")<br>public class Cart { … } |

### 1.2 What is Hibernate ORM? (http://hibernate.org/orm/what-is-an-orm/)

An object-relational mapping tool for the Java programming language.

Using Hibernate ORM will help your application to achieve Data Persistence.


## 2.Set Up

### 2.0 Environment Requirement

- Java 8 SDK
- A Java IDE that you are comfortable to work with.
- [Postman](https://www.getpostman.com/downloads/)

### 2.1 Create Spring Boot Application (Enable Maven Auto-import)

#### **Suggested** Method 1: Use [IntelliJ IDE](https://www.jetbrains.com/idea/download)

- Instead of downloading the Community Edition from above, it is recommended that students get the IntelliJ IDEA Ultimate for free by signing up using their university email address [here](https://www.jetbrains.com/shop/eform/students).

- If you do not see Spring Initializr in IntelliJ, (you are probably using the Community Edition which doesn't support this and thus) you can download the Spring Assistant plug-in by going to File > Settings > Plugins > Marketplace > Search for "Spring Assistant". Click "Install", then "Restart". Now when you create a new project under File > New > Project, you should be able to see Spring Assistant (an alternative to Spring Initializr).

![](https://github.com/LiMengyang990726/Spring-Boot-Introduction/blob/master/images/Step1.png)

![](https://github.com/LiMengyang990726/Spring-Boot-Introduction/blob/master/images/Step2.png)

![](https://github.com/LiMengyang990726/Spring-Boot-Introduction/blob/master/images/Step3.png)

#### Method 2: Use Eclipse IDE

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

#### Method 3: [Download from Spring Boot Website](https://start.spring.io/)
![](https://github.com/LiMengyang990726/Spring-Boot-Introduction/blob/master/images/IStep1.png)

### 2.2 Set Up MySQL database

- For Windows
  - [Download MySQL Community Server](https://dev.mysql.com/downloads/mysql/). Please download the `zip` file.
  
  ![](https://github.com/LiMengyang990726/Spring-Boot-Introduction/blob/master/images/MySQLWindows.png)
  
  ![](https://github.com/LiMengyang990726/Spring-Boot-Introduction/blob/master/images/MySQL1.png)
  
  - Unzip the `mysql-X.X.X-winxXX.zip` to a directory. E.g. `C:\Users\%USERNAME%\Downloads`
  
  - Open command prompt. Type in the following:

  ```
  $ cd C:\Users\%USERNAME%\Downloads\mysql-X.X.XX-winxXX\mysql-X.X.XX-winxXX\bin
  
  # Initialize the database. Create a root user with random password. Show the messages on console
  $ mysqld --initialize --console
  ...
  ...A temporary password is generated for root@localhost: xxxxxxxx // take note of this password, if forget, delete and unzipped folder, unzip it, and repeat the above steps
  ```
  
  - To start the server:
  
  ```
  $ mysqld --console
  ```
  
  - To shut down the server: Ctrl+C (but don't do it now, we need to keep the connection alive to connect to MySQL)
  
  - Open another Command Prompt. To start a 'Client':
  
  ```
  $ mysql -u root -p
  Enter password: XXXXXXX  // Enter temporary password which was generated just now
  Welcome to the MySQL monitor.  Commands end with ; or \g.
  Your MySQL connection id is 1
  Server version: 8.0.xx
  Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

  mysql>
  ```
  
- For MacOS
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
  $ cd /usr/local/mysql/bin
  ./mysql -u root -p
  Enter password:   // Enter the root's password given during installation. You will NOT any * for maximum security
  Welcome to the MySQL monitor.  Commands end with ; or \g.
  ......
  mysql>
  ```
  
- For [Ubuntu](https://www.ntu.edu.sg/home/ehchua/programming/howto/Ubuntu_HowTo.html#mysql).

### 2.3 Connect MySQL Database to Spring Boot project via Hibernate

- Step 1: Open `File/Project Structure` in IntelliJ

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

### 3.0 Goals

- (GET) Retreive products according to catagory 

- (GET) Retreive products that a merchant has

- (POST) Add new products

- (PUT) Update product information

- (DELETE) Delete products


### 3.1 Database Design

![](https://github.com/LiMengyang990726/Spring-Boot-Introduction/blob/master/images/ERDiagram.png)

### 3.2 File Structure (Good Software Engineering Practice Suggestion)

![](https://github.com/LiMengyang990726/Spring-Boot-Introduction/blob/master/images/fileStructure.png)

### 3.3 Coding

- Step 0: Create Database in MySQL and configuration ini `application.properties`

Windows: 

```
cd \SpringBootIntroduction\mysql\bin
mysql -u root -p
...
mysql> CREATE DATABASE inventory;
```

MacOS:

```
cd /usr/local/mysql/bin
./mysql -u root -p
...
mysql> CREATE DATABASE inventory;
```

Insert some data:

```
insert into Product (productID, category,description,merchantID,name,price) VALUES (110,"book","extrodinary book that deserves your reading",200,"Black Swan Green", 37.9);
insert into Product (productID, category,description,merchantID,name,price) VALUES (111,"pen","hand made wood pen that is specially for you",200,"Burgendy Pen",26.8);
insert into Product (productID, category,description,merchantID,name,price) VALUES (112,"mouse","hold this mouse, you will feel you own the whole world",201,"Good Mouse", 67);
insert into Product (productID, category,description,merchantID,name,price) VALUES (113,"book","heartbreaking. The portrait of Afghan culture broadly painted",202,"The Kite Runner",37);
insert into Product (productID, category,description,merchantID,name,price) VALUES (114,"book","When a man is found murdered in an abandoned building, unflappable detective Sasagaki is assigned to the case.", 202,"Journey Under the Midnight Sun", 37);
```
Application.properties:

```

server:
  port: 8080

spring:
  jpa:
    generate-ddl: true
    show-sql: true
    hibernate:
      show-sql: true
      ddl-auto: update
      naming.physical-strategy: org.hibernate.boot.model.naming.PhysicalNamingStrategyStandardImpl
    properties:
      hibernate:
        default_schema: app
        id.new_generator_mappings: true
        dialect: org.hibernate.dialect.MySQL5Dialect
  datasource:
    url: jdbc:mysql://localhost:3306/inventory?useUnicode=true&useJDBCCompliantTimezoneShift=true&useLegacyDatetimeCode=false&serverTimezone=UTC
    username: root
    password: 
```

- Step 1: Write Entities

`@Entity`: name an entity

`@Table(name="product")`: name a table in database

`@Id`: primary key

`@Column`: name a column in database

- Step 2: Create Repo

`extends JpaRepository<T,D>`: JpaRepository = CrudRepository + PageAndSortingRepository

- Step 3: Write Service

`ProductService`: `ProductServiceImpl`, `ProductServiceCacheImpl`,...

`@Service`: sterotype annotation

`@Autowire`: dependency injection

- Step 4: Write Controller

`@RestController`: = `@Controller` + `@RequestBody`

`@RequestMapping`: annotation

## Reference:
1. https://www.quora.com/What-is-Spring-Framework-used-for
2. https://www.ntu.edu.sg/home/ehchua/programming/sql/MySQL_HowTo.html
3. [Java Brains Youtube Tutorial Series](https://www.youtube.com/watch?v=bDtZvYAT5Sc&list=PLqq-6Pq4lTTbx8p2oCgcAQGQyqN8XeA1x&index=8)
4. [Telusko Youtube Tutorial Series](https://www.youtube.com/watch?v=Ch163VfHtvA)
