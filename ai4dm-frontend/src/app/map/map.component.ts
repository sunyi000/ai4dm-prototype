import {AfterViewInit, Component, OnInit} from '@angular/core';
import { NgElement, WithProperties } from '@angular/elements';
// import {latLng, MapOptions, tileLayer} from 'leaflet';
import * as L from 'leaflet';
import "leaflet.markercluster";

import { DataService } from '../common/services/data.service';
import { ConstantsService } from '../common/services/constants.service';

import { PopupComponent } from '../popup/popup.component';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss']
})
export class MapComponent implements AfterViewInit {

  airports = [];

  constructor(private constantService: ConstantsService,private dataService:DataService ){

  }

  // Open Street Map Definition
  LAYER_OSM = {
    id: "map",
    name: "Open Street Map",
    enabled: false,
    layer: L.tileLayer("http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 18,
      attribution: "Open Street Map"
    })
  };
  // Values to bind to Leaflet Directive
  layersControlOptions = { position: "bottomright" };
  baseLayers = {
    "Open Street Map": this.LAYER_OSM.layer
  };
  options = {
    zoom: 4,
    center: L.latLng([-25, 135])
  };

  // Marker cluster stuff
  markerClusterGroup: L.MarkerClusterGroup;
  markerClusterData: any[] = [];
  markerClusterOptions: L.MarkerClusterGroupOptions;



  ngAfterViewInit() {
    this.dataService.get_all_airports(0).subscribe((result : any[])=>{
      this.dataService.airports = result;
      this.dataService.set_heads(this.dataService.airports)
      this.dataService.set_airports(this.dataService.airports);
      this.displayAirports();

      this.dataService.dataSource.data = this.dataService.airports;
      this.dataService.cols=Object.keys(result[0])
    });

  }

  markerClusterReady(group: L.MarkerClusterGroup) {
    this.markerClusterGroup = group;
  }

  displayAirports() {
    const data: any[] = [];
    for (var s of this.dataService.airports) 
    {
      const icon = L.icon({
        iconUrl: "marker-icon.png",
        shadowUrl: "marker-shadow.png"
      });
      var marker = L.marker([parseFloat(s.Latitude.value),parseFloat(s.Longitude.value)],{icon})
      marker.bindPopup(this.createPopupComponent(s))
      data.push(marker)
    }

    this.dataService.set_coordinates(data);
    this.markerClusterData=data;
  }

  createPopupComponent(s) {
    var popupEl = s.Airport.value +
              '<br/><b>Name:</b>' +s.Description.value +
              '<br/><b>IATA/FAA:</b> ' + s.IATA.value +
              '<br/><b>Elevation:</b> ' + s.Elevation.value + " ft" +
              '<br/><b>Type:</b> ' + s.Type.value +
              '<br/><b>GPS Code:</b> ' + s.GPS_Code.value +
              '<br/><b>Country:</b> ' + s.Country.value +
              '<br/><b>Municipality:</b> ' + s.Municipality.value +
              '<br/><b>Latitude:</b> ' + s.Latitude.value +
              '<br/><b>Longitude:</b> ' + s.Longitude.value +
              '<br/><b>Region Served:</b> ' + s.Region_Served.value

    return popupEl;
  }

}