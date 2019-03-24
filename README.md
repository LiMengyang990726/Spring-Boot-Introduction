# Spring-Boot-Introduction
Special thanks to Java Brain Youtube Tutorial Series.

## Agenda
1. Spring Boot Basics
2. Set up
3. Build a Spring boot applicaton together!

## Spring Boot Basics

### Comparision between Spring and Spring boot

|  | Spring | Spring boot|
| ------------- | ------------- | ------------- |
| Definition|  huge Enterprise Java Framework | bootstrap a standalone, producation-grade Spring application that can be easily run|
| Features|  POJOs<br> Dependency Injection<br> MVC<br> Security<br> Integrate with other framework like Hibernate <br> ...| Convention over configuration. On top of Spring framework, help developers solve the additional jar files and configurations, while you can also done manual configuration in `applicatoin.properties` <br><br> Embedded Tomcat server <br><br> ...|

### When will you use Spring boot?

Spring boot can be used to build backend services. An easy start is to build a RESTful API.


### Important Concept

POJO: Plain Old Java Object. An ordinary Java object. [For more information](https://www.geeksforgeeks.org/pojo-vs-java-beans/)

| POJO | Java Bean |
| ---- | ----- |
| E.g `public class Employee { … }` | E.g  `public class GFG extends javax.servlet.http.HttpServlet { … } `|
| Not all POJOs are Java Beans | All Java Beans are POJOS |


MVC: Model-View-Controller (MVC). An architectural pattern.
![](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png)

Tomcat Server: (Will be added later)

Dependency Injection: Details will be talked about later.
