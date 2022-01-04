import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AirportTableComponent } from './airport-table.component';

describe('AirportTableComponent', () => {
  let component: AirportTableComponent;
  let fixture: ComponentFixture<AirportTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AirportTableComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AirportTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
