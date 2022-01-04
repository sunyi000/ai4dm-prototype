import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { UploadDialogComponent } from '../upload-dialog/upload-dialog.component';
import { DataService } from '../../common/services/data.service';
import { HelperService } from 'src/app/common/services/helper.service';
import {MatDialog} from "@angular/material/dialog";


interface Datasource {
  value: string;
  viewValue: string;
}

interface Category {
  value: string;
  viewValue: string;
}
@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.css']
})
export class AdminComponent implements OnInit {

  fileToUpload: File | null = null;
  selectedDS : string;
  selectedCat : string;

  datasources : Datasource[]=[
    {value: 'FAA', viewValue: "FAA Data"},
    {value: 'OurAirports', viewValue: "Our Airports"},
    {value: 'OurFlights', viewValue: "Our Flights"}

  ];

  categories : Category[]=[
    {value: 'Aircraft', viewValue: "Aircraft Data"},
    {value: 'Airport', viewValue: "Airport Data"},
    {value: 'Airline', viewValue: "Airline Data"},
    {value: 'Flight', viewValue: "Flight Data"},
    {value: 'Runway', viewValue: "Runway Data"},
    {value: 'Incident', viewValue: "Incident Data"},
    {value: 'Person', viewValue: "Person Data"},
    {value: 'Organisation', viewValue: "Organisation Data"},
    {value: 'Institution', viewValue: "Institution Data"}


  ];

  constructor(
    private route: ActivatedRoute,
    private dialog: MatDialog,
    private dataService: DataService,
    private helperService:HelperService) {}

  ngOnInit(): void {
  }

  handleFileInput(files: FileList) {
    this.fileToUpload = files.item(0);
  }

  uploadFileToActivity() {
    this.dataService.postFile(this.fileToUpload,this.selectedDS,this.selectedCat).subscribe(data => {
      const dlg = this.dialog.open(UploadDialogComponent);
      dlg.afterClosed().subscribe(confirmresult=>{
        console.log(confirmresult)
        if (confirmresult){

        }else{

        }
      })
      console.log("upload success")
      }, error => {
        console.log(error);
      });
  }

}
