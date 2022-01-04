import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AircraftComponent } from './components/aircraft/aircraft.component';
import { AirlineComponent } from './components/airline/airline.component';
import { AirportComponent } from './components/airport/airport.component';
import { PersonComponent } from './components/person/person.component';
import { FlightComponent } from './components/flight/flight.component';
import { RunwayComponent } from './components/runway/runway.component';
import { EventComponent } from './components/event/event.component';
import { MapComponent } from './map/map.component';
import { AdminComponent } from './components/admin/admin.component';
import { RegionComponent } from './components/region/region.component';
import { CountryComponent } from './components/country/country.component';
import { InstitutionComponent } from './components/institution/institution.component';
import { OrganisationComponent } from './components/organisation/organisation.component';

const routes: Routes = [
  {path: '', redirectTo: '/home', pathMatch: 'full'},
  {path: 'home', component: MapComponent },
  {path: 'airport/:airport_id', component: AirportComponent},
  {path: 'aircraft/:aircraft_id', component: AircraftComponent},
  {path: 'aircraft', component: AircraftComponent},
  {path: 'runway/:runway_id', component: RunwayComponent},
  {path: 'region/:region_id', component: RegionComponent},
  {path: 'country/:country_id', component: CountryComponent},
  {path: 'institution/:institution_id', component: InstitutionComponent},
  {path: 'airline/:airline_id', component: AirlineComponent},
  {path: 'airline', component: AirlineComponent},
  {path: 'flight/:flight_id', component: FlightComponent},
  {path: 'flight', component: FlightComponent},
  {path: 'person/:person_id', component: PersonComponent},
  {path: 'events/:event_id', component: EventComponent},
  {path: 'events', component: EventComponent},
  {path: 'orgs/:org_id', component: OrganisationComponent},
  {path: 'orgs', component: OrganisationComponent},
  {path: 'persons/:person_id', component: PersonComponent},
  {path: 'persons', component: PersonComponent},
  {path: 'admin', component: AdminComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
