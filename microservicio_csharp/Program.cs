using Npgsql;

var builder = WebApplication.CreateBuilder(args);

// SWAGGER
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// ACTIVAR SWAGGER
app.UseSwagger();
app.UseSwaggerUI();


// =====================================
// ELIMINAR PRODUCTO
// =====================================

app.MapDelete("/productos/{id:int}", async (int id) =>
{
    try
    {
        var host = Environment.GetEnvironmentVariable("DB_HOST");
        var port = Environment.GetEnvironmentVariable("DB_PORT") ?? "5432";
        var database = Environment.GetEnvironmentVariable("DB_NAME");
        var user = Environment.GetEnvironmentVariable("DB_USER");
        var password = Environment.GetEnvironmentVariable("DB_PASSWORD");

        var connectionString =
            $"Host={host};" +
            $"Port={port};" +
            $"Database={database};" +
            $"Username={user};" +
            $"Password={password};" +
            $"SSL Mode=Require";

        await using var conexion =
            new NpgsqlConnection(connectionString);

        await conexion.OpenAsync();

        await using var comando = new NpgsqlCommand(
            @"DELETE FROM mascotas_productoinventario
              WHERE id = @id
              RETURNING id, nombre, categoria, cantidad, precio",
            conexion
        );

        comando.Parameters.AddWithValue("id", id);

        await using var resultado =
            await comando.ExecuteReaderAsync();

        if (!await resultado.ReadAsync())
        {
            return Results.NotFound(new
            {
                mensaje = "Producto no encontrado"
            });
        }

        var producto = new
        {
            id = resultado.GetInt64(0),
            nombre = resultado.GetString(1),
            categoria = resultado.GetString(2),
            cantidad = resultado.GetInt32(3),
            precio = resultado.GetDecimal(4)
        };

        return Results.Ok(new
        {
            mensaje = "Producto eliminado correctamente",
            producto
        });
    }
    catch (Exception error)
    {
        Console.WriteLine(error.Message);

        return Results.Problem(
            "Error al eliminar el producto"
        );
    }
})
.WithName("EliminarProducto")
.WithSummary("Eliminar un producto")
.WithDescription(
    "Elimina un producto del inventario utilizando su ID."
);


// =====================================
// INICIAR APLICACIÓN
// =====================================

app.Run();