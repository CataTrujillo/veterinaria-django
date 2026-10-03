package com.veterinaria.microserviciojava;

import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/productos")
@CrossOrigin(origins = "*")
public class ProductoController {

    private final ProductoRepository repository;

    public ProductoController(ProductoRepository repository) {
        this.repository = repository;
    }

    @PostMapping
    public Producto insertarProducto(@RequestBody Producto producto) {
        return repository.save(producto);
    }
}