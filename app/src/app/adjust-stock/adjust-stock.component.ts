import { Component, OnInit } from "@angular/core";
import { ComponentsService } from "./../components.service";
import { Observable, Subscription } from "rxjs";
import { first } from "rxjs/operators";
import { Injectable } from '@angular/core';
import { NgModule } from '@angular/core';


@Component({
  selector: "app-adjust-stock",
  templateUrl: "./adjust-stock.component.html",
  styleUrls: ["./adjust-stock.component.css"]
})
export class AdjustStockComponent implements OnInit {

  currentPartNumber:string;
  partSubscription: Subscription;
  history: string[] = [];

  constructor(private componentsService: ComponentsService) {
  }

  selectedPartNumber(PN:string){
    this.currentPartNumber = PN;
  }
  updatedPartData(partData:any)
  {
    this.componentsService.setStock(partData)
    this.componentsService
      .getComponents().pipe(first())
        .toPromise().then(data=>{
          var message
          if(data['Part Number'] == this.currentPartNumber)    
          {
            message = `Successfully changed ${this.currentPartNumber}`;
            
          }
          else 
          {
            message = `Fail, when writing ${this.currentPartNumber}`;
          }
          this.history.push(message);
            console.info(this.history)
        });

  }
  ngOnInit() {

  }

}
