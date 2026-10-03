const express = require("express");
const { Pool } = require("pg");
const swaggerUi = require("swagger-ui-express");
const swaggerJsdoc = require("swagger-jsdoc");

const app = express();
app.use(express.json());


// ================================
// CONEXIÓN A SUPABASE
// ================================

const pool = new Pool({
    host: process.env.DB_HOST,
    port: process.env.DB_PORT || 5432,
    database: process.env.DB_NAME,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    ssl: {
        rejectUnauthorized: false
    }
});


// ================================
// CONFIGURACIÓN SWAGGER
// ================================

const swaggerOptions = {
    definition: {
        openapi: "3.0.0",
        info: {
            title: "Microservicio Node.js - Veterinaria",
            version: "1.0.0",
            description:
                "Microservicio para actualizar productos y servir como respaldo de consulta."
        },
        servers: [
            {
                url: "http://127.0.0.1:3001"
            }
        ]
    },
    apis: [__filename]
};

const swaggerSpec = swaggerJsdoc(swaggerOptions);

app.use(
    "/swagger",
    swaggerUi.serve,
    swaggerUi.setup(swaggerSpec)
);


// ================================
// ACTUALIZAR PRODUCTO
// ================================

/**
 * @swagger
 * /productos/{id}:
 *   put:
 *     summary: Actualizar un producto
 *     description: Actualiza un producto existente en el inventario.
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: integer
 *         description: ID del producto
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - nombre
 *               - categoria
 *               - cantidad
 *               - precio
 *             properties:
 *               nombre:
 *                 type: string
 *                 example: Alimento para gatos
 *               categoria:
 *                 type: string
 *                 example: Comida
 *               cantidad:
 *                 type: integer
 *                 example: 20
 *               precio:
 *                 type: number
 *                 example: 35000
 *     responses:
 *       200:
 *         description: Producto actualizado correctamente
 *       404:
 *         description: Producto no encontrado
 *       500:
 *         description: Error al actualizar el producto
 */

app.put("/productos/:id", async (req, res) => {
    try {
        const { id } = req.params;
        const {
            nombre,
            categoria,
            cantidad,
            precio
        } = req.body;

        const resultado = await pool.query(
            `UPDATE mascotas_productoinventario
             SET nombre = $1,
                 categoria = $2,
                 cantidad = $3,
                 precio = $4
             WHERE id = $5
             RETURNING *`,
            [
                nombre,
                categoria,
                cantidad,
                precio,
                id
            ]
        );

        if (resultado.rows.length === 0) {
            return res.status(404).json({
                mensaje: "Producto no encontrado"
            });
        }

        res.json(resultado.rows[0]);

    } catch (error) {

        console.error(error);

        res.status(500).json({
            mensaje: "Error al actualizar el producto"
        });
    }
});


// ================================
// CONSULTAR PRODUCTOS
// RESPALDO PARA RESILIENCIA
// ================================

/**
 * @swagger
 * /productos:
 *   get:
 *     summary: Consultar productos
 *     description: >
 *       Consulta los productos del inventario.
 *       Este endpoint funciona como respaldo
 *       cuando falla el microservicio Python.
 *     responses:
 *       200:
 *         description: Lista de productos obtenida correctamente
 *       500:
 *         description: Error al consultar los productos
 */

app.get("/productos", async (req, res) => {

    try {

        const resultado = await pool.query(
            `SELECT id,
                    nombre,
                    categoria,
                    cantidad,
                    precio
             FROM mascotas_productoinventario
             ORDER BY id`
        );

        res.json(resultado.rows);

    } catch (error) {

        console.error(error);

        res.status(500).json({
            mensaje: "Error al consultar los productos"
        });
    }
});


// ================================
// INICIAR SERVIDOR
// ================================

app.listen(3001, () => {
    console.log(
        "Microservicio Node.js ejecutándose en puerto 3001"
    );

    console.log(
        "Swagger disponible en http://127.0.0.1:3001/swagger"
    );
});