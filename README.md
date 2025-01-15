# Gestión Bibliotecaria

Este proyecto es un programa interactivo desarrollado en Python para la gestión de una biblioteca.
Está diseñado para ser eficiente y fácil de usar, integrando tablas hash para búsquedas rápidas y un historial de préstamos
para rastrear las actividades de los usuarios.

## Características

### **Gestión de Usuarios**
- Crear usuarios con un ID único.
- Los datos de los usuarios se almacenan en un archivo JSON (`usuarios.json`).

### **Gestión de Libros**
- Agregar nuevos libros a la biblioteca.
- Buscar libros por título, utilizando tablas hash para una búsqueda rápida.
- Mostrar la localización del libro en la biblioteca.
- Los datos de los libros se almacenan en un archivo JSON (`libros.json`).

### **Historial de Préstamos**
- Registrar préstamos de libros realizados por los usuarios.
- Consultar el historial de préstamos.
- Permitir devoluciones de libros y actualizar el historial.
- El historial de préstamos se almacena en un archivo JSON (`historial_prestamos.json`).

### **Persistencia de Datos**
- Toda la información (usuarios, libros y préstamos) se guarda en archivos JSON, lo que asegura que los datos estén disponibles incluso después de cerrar el programa.

## Cómo usar el programa

1. **Requisitos previos**:
   - Tener instalado Python 3.x.

2. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/pablo-ph-py/gestion-bibliotecaria.git
   cd gestion-bibliotecaria
   python gestion_biblioteca.py