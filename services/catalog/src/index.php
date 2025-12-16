<?php
declare(strict_types=1);

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

$path = parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH) ?: '/';
$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';

$send = static function (int $status, mixed $payload): void {
    http_response_code($status);
    $normalized = is_array($payload) ? $payload : ['message' => (string) $payload];
    echo json_encode($normalized, JSON_PRETTY_PRINT);
};

$dbConfig = [
    'host' => getenv('DB_HOST') ?: 'postgres',
    'port' => getenv('DB_PORT') ?: '5432',
    'dbname' => getenv('DB_NAME') ?: 'catalog_db',
    'user' => getenv('DB_USER') ?: 'catalog_user',
    'password' => getenv('DB_PASSWORD') ?: 'catalog_pass',
];

$dbTest = static function () use ($dbConfig): array {
    $dsn = sprintf('pgsql:host=%s;port=%s;dbname=%s', $dbConfig['host'], $dbConfig['port'], $dbConfig['dbname']);
    try {
        $pdo = new PDO($dsn, $dbConfig['user'], $dbConfig['password'], [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        ]);
        $row = $pdo->query('SELECT current_database() AS db, current_user AS user')->fetch();
        return [
            'status' => 'ok',
            'db' => $row['db'] ?? null,
            'user' => $row['user'] ?? null,
        ];
    } catch (Throwable $e) {
        return [
            'status' => 'error',
            'message' => 'DB connection failed',
            'error' => $e->getMessage(),
        ];
    }
};

if ($path === '/health') {
    $send(200, [
        'service' => 'catalog',
        'status' => 'ok',
        'timestamp' => (new DateTimeImmutable())->format(DateTimeInterface::ATOM),
    ]);
    exit;
}

$sampleFilms = [
    [
        'id' => 1,
        'title' => 'Placeholder Film',
        'duration' => 120,
        'rating' => 'PG-13',
        'director' => 'A. Director',
        'description' => 'Seed data so that front-end devs can start.',
        'posterUrl' => 'https://via.placeholder.com/300x450.png?text=Poster',
        'posterRotationDeg' => 0,
    ],
];

$routes = [
    'GET' => [
        '/films' => static fn () => $sampleFilms,
        '/films/1' => static fn () => $sampleFilms[0],
        '/hello' => static fn () => [
            'status' => 'ok',
            'message' => 'Hello World',
        ],
        '/db-test' => $dbTest,
    ],
];

if (isset($routes[$method][$path])) {
    $payload = $routes[$method][$path]();
    $send(200, $payload);
    exit;
}

$send(501, [
    'message' => 'Catalog service skeleton. Implement business logic here.',
    'method' => $method,
    'path' => $path,
]);
