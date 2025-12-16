FROM php:8.2-cli

RUN apt-get update \
	&& apt-get install -y --no-install-recommends libpq-dev \
	&& docker-php-ext-install pdo pdo_pgsql \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /var/www/html

COPY src/ /var/www/html/

EXPOSE 4001

CMD ["php", "-S", "0.0.0.0:4001", "-t", "/var/www/html"]
