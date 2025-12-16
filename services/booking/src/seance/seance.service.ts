import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Seance } from '../entities/seance.entity';
import { SeanceDto } from '../dto/seance.dto';

@Injectable()
export class SeanceService {
  constructor(
    @InjectRepository(Seance)
    private readonly seanceRepository: Repository<Seance>,
  ) {}

  async findAll(): Promise<Seance[]> {
    return this.seanceRepository.find({ relations: ['reservations'] });
  }

  async findOne(id: string): Promise<Seance> {
    const seance = await this.seanceRepository.findOne({
      where: { id },
      relations: ['reservations'],
    });
    if (!seance) {
      throw new NotFoundException(`Seance with ID ${id} not found`);
    }
    return seance;
  }

  async create(seanceDto: SeanceDto): Promise<Seance> {
    const seance = this.seanceRepository.create(seanceDto);
    return this.seanceRepository.save(seance);
  }

  async update(id: string, seanceDto: Partial<SeanceDto>): Promise<Seance> {
    await this.findOne(id);
    await this.seanceRepository.update(id, seanceDto);
    return this.findOne(id);
  }

  async delete(id: string): Promise<void> {
    const result = await this.seanceRepository.delete(id);
    if (result.affected === 0) {
      throw new NotFoundException(`Seance with ID ${id} not found`);
    }
  }
}
