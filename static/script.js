const API_URL = '/api/devis'; // 在 Replit 本地使用相对路径，GitHub 页可换为完整 URL

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('gh-devisBtn');
  btn.addEventListener('click', async () => {
    const w = parseInt(document.getElementById('gh-width').value);
    const h = parseInt(document.getElementById('gh-height').value);
    const type = document.getElementById('gh-type').value;
    const out = document.getElementById('gh-result');

    if (!w || !h || !type) {
      out.textContent = 'Veuillez remplir tous les champs.';
      return;
    }

    try {
      const resp = await fetch(API_URL, {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({ largeur: w, hauteur: h, type: type })
      });

      if (!resp.ok) throw new Error(resp.statusText);
      const data = await resp.json();

      if (data && data.base_price) {
        out.innerHTML = `
          <strong>${type}</strong><br>
          Taille : ${data.matched_width}×${data.matched_height} mm<br>
          Prix : ${data.base_price} € TTC
        `;
      } else {
        out.textContent = "Aucune correspondance pour cette taille.";
      }
    } catch (err) {
      console.error('Erreur fetch:', err);
      out.textContent = 'Erreur serveur.';
    }
  });
});
