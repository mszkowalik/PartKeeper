import { NgModule } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";
import { RouterModule } from "@angular/router";
import { MatSidenavModule } from "@angular/material/sidenav";
import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
import { DemoMaterialModule } from "./material-module";
import { MatNativeDateModule } from "@angular/material/core";
import { HttpClientModule, HttpClient } from "@angular/common/http";
import {
  FormArray,
  ReactiveFormsModule,
  FormControl,
  FormsModule
} from "@angular/forms";

import { AppComponent } from "./app.component";
import { HomeComponent } from "./home/home.component";
import { TopBarComponent } from "./top-bar/top-bar.component";
import { ComponentsService } from "./components.service";
import { AdjustStockComponent } from "./adjust-stock/adjust-stock.component";
import { AdminConsoleComponent } from "./admin-console/admin-console.component";
import { PartSelectorComponent } from './part-selector/part-selector.component';
import { PartViewerComponent } from './part-viewer/part-viewer.component';

@NgModule({
  imports: [
    BrowserModule,
    ReactiveFormsModule,
    HttpClientModule,
    RouterModule.forRoot([
      { path: "", component: HomeComponent },
      { path: "adjustStock", component: AdjustStockComponent },
      { path: "adminConsole", component: AdminConsoleComponent }
    ]),
    MatSidenavModule,
    BrowserAnimationsModule,
    MatNativeDateModule,
    DemoMaterialModule,
    FormsModule
  ],
  declarations: [		
    AppComponent,
    HomeComponent,
    TopBarComponent,
    AdjustStockComponent,
    AdminConsoleComponent,
    PartViewerComponent,
    PartSelectorComponent,
   ],
  bootstrap: [AppComponent],
  providers: [ComponentsService, HttpClientModule]
})
export class AppModule {}
