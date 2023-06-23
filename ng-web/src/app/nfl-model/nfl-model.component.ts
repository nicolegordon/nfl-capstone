import { Component, OnInit } from '@angular/core';
import {
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { NgIf, NgFor } from '@angular/common';
import { ModelService } from '../model/model.service';
import { NflGame, WinnerPrediction } from '../model/types';

@Component({
  selector: 'nfl-model',
  templateUrl: './nfl-model.component.html',
  styleUrls: ['./nfl-model.component.css'],
  standalone: true,
  imports: [
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    ReactiveFormsModule,
    NgIf,
    NgFor,
  ],
})
export class NflModelComponent implements OnInit {
  gameInfo!: NflGame;
  predictionProb!: number;

  // List of all NFL teams
  public nflTeams: string[] = [
    'ARI',
    'ATL',
    'BAL',
    'BUF',
    'CAR',
    'CHI',
    'CIN',
    'CLE',
    'DAL',
    'DEN',
    'DET',
    'GB',
    'HOU',
    'IND',
    'JAX',
    'KC',
    'LV',
    'LAC',
    'LAR',
    'MIA',
    'MIN',
    'NE',
    'NO',
    'NYG',
    'NYJ',
    'PHI',
    'PIT',
    'SF',
    'SEA',
    'TB',
    'TEN',
    'WAS',
  ];

  // Form group
  gameForm = new FormGroup({
    homeTeam: new FormControl('', [Validators.required]),
    awayTeam: new FormControl('', [Validators.required]),
    homeScore: new FormControl('', [
      Validators.required,
      Validators.min(0),
      Validators.pattern('([0-9]+)'),
    ]),
    awayScore: new FormControl('', [
      Validators.required,
      Validators.min(0),
      Validators.pattern('([0-9]+)'),
    ]),
    possessionTeam: new FormControl('', [Validators.required]),
    quarter: new FormControl('', [
      Validators.min(1),
      Validators.max(5),
      Validators.pattern('([0-9]+)'),
      Validators.required,
    ]),
    week: new FormControl('', [
      Validators.min(1),
      Validators.max(17),
      Validators.pattern('([0-9]+)'),
      Validators.required,
    ]),
  });

  // Current selected variables
  selectedHomeTeam: string | null = 'Home Team';
  selectedAwayTeam: string | null = 'Away Team';
  currentHomeScore: string | null = '';
  currentAwayScore: string | null = '';
  currentPossessionTeam: string | null = '';
  currentQuarter: string | null = '';
  currentWeek: string | null = '';

  // Two teams selected as home and away
  playingTeams: (string | null)[] = [
    this.selectedAwayTeam,
    this.selectedHomeTeam,
  ].sort();

  // Winner prediction
  prediction: string = '';

  // If the Predict button is disabled
  isDisabled: boolean = true;

  constructor(private modelSvc: ModelService) {}
  ngOnInit() {
    // Subscriptions to all form controls
    this.gameForm.get('homeTeam')?.valueChanges.subscribe((team) => {
      this.selectedHomeTeam = team;
      this.playingTeams = [this.selectedAwayTeam, this.selectedHomeTeam].sort();
    });

    this.gameForm.get('awayTeam')?.valueChanges.subscribe((team) => {
      this.selectedAwayTeam = team;
      this.playingTeams = [this.selectedAwayTeam, this.selectedHomeTeam].sort();
    });

    this.gameForm.get('homeScore')?.valueChanges.subscribe((score) => {
      this.currentHomeScore = score;
    });

    this.gameForm.get('awayScore')?.valueChanges.subscribe((score) => {
      this.currentAwayScore = score;
    });

    this.gameForm.get('possessionTeam')?.valueChanges.subscribe((team) => {
      this.currentPossessionTeam = team;
    });

    this.gameForm.get('quarter')?.valueChanges.subscribe((quarter) => {
      this.currentQuarter = quarter;
    });

    this.gameForm.get('week')?.valueChanges.subscribe((week) => {
      this.currentWeek = week;
    });
  }

  // Function executes when predict button is clicked
  onPredictClick(): void {
    this.gameInfo = this.gameForm.value;
    this.modelSvc
      .predictNflWinner(this.gameInfo)
      .subscribe((response: WinnerPrediction) => {
        this.predictionProb = response.value;
        this.prediction = `${response.name} has a ${this.predictionProb}% chance of winning`;
      });
  }

  // Function to get score errors
  getScoreError(formField: string): string {
    if (this.gameForm.get(formField)?.hasError('required')) {
      return 'Field is required';
    }

    if (this.gameForm.get(formField)?.hasError('min')) {
      return 'Score must be greater than or equal to 0';
    }

    return this.gameForm.get(formField)?.hasError('pattern')
      ? 'Score must be an integer'
      : '';
  }

  // Function to get quarter errors
  getQuarterError(): string {
    if (this.gameForm.get('quarter')?.hasError('required')) {
      return 'Field is required';
    }

    if (
      this.gameForm.get('quarter')?.hasError('min') ||
      this.gameForm.get('quarter')?.hasError('max')
    ) {
      return 'Valid range: 1-5';
    }

    return this.gameForm.get('quarter')?.hasError('pattern')
      ? 'Quarter must be an integer'
      : '';
  }

  // Function to get week errors
  getWeekError(): string {
    if (this.gameForm.get('week')?.hasError('required')) {
      return 'Field is required';
    }

    if (
      this.gameForm.get('week')?.hasError('min') ||
      this.gameForm.get('week')?.hasError('max')
    ) {
      return 'Valid range: 1-17';
    }

    return this.gameForm.get('week')?.hasError('pattern')
      ? 'Week must be an integer'
      : '';
  }
}
