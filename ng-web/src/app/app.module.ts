import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavBarComponent } from './nav-bar/nav-bar.component';
import { ResumeComponent } from './resume/resume.component';
import { HomepageComponent } from './homepage/homepage.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ProjectsComponent } from './projects/projects.component';
import { NflModelComponent } from './nfl-model/nfl-model.component';

@NgModule({
  declarations: [
    AppComponent,
    ResumeComponent,
    HomepageComponent,
    ProjectsComponent,
    NflModelComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NavBarComponent,
    BrowserAnimationsModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }