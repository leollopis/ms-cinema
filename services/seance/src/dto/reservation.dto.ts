import { IsOptional, IsString, IsNotEmpty } from 'class-validator';

export class ReservationDto {
  @IsString()
  @IsNotEmpty()
  name: string;

  @IsOptional()
  @IsString()
  email?: string;

  @IsOptional()
  @IsString()
  seanceId?: string;

  @IsOptional()
  @IsString()
  seatNumber?: string;

  



}
