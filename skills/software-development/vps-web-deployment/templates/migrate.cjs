const fs = require('fs');
const path = require('path');
const mysql = require('mysql2/promise');
require('dotenv').config({ path: path.resolve(__dirname, '../.env') });

async function runMigrations() {
  const connection = await mysql.createConnection({
    host: process.env.DB_HOST || '127.0.0.1',
    port: parseInt(process.env.DB_PORT || '3306', 10),
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
    multipleStatements: true,
  });

  try {
    await connection.query(`
      CREATE TABLE IF NOT EXISTS _migrations (
        name VARCHAR(255) PRIMARY KEY,
        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `);

    const [rows] = await connection.query(`SELECT name FROM _migrations`);
    const applied = new Set(rows.map(r => r.name));

    const dir = path.resolve(__dirname, '../migrations');
    if (!fs.existsSync(dir)) {
      console.log('No migrations directory found.');
      return;
    }

    const files = fs.readdirSync(dir)
      .filter(f => f.endsWith('.sql'))
      .sort();

    for (const file of files) {
      if (applied.has(file)) {
        continue;
      }
      console.log(`Applying migration: ${file}`);
      const sql = fs.readFileSync(path.join(dir, file), 'utf8');
      if (sql.trim()) {
        await connection.query(sql);
      }
      await connection.query(`INSERT INTO _migrations (name) VALUES (?)`, [file]);
      console.log(`✓ Applied: ${file}`);
    }
    console.log('All migrations up to date.');
  } finally {
    await connection.end();
  }
}

runMigrations().catch(err => {
  console.error('Migration failed:', err.message);
  process.exit(1);
});
