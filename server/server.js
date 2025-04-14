// server.js
const express = require("express");
const fetch = require("node-fetch");
const dotenv = require("dotenv");
const path = require("path");

dotenv.config();

const app = express();
const PORT = 3000;

// Configurar carpeta pública
app.use(express.static("public")); // <-- Asegurate que tus archivos HTML/CSS/JS estén en esa carpeta

// Ruta para obtener los archivos de poemas
app.get("/api/poemas", async (req, res) => {
  try {
    const response = await fetch(
      "https://api.github.com/repos/GabrielLugooo/Vicky-Backup-Poemas/contents/poemas",
      {
        headers: {
          Authorization: `token ${process.env.GITHUB_TOKEN}`,
          Accept: "application/vnd.github.v3+json",
        },
      }
    );

    if (!response.ok) {
      return res
        .status(response.status)
        .json({ error: "No se pudo acceder al repositorio" });
    }

    const archivos = await response.json();
    const markdowns = archivos.filter((file) => file.name.endsWith(".md"));

    const poemas = await Promise.all(
      markdowns.map(async (file) => {
        const raw = await fetch(file.download_url);
        const contenido = await raw.text();
        return {
          nombre: file.name.replace(".md", ""),
          contenido,
        };
      })
    );

    res.json(poemas);
  } catch (error) {
    console.error("Error al obtener poemas:", error);
    res.status(500).json({ error: "Error interno del servidor" });
  }
});

app.listen(PORT, () => {
  console.log(`🚀 Servidor corriendo en http://localhost:${PORT}`);
});
