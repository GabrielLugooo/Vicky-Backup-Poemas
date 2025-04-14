// app.js

document.addEventListener("DOMContentLoaded", async () => {
  const poemsContainer = document.getElementById("poems-container");
  const loadingMessage = document.getElementById("loading-message");

  try {
    const res = await fetch("http://localhost:3000/api/poemas");
    const data = await res.json();

    loadingMessage.style.display = "none";
    poemsContainer.innerHTML = "";

    data.forEach((poema) => {
      const poemCard = document.createElement("div");
      poemCard.className = "card";

      const lines = poema.contenido.trim().split("\n");
      let titulo = "Poema sin título";
      let contenido = lines;

      if (lines[0].startsWith("#")) {
        titulo = lines[0].replace(/^#/, "").trim();
        contenido = lines.slice(1);
      }

      const titleEl = document.createElement("div");
      titleEl.className = "poem-title";
      titleEl.textContent = titulo;

      const contentEl = document.createElement("div");
      contentEl.className = "poem-content";
      contentEl.innerHTML = marked.parse(contenido.join("\n"));

      poemCard.appendChild(titleEl);
      poemCard.appendChild(contentEl);
      poemsContainer.appendChild(poemCard);
    });
  } catch (error) {
    console.error("Error al cargar los poemas:", error);
    loadingMessage.innerHTML = "<p>💔 No se pudieron cargar los poemas.</p>";
  }
});
