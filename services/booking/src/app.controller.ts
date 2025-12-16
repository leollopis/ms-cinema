import { Controller, Get, HttpException } from '@nestjs/common';
import { DataSource } from 'typeorm';
import { AppService } from './app.service';

@Controller()
export class AppController {
  constructor(
    private readonly appService: AppService,
    private readonly dataSource: DataSource,
  ) {}

  @Get('hello')
  getHello(): Record<string, string> {
    return this.appService.getHello();
  }

  @Get('db-test')
  async dbTest(): Promise<Record<string, string>> {
    try {
      const result = await this.dataSource.query(
        'SELECT current_database() AS db, current_user AS user',
      );
      const row = Array.isArray(result) && result[0] ? result[0] : {};
      return { status: 'ok', db: row.db, user: row.user };
    } catch (err) {
      throw new HttpException(
        { status: 'error', message: (err as Error).message },
        500,
      );
    }
  }
}
