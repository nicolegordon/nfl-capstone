import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NflModelComponent } from './nfl-model.component';

describe('NflModelComponent', () => {
  let component: NflModelComponent;
  let fixture: ComponentFixture<NflModelComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [NflModelComponent]
    });
    fixture = TestBed.createComponent(NflModelComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
