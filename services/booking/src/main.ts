import { NestFactory } from '@nestjs/core';
import * as dotenv from 'dotenv';
import { AppModule } from './app.module';

dotenv.config();

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.enableCors({ origin: '*', credentials: false });
  const port = Number(process.env.APP_PORT || 4003);
  await app.listen(port, '0.0.0.0');
}
bootstrap();
