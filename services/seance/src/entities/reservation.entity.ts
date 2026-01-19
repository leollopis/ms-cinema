import { Entity, PrimaryGeneratedColumn, Column, ManyToOne, JoinColumn } from 'typeorm';
import { Seance } from './seance.entity';

@Entity('reservations')
export class Reservation {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  name: string;

  @Column({ nullable: true })
  email: string;

  @Column({ nullable: true })
  seatNumber: string;

  @Column({ nullable: true })
  seanceId: string;

  @ManyToOne(() => Seance, (seance) => seance.reservations)
  @JoinColumn({ name: 'seanceId' })
  seance: Seance;
}
