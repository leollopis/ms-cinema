<?php
/**
 * Catalog Microservice - Core helpers
 * Database connection + utility functions
 */

function getDbConnection(): PDO
{
    static $pdo = null;
    if ($pdo !== null) {
        return $pdo;
    }

    $host = getenv('DB_HOST') ?: 'localhost';
    $port = getenv('DB_PORT') ?: '5432';
    $dbname = getenv('DB_NAME') ?: 'catalog_db';
    $user = getenv('DB_USER') ?: 'catalog_user';
    $password = getenv('DB_PASSWORD') ?: 'catalog_pass';

    $dsn = "pgsql:host={$host};port={$port};dbname={$dbname}";

    $pdo = new PDO($dsn, $user, $password, [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        PDO::ATTR_EMULATE_PREPARES => false,
    ]);

    return $pdo;
}

function initDatabase(): void
{
    $pdo = getDbConnection();

    $pdo->exec("
        CREATE TABLE IF NOT EXISTS movies (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            genre VARCHAR(100),
            duration INTEGER,
            rating NUMERIC(3,1) DEFAULT 0,
            year INTEGER,
            age_rating VARCHAR(10),
            image TEXT,
            description TEXT,
            synopsis TEXT,
            director VARCHAR(255),
            writer VARCHAR(255),
            producer VARCHAR(255),
            studio VARCHAR(255),
            release_date VARCHAR(100),
            budget VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ");
}

function jsonResponse(mixed $data, int $code = 200): void
{
    http_response_code($code);
    echo json_encode($data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
    exit;
}

function getJsonBody(): array
{
    $raw = file_get_contents('php://input');
    $data = json_decode($raw, true);
    return is_array($data) ? $data : [];
}

/**
 * Convert snake_case DB row to camelCase for the front-end
 */
function rowToCamel(array $row): array
{
    return [
        'id'          => (int) $row['id'],
        'title'       => $row['title'],
        'genre'       => $row['genre'],
        'duration'    => $row['duration'] !== null ? (int) $row['duration'] : null,
        'rating'      => $row['rating'] !== null ? (float) $row['rating'] : null,
        'year'        => $row['year'] !== null ? (int) $row['year'] : null,
        'ageRating'   => $row['age_rating'],
        'image'       => $row['image'],
        'description' => $row['description'],
        'synopsis'    => $row['synopsis'],
        'director'    => $row['director'],
        'writer'      => $row['writer'],
        'producer'    => $row['producer'],
        'studio'      => $row['studio'],
        'releaseDate' => $row['release_date'],
        'budget'      => $row['budget'],
        'createdAt'   => $row['created_at'],
        'updatedAt'   => $row['updated_at'],
    ];
}
