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

  // Form controls
  // homeTeam = new FormControl(null, [Validators.required]);
  // awayTeam = new FormControl(null, [Validators.required]);
  // homeScore = new FormControl(null, [
  //   Validators.required,
  //   Validators.min(0),
  //   Validators.pattern('([0-9]+)'),
  // ]);
  // awayScore = new FormControl(null, [
  //   Validators.required,
  //   Validators.min(0),
  //   Validators.pattern('([0-9]+)'),
  // ]);
  // possessionTeam = new FormControl(null, [Validators.required]);
  gameForm = new FormGroup({
    homeTeam: new FormControl(null, [Validators.required]),
    awayTeam: new FormControl(null, [Validators.required]),
    homeScore: new FormControl(null, [
      Validators.required,
      Validators.min(0),
      Validators.pattern('([0-9]+)'),
    ]),
    awayScore: new FormControl(null, [
      Validators.required,
      Validators.min(0),
      Validators.pattern('([0-9]+)'),
    ]),
    possessionTeam: new FormControl(null, [Validators.required]),
  });

  // Current selected variables
  selectedHomeTeam: string | null = 'Home Team';
  selectedAwayTeam: string | null = 'Away Team';
  currentHomeScore: number | null = null;
  currentAwayScore: number | null = null;
  currentPossessionTeam: string | null = null;

  // Two teams selected as home and away
  playingTeams: (string | null)[] = [
    this.selectedAwayTeam,
    this.selectedHomeTeam,
  ].sort();

  // If the Predict button is disabled
  isDisabled: boolean = true;

  constructor() {}
  ngOnInit() {
    // Subscriptions to all form controls
    this.gameForm.get('homeTeam')?.valueChanges.subscribe((team) => {
      this.selectedHomeTeam = team;
      this.playingTeams = [this.selectedAwayTeam, this.selectedHomeTeam].sort();
      this.isInvalid();
    });

    this.gameForm.get('awayTeam')?.valueChanges.subscribe((team) => {
      this.selectedAwayTeam = team;
      this.playingTeams = [this.selectedAwayTeam, this.selectedHomeTeam].sort();
      this.isInvalid();
    });

    this.gameForm.get('homeScore')?.valueChanges.subscribe((score) => {
      this.currentHomeScore = score;
      this.isInvalid();
    });

    this.gameForm.get('awayScore')?.valueChanges.subscribe((score) => {
      this.currentAwayScore = score;
      this.isInvalid();
    });

    this.gameForm.get('possessionTeam')?.valueChanges.subscribe((team) => {
      this.currentPossessionTeam = team;
      this.isInvalid();
    });
  }

  // Function executes when predict button is clicked
  onPredictClick(): void {
    console.log(this.gameForm.get('possessionTeam')?.value);
  }

  // Function to get errors
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

  // Function to check if form controls are invalid
  isInvalid(): void {
    if (this.gameForm.invalid) {
      this.isDisabled = true;
    } else {
      this.isDisabled = false;
    }
  }
}
