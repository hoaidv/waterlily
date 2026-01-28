
Let's keep our system extremely simple with the following components/layers

# Layers

## API layer

Convert requests into command and invoke the corresponding AppCore function.

## AppCore layer

Perform the actual logic. We do the actual logic right here.

## Repository layer

Access the database. Map database result to business entities or any 
helper objects.

This component may have its own database model (depends on the actual library used).

# Shared components

## Models

Containing business entities and helper entities description as Java/Kotlin classes. 
This is not the database models. `AppCore` works on these models.

- Business entities: A business entity has an actual business definition, 
  in a ubiquitous language.
- Helper objects: A helper object is derived from one or serveral business entities.
  - Example 1: We need a helper category entity (1) together with its 
    product definition entity (1) and its attribute definition entities (N). 
    This becomes handy when we validate or create products.
    This is shared among services within `AppCore`.
  - Example 2: We need a query entity to enrich, manipulate and store all 
    query information, before passing it to repositories. 
    This is shared between `AppCore` and related `Repository`.
  - Example 3: We need a product detail object to include not only product fields 
    but also its media, variants and category detail.
    This is shared between `AppCore` and related `API`.