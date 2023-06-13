import { NflGame, WinnerPrediction } from './types';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class ModelService {
  constructor(private http: HttpClient) {}

  public predictNflWinner(game: NflGame): Observable<WinnerPrediction> {
    const url: string = `api/predict`;
    return this.http.post<WinnerPrediction>(url, game);
  }
}
