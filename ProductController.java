package com.example.demo.controller;

import com.example.demo.model.Product;
import com.example.demo.service.ProductService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.List;

@RestController
@RequestMapping(value = "/product")
public class ProductController {

    @Autowired
    private ProductService productService;

    // (GET) get all products
    @GetMapping("/")
    public List<Product> getAll(){
        return productService.retreiveAll();
    }


    // (GET) get all products by category
    @GetMapping("/category")
    public List<Product> getAllProductByCategory(
            @RequestParam String category
    ){
        return productService.retreiveByCategory(category);
    }


    // (GET) get all products that a merchant has by category
    @GetMapping("/category/merchant")
    public List<Product> getAllProductByCategoryOfMerchant(
            @RequestParam String category,
            @RequestParam int merchantID
    ){
        return productService.retreiveByCategoryOfMerchant(merchantID,category);
    }


    // (POST) add new product
    @PostMapping("/new")
    public Product addProduct(
            @Valid @RequestBody Product product
    ){
        return productService.saveNewProduct(product);
    }


    // (PUT) update existing product by productID
    @PutMapping("/update")
    public void updateProduct(
            @Valid @RequestBody Product product,
            @RequestParam int productID
    ){
        productService.updateExistingProduct(productID,product);
    }


    // (DELETE) delete product by productID
    @DeleteMapping("/delete")
    public void deleteProduct(
            @RequestParam int productID
    ){
        productService.deleteProduct(productID);
    }


//    @RequestMapping(value = "/", method = RequestMethod.GET)
//    public List<Product> getAll(){
//        return productService.retreiveAll();
//    }
//
//    @RequestMapping(value = "/category/{category}", method = RequestMethod.GET)
//    public List<Product> getAllProductByCategory(@PathVariable("category") String category){
//        return productService.retreiveByCategory(category);
//    }
//    @RequestMapping(value = "/category/{category}/merchant/{merchantID}",method = RequestMethod.GET)
//    public List<Product> getAllProductByCategoryOfMerchant(@PathVariable("category") String category, @PathVariable("merchantID") int merchantID){
//        return productService.retreiveByCategoryOfMerchant(merchantID,category);
//    }
}
