import { Controller, Get, Post, Body, Param, Delete } from '@nestjs/common';
import { ReservationDto } from '../dto/reservation.dto';
import { ReservationService } from './reservation.service';
import { Reservation } from '../entities/reservation.entity';

@Controller('reservation')
export class ReservationController {
  constructor(private readonly reservationService: ReservationService) {}

  @Get()
  async findAll(): Promise<Reservation[]> {
    return this.reservationService.findAll();
  }

  @Get(':id')
  async findOne(@Param('id') id: string): Promise<Reservation> {
    return this.reservationService.findOne(id);
  }

  @Post()
  async create(@Body() reservationDto: ReservationDto): Promise<Reservation> {
    return this.reservationService.create(reservationDto);
  }

  @Delete(':id')
  async delete(@Param('id') id: string): Promise<{ message: string }> {
    await this.reservationService.delete(id);
    return { message: 'Reservation cancelled successfully!' };
  }
}
