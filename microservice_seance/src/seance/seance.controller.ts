import { Controller, Get, Post, Body, Delete, Param } from '@nestjs/common';
import { SeanceDto } from '../dto/seance.dto';
import { SeanceService } from './seance.service';
import { Seance } from '../entities/seance.entity';

@Controller('seance')
export class SeanceController {
  constructor(private readonly seanceService: SeanceService) {}

  @Get()
  async findAll(): Promise<Seance[]> {
    return this.seanceService.findAll();
  }

  @Get(':id')
  async findOne(@Param('id') id: string): Promise<Seance> {
    return this.seanceService.findOne(id);
  }

  @Post()
  async create(@Body() seanceDto: SeanceDto): Promise<Seance> {
    return this.seanceService.create(seanceDto);
  }

  @Delete(':id')
  async delete(@Param('id') id: string): Promise<{ message: string }> {
    await this.seanceService.delete(id);
    return { message: 'Seance deleted successfully!' };
  }
}
