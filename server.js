const http = require('http');

// Création du serveur
const server = http.createServer((req, res) => {
  // Vérifier si la méthode est GET
  if (req.method === 'GET') {
    // Récupérer les headers de la requête
    const headers = req.headers;
    
    // Afficher les détails de la requête dans la console
    console.log(`Méthode: ${req.method}`);
    console.log(`URL: ${req.url}`);
    console.log('Headers:', headers);

    // Répondre avec un message
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('Requête GET reçue et les headers ont été récupérés.');
  } else {
    // Si ce n'est pas une méthode GET, répondre par un message d'erreur
    res.writeHead(405, { 'Content-Type': 'text/plain' });
    res.end('Méthode non autorisée. Seules les requêtes GET sont acceptées.');
  }
});

// Le serveur écoute sur le port 3000
server.listen(3000, () => {
  console.log('Le serveur écoute sur le port 3000 pour les requêtes GET');
});