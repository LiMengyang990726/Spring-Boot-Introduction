package com.example.demo.service;

import com.example.demo.model.Product;

import java.util.List;

public interface ProductService {

    List<Product> retreiveAll();

    List<Product> retreiveByCategory(String category);

    List<Product> retreiveByCategoryOfMerchant(int merchantID,String category);

    Product saveNewProduct(Product product);

    void updateExistingProduct(int productID, Product newProduct);

    void deleteProduct(int productID);



}
