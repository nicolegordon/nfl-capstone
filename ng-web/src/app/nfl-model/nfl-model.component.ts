import { Component, OnInit } from '@angular/core';
import {
  Form,
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
  homeTeamForm = new FormControl(null, [Validators.required]);
  awayTeamForm = new FormControl(null, [Validators.required]);
  homeScoreForm = new FormControl(null, [
    Validators.required,
    Validators.min(0),
    Validators.pattern('([0-9]+)'),
  ]);
  awayScoreForm = new FormControl(null, [
    Validators.required,
    Validators.min(0),
    Validators.pattern('([0-9]+)'),
  ]);
  possessionTeamForm = new FormControl(null, [Validators.required]);

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
    this.homeTeamForm.valueChanges.subscribe((team) => {
      this.selectedHomeTeam = team;
      this.playingTeams = [this.selectedAwayTeam, this.selectedHomeTeam].sort();
      this.isInvalid();
    });

    this.awayTeamForm.valueChanges.subscribe((team) => {
      this.selectedAwayTeam = team;
      this.playingTeams = [this.selectedAwayTeam, this.selectedHomeTeam].sort();
      this.isInvalid();
    });

    this.homeScoreForm.valueChanges.subscribe((score) => {
      this.currentHomeScore = score;
      this.isInvalid();
    });

    this.awayScoreForm.valueChanges.subscribe((score) => {
      this.currentAwayScore = score;
      this.isInvalid();
    });

    this.possessionTeamForm?.valueChanges.subscribe((team) => {
      this.currentPossessionTeam = team;
      this.isInvalid();
    });
  }

  // Function executes when predict button is clicked
  onPredictClick(): void {
    console.log(this.possessionTeamForm.value);
  }

  // Function to get errors
  getScoreError(form: FormControl): string {
    if (form.hasError('required')) {
      return 'Field is required';
    }

    if (form.hasError('min')) {
      return 'Score must be greater than or equal to 0';
    }

    return form.hasError('pattern') ? 'Score must be an integer' : '';
  }

  // Function to check if form controls are invalid
  isInvalid(): void {
    if (
      this.awayScoreForm.invalid ||
      this.homeScoreForm.invalid ||
      this.possessionTeamForm.invalid
    ) {
      this.isDisabled = true;
    } else {
      this.isDisabled = false;
    }
  }
}
