package com.example.demo.repo;

import com.example.demo.model.Product;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;


public interface ProductRepo extends JpaRepository<Product, Integer> {
    List<Product> findAllByCategory(String category);

    Product findByProductID(int productID);

    List<Product> findAllByMerchantID(int merchantID);

    Product save(Product product);

}
