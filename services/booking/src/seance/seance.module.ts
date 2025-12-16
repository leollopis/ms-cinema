import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { SeanceController } from './seance.controller';
import { SeanceService } from './seance.service';
import { Seance } from '../entities/seance.entity';

@Module({
  imports: [TypeOrmModule.forFeature([Seance])],
  controllers: [SeanceController],
  providers: [SeanceService],
  exports: [SeanceService],
})
export class SeanceModule {}