import { Injectable } from '@angular/core';



@Injectable()
export class ConstantsService {

  readonly baseUrl: string = 'http://localhost:4200/';
  readonly apiEndpoint: string = 'http://localhost:5000/';

  public themeElement: HTMLElement;
  public mapElement:HTMLElement;

  public map;
}