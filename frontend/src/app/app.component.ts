import { Component } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatIconModule } from '@angular/material/icon';
import { MatExpansionModule } from '@angular/material/expansion';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterOutlet,
    RouterLink,
    RouterLinkActive,
    MatSidenavModule,
    MatListModule,
    MatToolbarModule,
    MatIconModule,
    MatExpansionModule
  ],
  template: `
    <mat-sidenav-container>
      <mat-sidenav mode="side" opened>
        <mat-nav-list>
          <a mat-list-item routerLink="/" routerLinkActive="active" [routerLinkActiveOptions]="{exact: true}">
            <mat-icon>home</mat-icon> Home
          </a>
          <a mat-list-item routerLink="/users" routerLinkActive="active">
            <mat-icon>people</mat-icon> Users
          </a>
          <a mat-list-item routerLink="/campaigns" routerLinkActive="active">
            <mat-icon>campaign</mat-icon> Campaigns
          </a>
          <mat-expansion-panel>
            <mat-expansion-panel-header>
              <mat-panel-title>
                <mat-icon>description</mat-icon> Docs
              </mat-panel-title>
            </mat-expansion-panel-header>
            <mat-nav-list>
              <a mat-list-item href="/docs" target="_blank">
                <mat-icon>api</mat-icon> API (Swagger)
              </a>
              <a mat-list-item routerLink="/docs/coding-guidelines" routerLinkActive="active">
                <mat-icon>code</mat-icon> Coding Guidelines
              </a>
              <a mat-list-item routerLink="/docs/general-guidelines" routerLinkActive="active">
                <mat-icon>list_alt</mat-icon> General Guidelines
              </a>
              <a mat-list-item routerLink="/docs/backend-guidelines" routerLinkActive="active">
                <mat-icon>storage</mat-icon> Backend Guidelines
              </a>
              <a mat-list-item routerLink="/docs/frontend-guidelines" routerLinkActive="active">
                <mat-icon>web</mat-icon> Frontend Guidelines
              </a>
            </mat-nav-list>
          </mat-expansion-panel>
        </mat-nav-list>
      </mat-sidenav>
      <mat-sidenav-content>
        <mat-toolbar color="primary">
          <span>{{title}}</span>
        </mat-toolbar>
        <router-outlet></router-outlet>
      </mat-sidenav-content>
    </mat-sidenav-container>
  `,
  styles: [`
    mat-sidenav-container {
      height: 100vh;
    }
    mat-sidenav {
      width: 200px;
    }
    .active {
      background-color: rgba(0,0,0,.1);
    }
  `]
})
export class AppComponent {
  title = 'Sales Manager';
}
