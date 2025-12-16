import { IsOptional, IsString, IsNotEmpty, IsInt, IsDecimal } from 'class-validator';

export class SeanceDto {
    @IsString()
    @IsNotEmpty()
    nameMovie: string;

    @IsOptional()
    @IsInt()
    numberPlace?: number;

    @IsOptional()
    @IsString()
    hourStart?: string;

    @IsOptional()
    @IsString()
    hourEnd?: string;

    @IsOptional()
    @IsString()
    dateSeance?: string;

    @IsOptional()
    @IsString()
    salleId?: string;

    @IsOptional()
    @IsDecimal()
    price?: number;
}
