import { Component } from "@angular/core";

@Component({
  selector: "app-root",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.css"]
})
export class AppComponent {
  linkList = [
    { name: "Home", address: "" },
    { name: "Adjust Stock", address: "/adjustStock" },
    { name: "Admin Console", address: "/adminConsole" }
  ];

  constructor() {}
}
