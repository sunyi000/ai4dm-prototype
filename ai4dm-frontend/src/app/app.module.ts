import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { MDBBootstrapModule } from 'angular-bootstrap-md';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LeafletMarkerClusterModule } from '@asymmetrik/ngx-leaflet-markercluster';
import { MapComponent } from './map/map.component';
import {LeafletModule} from '@asymmetrik/ngx-leaflet';
import { ConstantsService } from './common/services/constants.service';
import { HeaderComponent } from './header/header.component';
import { FooterComponent } from './footer/footer.component';
import {MatAutocompleteModule} from '@angular/material/autocomplete';
import {MatTableModule} from '@angular/material/table';
import {MatInputModule} from '@angular/material/input';
import {MatPaginatorModule} from '@angular/material/paginator';
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';
import {MatSortModule} from '@angular/material/sort';
import { ReactiveFormsModule } from '@angular/forms';
import { PopupComponent } from './popup/popup.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations'
import {FormsModule} from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { AirportTableComponent } from './components/airport-table/airport-table.component';
import { AirportComponent } from './components/airport/airport.component';
import { AirlineComponent } from './components/airline/airline.component';
import { RunwayComponent } from './components/runway/runway.component';
import { PersonComponent } from './components/person/person.component';
import { FlightComponent } from './components/flight/flight.component';
import { EventComponent } from './components/event/event.component';
import { AircraftComponent } from './components/aircraft/aircraft.component';
import { MatSelectModule } from '@angular/material/select';
import {MatCardModule} from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { AdminComponent } from './components/admin/admin.component';
import { UploadDialogComponent } from './components/upload-dialog/upload-dialog.component';
import { MatDialogModule } from '@angular/material/dialog';
import { RegionComponent } from './components/region/region.component';
import { CountryComponent } from './components/country/country.component';
import { InstitutionComponent } from './components/institution/institution.component';
import { OrganisationComponent } from './components/organisation/organisation.component';
// import { ResultsCardComponent } from './components/results-card/results-card.component';


@NgModule({
  declarations: [
    AppComponent,
    MapComponent,
    HeaderComponent,
    FooterComponent,
    PopupComponent,
    AirportTableComponent,
    AirportComponent,
    AirlineComponent,
    RunwayComponent,
    PersonComponent,
    FlightComponent,
    EventComponent,
    AircraftComponent,
    AdminComponent,
    UploadDialogComponent,
    RegionComponent,
    CountryComponent,
    InstitutionComponent,
    OrganisationComponent
    // ResultsCardComponent
 
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    LeafletMarkerClusterModule,
    LeafletModule,
    BrowserAnimationsModule,
    HttpClientModule,
    MatTableModule,
    MatInputModule,
    MatPaginatorModule,
    MatProgressSpinnerModule,
    MatSortModule,
    MatCardModule,
    MatFormFieldModule,
    MatSelectModule,
    MatDialogModule,
    FormsModule,
    ReactiveFormsModule,
    MatAutocompleteModule,
    MDBBootstrapModule.forRoot()
  ],
  providers: [ConstantsService],
  bootstrap: [AppComponent]
})
export class AppModule { }
