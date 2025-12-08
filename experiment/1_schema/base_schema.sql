-- Base Schema for E-commerce Platform
-- Generated from base_schema.md

-- Drop tables if they exist (in reverse order of dependencies)
DROP TABLE IF EXISTS product_variants;
DROP TABLE IF EXISTS product_variant_defs;
DROP TABLE IF EXISTS product_def_attributes;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS product_defs;

-- Create product_defs table
-- Role: Define how to dictate a product's attributes
CREATE TABLE product_defs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(512) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create categories table
-- Role: Categorize the product
CREATE TABLE categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(256) NOT NULL,
    description TEXT,
    product_def_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (product_def_id) REFERENCES product_defs(id) ON DELETE SET NULL,
    INDEX idx_product_def_id (product_def_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create products table
-- Role: Main product entity
CREATE TABLE products (
    id BIGINT PRIMARY KEY,
    base_sku VARCHAR(128) NOT NULL UNIQUE,
    name VARCHAR(512) NOT NULL,
    description TEXT,
    status ENUM('ACTIVE', 'INACTIVE') NOT NULL DEFAULT 'ACTIVE',
    source VARCHAR(128) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    category_id INT,
    product_def_id INT,
    attributes JSON,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
    FOREIGN KEY (product_def_id) REFERENCES product_defs(id) ON DELETE SET NULL,
    INDEX idx_base_sku (base_sku),
    INDEX idx_status (status),
    INDEX idx_source (source),
    INDEX idx_category_id (category_id),
    INDEX idx_product_def_id (product_def_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create product_def_attributes table
-- Role: List of attributes a product must have
CREATE TABLE product_def_attributes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_def_id INT NOT NULL,
    name VARCHAR(128) NOT NULL,
    datatype VARCHAR(64) NOT NULL,
    display_name VARCHAR(256) NOT NULL,
    default_value VARCHAR(512),
    validation_rules JSON DEFAULT (JSON_OBJECT()),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (product_def_id) REFERENCES product_defs(id) ON DELETE CASCADE,
    UNIQUE KEY uk_product_def_name (product_def_id, name),
    INDEX idx_name (name),
    INDEX idx_product_def_id (product_def_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create product_variant_defs table
-- Role: Maps products to which attributes are used for creating variants
CREATE TABLE product_variant_defs (
    product_id BIGINT NOT NULL,
    attribute_name VARCHAR(128) NOT NULL,
    `order` INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (product_id, attribute_name),
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    INDEX idx_product_id_order (product_id, `order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create product_variants table
-- Role: Actual product variants (combinations of attribute values)
CREATE TABLE product_variants (
    id BIGINT PRIMARY KEY,
    product_id BIGINT NOT NULL,
    variant_sku VARCHAR(256) NOT NULL UNIQUE,
    quantity INT NOT NULL DEFAULT 0,
    price DECIMAL(15, 2) NOT NULL,
    attributes JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    INDEX idx_product_id (product_id),
    INDEX idx_variant_sku (variant_sku),
    INDEX idx_quantity (quantity)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Add comments to tables
ALTER TABLE product_defs COMMENT = 'Defines how to dictate a products attributes';
ALTER TABLE categories COMMENT = 'Product categories';
ALTER TABLE products COMMENT = 'Main product entity';
ALTER TABLE product_def_attributes COMMENT = 'List of attributes a product must have';
ALTER TABLE product_variant_defs COMMENT = 'Maps products to variant attributes';
ALTER TABLE product_variants COMMENT = 'Actual product variants';

