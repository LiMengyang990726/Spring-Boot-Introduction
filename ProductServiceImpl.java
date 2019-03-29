package com.example.demo.service;

import com.example.demo.model.Product;
import com.example.demo.repo.ProductRepo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ProductServiceImpl implements ProductService{

    @Autowired
    private ProductRepo productRepo;

    @Override
    public List<Product> retreiveAll(){
        return productRepo.findAll();
    }

    @Override
    public List<Product> retreiveByCategory(String category){
        return productRepo.findAllByCategory(category);
    }

    @Override
    public List<Product> retreiveByCategoryOfMerchant(int merchantID,String category){
        List<Product> products = productRepo.findAllByMerchantID(merchantID);
        products.stream().filter(p -> p.getCategory().equals(category));
        return products;
    }

    @Override
    public Product saveNewProduct(Product product){
        return productRepo.save(product);
    }

    @Override
    public void updateExistingProduct(int productID, Product newProduct){
        Product product = productRepo.findByProductID(productID);
        product.setCategory(newProduct.getCategory());
        product.setDescription(newProduct.getDescription());
        product.setName(newProduct.getName());
        product.setPrice(newProduct.getPrice());
        product.setMerchantID(newProduct.getMerchantID());
    }

    @Override
    public void deleteProduct(int productID){
        Product product = productRepo.findByProductID(productID);
        productRepo.delete(product);
    }

}
