import pkg from 'pg';
const { Client } = pkg;

const client = new Client({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false }
});

(async () => {
  try {
    await client.connect();
    const res = await client.query('SELECT 1 AS ok;');
    console.log('✅ Connexion réussie, résultat :', res.rows);
  } catch (err) {
    console.error('❌ Erreur de connexion :', err);
  } finally {
    await client.end();
  }
})();
