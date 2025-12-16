import { Entity, PrimaryGeneratedColumn, Column, OneToMany } from 'typeorm';
import { Reservation } from './reservation.entity';

@Entity('seances')
export class Seance {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  nameMovie: string;

  @Column({ nullable: true })
  numberPlace: number;

  @Column({ nullable: true })
  hourStart: string;

  @Column({ nullable: true })
  hourEnd: string;

  @Column({ nullable: true })
  dateSeance: string;

  @Column({ nullable: true })
  salleId: string;

  @Column({ type: 'decimal', precision: 10, scale: 2, nullable: true })
  price: number;

  @OneToMany(() => Reservation, (reservation) => reservation.seance)
  reservations: Reservation[];
}
