import { Injectable } from '@nestjs/common';

@Injectable()
export class AppService {
  getHello(): Record<string, string> {
    return { status: 'ok', message: 'Hello World' };
  }
}
