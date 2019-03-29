package com.example.demo.model;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Table(name = "Product")
public class Product {

    @Id
    @Column
    private int productID;

    @Column
    private int merchantID;

    @Column
    private float price;

    @Column
    private String name;

    @Column
    private String description;

    @Column
    private String category;

    public Product(){

    }

    public Product(int productID, int merchantID, float price, String name, String description, String category) {
        this.productID = productID;
        this.merchantID = merchantID;
        this.price = price;
        this.name = name;
        this.description = description;
        this.category = category;
    }

    public int getProductID() {
        return productID;
    }

    public void setProductID(int productID) {
        this.productID = productID;
    }

    public int getMerchantID() {
        return merchantID;
    }

    public void setMerchantID(int merchantID) {
        this.merchantID = merchantID;
    }

    public float getPrice() {
        return price;
    }

    public void setPrice(float price) {
        this.price = price;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }
}
